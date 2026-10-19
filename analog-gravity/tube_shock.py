#!/usr/bin/env python3
"""
Does a resonator-loaded tube stop a shock from forming? Time-domain test of
plain vs periodic vs Fibonacci tubes at 5 kHz, 150-160 dB.

MODEL (same plane-wave duct + side-stub model as fibonacci_tube.py)
--------------------------------------------------------------------
* The duct carries a forward wave F and a backward wave G (pressure in units of
  rho c^2, i.e. acoustic Mach number). Each steepens on its own, Burgers-style:
  forward speed c(1 + beta F), backward speed -c(1 + beta G). Counter-propagating
  waves don't interact cumulatively in 1-D, so cross terms are dropped.
* Each ring = n_s closed quarter-wave stubs (total area S_b, effective length
  l_s + 0.85 r_s) joined to the duct at a point: pressure is continuous and
  volume flow is conserved. Stubs are linear, lossy delay lines.
* Wall loss: frequency-independent attenuation (Np/m), the Kirchhoff
  boundary-layer value at 2f = 10 kHz, separately for duct and stub radius.
  (Real wall loss grows like sqrt(f): this over-damps f by ~1.4x and
  under-damps 3f by ~1.2x.)
* Source at x=0 and exit after the last ring are anechoic.

NUMERICS
--------
Lattice with dx = c dt: linear propagation is an exact one-cell shift per step,
so junctions sit exactly between cells (dx is chosen so that every gap length is
within 0.4 um of a whole number of cells). Steepening is a separate sub-step
every NL_EVERY steps: Burgers flux beta F^2/2 on the lattice (Godunov,
Courant number NL_EVERY*beta*|F| << 1). At a junction the nonlinear flux leaving
the left segment uses the incoming value and the flux entering the right segment
uses the outgoing value (the junction conditions apply to point values).
The step loop is compiled with numba when available (bitwise identical to the
numpy loop, which remains as a fallback), and independent runs execute in
parallel worker processes.

VALIDATION (runs first; the comparison runs only if every check passes)
------------------------------------------------------------------------
L1  linear limit (tiny amplitude, full solver): transmission spectrum must match
    fibonacci_tube.T_dB (transfer matrices) with the same loss, for periodic
    and Fibonacci layouts at 55 and 144 rings
N1  no stubs, finite amplitude, no loss: the max gradient must reach 5x its
    initial value at 0.8 x_s, x_s = 1/(beta eps k) (Burgers; same check as B1)
N2  zero-area stubs at every ring position: junction bookkeeping must not change
    the nonlinear result vs a plain tube
C1  grid convergence: periodic tube at 160 dB, dx vs 2 dx

SPL convention as resonator_tube_design.py: L = 20 log10(p_peak / 20 uPa).
"""
import math
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fibonacci_tube import T_dB, layouts, gaps_list, c, rho, a, S, S_b, r_s, l_s

BETA = 1.2
NU, GAM, PR = 1.5e-5, 1.4, 0.71
F0 = 5e3                      # fundamental (Hz)
N_RINGS = 144                 # Fibonacci number; 1.23 m tube
DX = 0.0348385e-3             # lattice spacing (m), see docstring
NL_EVERY = 8
GRAD_H = 16                   # N1 gradient stencil half-width (0.56 mm, vs 2.2 mm gradient scale at 5x)
L_EFF = l_s + 0.85 * r_s      # stub length incl. end correction (as fibonacci_tube.py)
WORKERS = max(1, min(9, (os.cpu_count() or 2) - 1))  # parallel independent runs
NUMPY_LOOP = False            # True: force the (slow) numpy step loop even if numba is installed


def kirchhoff(f, radius):     # boundary-layer attenuation, Np/m (as resonator_tube_design.py)
    return math.sqrt(2 * math.pi * f * NU / 2) * (1 + (GAM - 1) / math.sqrt(PR)) / (radius * c)


ALPHA = (kirchhoff(2 * F0, a), kirchhoff(2 * F0, r_s))


def spl_to_eps(spl):
    return 20e-6 * 10 ** (spl / 20) / (rho * c * c)


def godunov(uL, uR):
    """Godunov flux for u^2/2."""
    fL, fR = 0.5 * uL * uL, 0.5 * uR * uR
    return np.where(uL > uR, np.maximum(fL, fR),
                    np.where(uL > 0, fL, np.where(uR < 0, fR, 0.0)))


def burgers_substep(U, j_out, j_in, k):
    """k * beta * d/dx(U^2/2) on the lattice (dx = c dt), segments joined at
    interfaces j_out|j_in. Ends: inflow at cell 0, outflow at the last cell."""
    h = 0.5 * U * U
    fl = godunov(U[:-1], U[1:])
    out = np.empty_like(U); inn = np.empty_like(U)
    out[:-1] = fl; out[-1] = h[-1]
    inn[1:] = fl; inn[0] = h[0]
    out[j_out] = h[j_out]; inn[j_in] = h[j_in]
    U -= k * BETA * (out - inn)


try:
    from numba import njit
except ImportError:          # falls back to the numpy step loop in Tube.run (same numbers, ~15x slower)
    njit = None

if njit:
    @njit(cache=True)
    def _burgers_nb(U, j_out, j_in, kb, fl, out, inn):
        """Same arithmetic, in the same order, as burgers_substep."""
        N = U.shape[0]
        for i in range(N - 1):
            uL, uR = U[i], U[i + 1]
            fL, fR = 0.5 * uL * uL, 0.5 * uR * uR
            if uL > uR:
                fl[i] = fL if fL > fR else fR
            elif uL > 0:
                fl[i] = fL
            elif uR < 0:
                fl[i] = fR
            else:
                fl[i] = 0.0
        for i in range(N - 1):
            out[i] = fl[i]; inn[i + 1] = fl[i]
        out[N - 1] = 0.5 * U[N - 1] * U[N - 1]; inn[0] = 0.5 * U[0] * U[0]
        for j in j_out:
            out[j] = 0.5 * U[j] * U[j]
        for j in j_in:
            inn[j] = 0.5 * U[j] * U[j]
        for i in range(N):
            U[i] -= kb * (out[i] - inn[i])

    @njit(cache=True)
    def _run_nb(src, nsteps, N, e, s, r_out, r_in, rs, fr, m, M, w, Sd, Sb, q,
                nl_every, kb, n0, n1, h, gmax):
        """The Tube.run step loop compiled; same arithmetic, in the same order."""
        K = e.shape[0]
        F = np.zeros(N); G = np.zeros(N); buf = np.zeros((M, K)); exit_ = np.empty(nsteps)
        FL = np.empty(K); GR = np.zeros(K); p = np.empty(K)
        fl = np.empty(N - 1); out = np.empty(N); inn = np.empty(N)
        Gr = G[::-1]
        for n in range(nsteps):
            i1, i2, iw = (n - m) % M, (n - m - 1) % M, n % M
            for j in range(K):
                b = rs * ((1 - fr) * buf[i1, j] + fr * buf[i2, j])
                FL[j] = F[e[j]]
                if j < K - 1:
                    GR[j] = G[s[j]]
                p[j] = w * (Sd * FL[j] + Sd * GR[j] + Sb * b)
                buf[iw, j] = p[j] - b
            # shift + loss fused: same multiply by q on the same values as the numpy loop
            for i in range(N - 1, 0, -1):
                F[i] = F[i - 1] * q
            F[0] = src[n] * q
            for j in range(K - 1):
                F[s[j]] = (p[j] - GR[j]) * q
            exit_[n] = p[K - 1] - GR[K - 1]
            for i in range(N - 1):
                G[i] = G[i + 1] * q
            G[N - 1] *= q
            for j in range(K):
                G[e[j]] = (p[j] - FL[j]) * q
            if kb != 0.0 and n % nl_every == 0:
                _burgers_nb(F, e[:-1], s, kb, fl, out, inn)
                _burgers_nb(Gr, r_out, r_in, kb, fl, out, inn)
            if n0 <= n < n1:
                for i in range(N - 2 * h):
                    v = abs(F[i + 2 * h] - F[i])
                    if v > gmax[i]:
                        gmax[i] = v
        return exit_


class Tube:
    """Duct of segments (lengths `gaps`), a ring of stubs after each segment.
    stub_area=0 gives transparent junctions; gaps=[L] with stub_area=0 is a plain tube."""

    def __init__(self, gaps, dx=DX, stub_area=S_b, alpha=ALPHA, beta=BETA):
        n = np.maximum(1, np.round(np.asarray(gaps) / dx)).astype(int)
        self.N = int(n.sum()); self.K = len(n)
        starts = np.concatenate(([0], np.cumsum(n)[:-1]))
        self.e = starts + n - 1                  # last cell before each ring
        self.s = starts[1:]                      # first cell after rings 1..K-1
        self.dx, self.dt = dx, dx / c
        self.q = math.exp(-alpha[0] * dx)
        D = 2 * L_EFF / c / self.dt              # stub round trip, in steps
        self.m, self.fr = int(D), D - int(D)
        self.M = self.m + 2
        self.rs = math.exp(-2 * alpha[1] * L_EFF)
        self.Sb, self.beta = stub_area, beta
        self.length = self.N * dx
        # reversed-lattice junction indices for the backward wave
        self.r_out, self.r_in = self.N - 1 - self.s, self.N - 1 - self.e[:-1]

    def run(self, src, nsteps, track_grad=None):
        """src: F at x=0 for each step. Returns exit pressure (Mach units) per step.
        track_grad=(n0, n1): also return max |dF/dx| over steps n0..n1 at cell
        centres GRAD_H..N-1-GRAD_H, from a centred difference over +-GRAD_H cells
        (a one-cell difference picks up ~1e-3 cell-scale jitter from the Godunov
        flux switch at F = 0 and turns it into a spurious gradient)."""
        N, K, e, s = self.N, self.K, self.e, self.s
        F = np.zeros(N); G = np.zeros(N); buf = np.zeros((self.M, K))
        exit_ = np.empty(nsteps); GR = np.zeros(K)
        w = 2 / (2 * S + self.Sb)
        h = GRAD_H
        gmax = np.zeros(N - 2 * h) if track_grad else None
        if njit and not NUMPY_LOOP:
            n0, n1 = track_grad or (0, 0)
            exit_ = _run_nb(np.asarray(src, dtype=float), nsteps, N, e, s, self.r_out, self.r_in,
                            self.rs, self.fr, self.m, self.M, w, S, self.Sb, self.q, NL_EVERY,
                            NL_EVERY * BETA if self.beta else 0.0, n0, n1, h,
                            gmax if track_grad else np.zeros(1))
            return (exit_, gmax / (2 * h * self.dx)) if track_grad else exit_
        for n in range(nsteps):
            b = self.rs * ((1 - self.fr) * buf[(n - self.m) % self.M] + self.fr * buf[(n - self.m - 1) % self.M])
            FL = F[e]; GR[:-1] = G[s]
            p = w * (S * FL + S * GR + self.Sb * b)   # junction pressure
            buf[n % self.M] = p - b                   # wave sent into the stubs
            F[1:] = F[:-1]; F[0] = src[n]; F[s] = (p - GR)[:-1]; exit_[n] = p[-1] - GR[-1]
            G[:-1] = G[1:]; G[e] = p - FL
            F *= self.q; G *= self.q
            if self.beta and n % NL_EVERY == 0:
                burgers_substep(F, e[:-1], s, NL_EVERY)
                burgers_substep(G[::-1], self.r_out, self.r_in, NL_EVERY)
            if track_grad and track_grad[0] <= n < track_grad[1]:
                np.maximum(gmax, np.abs(F[2 * h:] - F[:-2 * h]), out=gmax)
        return (exit_, gmax / (2 * h * self.dx)) if track_grad else exit_


def harmonics(sig, dt, f0, nper=10, nh=30):
    """Peak amplitudes of harmonics 1..nh over the last nper periods (least squares)."""
    n = int(round(nper / f0 / dt)); y = sig[-n:]; t = np.arange(n) * dt
    cols = [np.ones(n)] + [fn(2 * np.pi * h * f0 * t) for h in range(1, nh + 1) for fn in (np.cos, np.sin)]
    co = np.linalg.lstsq(np.array(cols).T, y, rcond=None)[0]
    return np.hypot(co[1::2], co[2::2])


def tone(eps, nsteps, dt, f0=F0, ramp_periods=2):
    t = np.arange(nsteps) * dt
    env = np.where(t < ramp_periods / f0, 0.5 - 0.5 * np.cos(np.pi * t * f0 / ramp_periods), 1.0)
    return eps * env * np.sin(2 * np.pi * f0 * t)


def check(name, ok, detail):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return ok


def spl(amp_mach):
    return 20 * np.log10(np.maximum(amp_mach * rho * c * c, 1e-30) / 20e-6)


def steady_run(tube, level, settle=8.0):
    """Drive at `level` dB until `settle` extra transits after the front, return exit signal.
    f settles within ~2 transits, but the 2f/3f residues ~70 dB below f in the stub
    tubes need ~6-7 (start-up ringing near the band edges); 8 leaves margin."""
    nsteps = int(((1 + settle) * tube.length / c + 2 / F0 + 20 / F0) / tube.dt)
    return tube.run(tone(spl_to_eps(level), nsteps, tube.dt), nsteps)


def _sim(job):
    """One independent simulation (runs in a worker process)."""
    kind, gaps, kw, arg = job
    tube = Tube(gaps, **kw)
    if kind == "l1":                          # broadband pulse, tiny amplitude
        sig_t = 2 / (2 * np.pi * 25e3)        # Gaussian pulse, still ~-17 dB at 25 kHz
        nsteps = int(0.08 / tube.dt)
        t = np.arange(nsteps) * tube.dt
        src = 1e-9 * np.exp(-0.5 * ((t - 8 * sig_t) / sig_t) ** 2)
        out = tube.run(src, nsteps)
        tail = np.sum(out[-nsteps // 10:] ** 2) / np.sum(out ** 2)
        f = np.fft.rfftfreq(nsteps, tube.dt)
        sel = (f >= 500) & (f <= 25000)
        return f[sel], 20 * np.log10(np.abs(np.fft.rfft(out)[sel] / np.fft.rfft(src)[sel])), tail
    if kind == "n1":                          # max gradient over one period, steady state
        n0 = int((tube.length / c + 4 / F0) / tube.dt); n1 = n0 + int(1 / F0 / tube.dt) + 1
        return tube.run(tone(arg, n1, tube.dt), n1, track_grad=(n0, n1))[1]
    return steady_run(tube, arg), tube.dt     # "steady": tone at `arg` dB


def run_all(jobs):
    """Independent runs in parallel worker processes; results in job order (each run
    is deterministic, so the numbers don't depend on which process ran it)."""
    if WORKERS > 1 and len(jobs) > 1:
        with ProcessPoolExecutor(min(WORKERS, len(jobs))) as ex:
            return list(ex.map(_sim, jobs))
    return [_sim(j) for j in jobs]


def main():
    t_start = time.time()
    results = []
    print(f"lattice dx = {DX*1e3:.5f} mm, dt = {DX/c*1e9:.1f} ns; nonlinear sub-step every {NL_EVERY} steps")
    print(f"wall loss (Kirchhoff at {2*F0/1e3:g} kHz): duct {ALPHA[0]:.3f} Np/m, stubs {ALPHA[1]:.3f} Np/m")
    eps = spl_to_eps(160); k = 2 * np.pi * F0 / c
    per, fib, _ = layouts(N_RINGS)
    l1_cases = [(N, name, gaps) for N in (55, 144)
                for name, gaps in zip(("periodic", "fibonacci"), layouts(N)[:2])]
    plain = dict(stub_area=0.0)
    jobs = ([("l1", gaps, {}, None) for _, _, gaps in l1_cases]
            + [("n1", [0.75], dict(stub_area=0.0, alpha=(0.0, 0.0)), eps)]
            + [("steady", [sum(per)], plain, 160), ("steady", per, plain, 160)]
            + [("steady", per, {}, 160), ("steady", per, dict(dx=2 * DX), 160)])
    out = run_all(jobs)

    # ---- L1: linear limit vs transfer matrices --------------------------------
    print("\nL1  linear limit: time-domain transmission vs fibonacci_tube.T_dB (same loss)")
    l1 = {}
    for (N, name, gaps), (f, Ttd, tail) in zip(l1_cases, out[:4]):
        Ttm = T_dB(f, gaps, alpha=ALPHA)
        mask = Ttm > -40
        err = np.max(np.abs(Ttd - Ttm)[mask])
        gtd = [(lo, hi) for lo, hi, ed in gaps_list(Ttd, freqs=f) if not ed]
        gtm = [(lo, hi) for lo, hi, ed in gaps_list(Ttm, freqs=f) if not ed]
        edge_err = (max(max(abs(x1 - x2), abs(y1 - y2)) for (x1, y1), (x2, y2) in zip(gtd, gtm))
                    if len(gtd) == len(gtm) and gtd else float("inf"))
        results.append(check(f"{N} rings {name}: |T| where T > -40 dB", err < 0.5,
                             f"max error {err:.3f} dB (tail energy {tail:.1e})"))
        results.append(check(f"{N} rings {name}: gaps < -20 dB", len(gtd) == len(gtm) and edge_err < 0.1,
                             f"{len(gtd)} vs {len(gtm)} gaps, edges within {edge_err*1e3:.0f} Hz"))
        l1[(N, name)] = (f, Ttd, Ttm)
        # informational: how much the loss model matters for the gap structure
        if N == 55:
            gdef = [(lo, hi) for lo, hi, ed in gaps_list(T_dB(f, gaps), freqs=f) if not ed]
            print(f"    (fibonacci_tube.py default loss gives {len(gdef)} gaps: "
                  + ", ".join(f"{x:.1f}-{y:.1f}" for x, y in gdef) + " kHz; this loss: "
                  + ", ".join(f"{x:.1f}-{y:.1f}" for x, y in gtm) + " kHz)")

    # ---- N1: Burgers steepening distance, no stubs, no loss ------------------
    print("\nN1  no stubs, finite amplitude: steepening distance vs Burgers x_s = 1/(beta eps k)")
    xs = 1 / (BETA * eps * k)
    ratio = out[4] / (eps * k)
    x5 = (np.argmax(ratio > 5) + GRAD_H + 0.5) * DX if (ratio > 5).any() else float("nan")
    results.append(check("gradient 5x distance", abs(x5 / (0.8 * xs) - 1) < 0.05,
                         f"sim {x5:.4f} m vs Burgers 0.8 x_s = {0.8*xs:.4f} m (160 dB, x_s = {xs:.3f} m)"))

    # ---- N2: transparent junctions -------------------------------------------
    print("\nN2  zero-area stubs at every ring: must reproduce the plain tube (160 dB)")
    hp, hj = (harmonics(sig, dt, F0) for sig, dt in out[5:7])
    dd = np.abs(spl(hj[:3]) - spl(hp[:3]))
    results.append(check("f, 2f, 3f at exit", dd.max() < 0.2,
                         "differences " + ", ".join(f"{x:.3f}" for x in dd) + " dB"))

    # ---- C1: grid convergence -------------------------------------------------
    print("\nC1  grid convergence: periodic tube, 160 dB, dx vs 2 dx")
    h1, h2 = (harmonics(sig, dt, F0) for sig, dt in out[7:9])
    dd = np.abs(spl(h1[:3]) - spl(h2[:3]))
    results.append(check("f, 2f, 3f at exit", dd.max() < 1.0,
                         "differences " + ", ".join(f"{x:.2f}" for x in dd) + " dB"))

    allok = all(results)
    print("\nVALIDATION:", "ALL TESTS PASS" if allok else "SOME TESTS FAILED -- comparison not run")
    plot_validation(l1)
    if not allok:
        return 1

    # ---- comparison -----------------------------------------------------------
    L = sum(per)
    tubes = (("plain", [L], plain), ("periodic", per, {}), ("Fibonacci", fib, {}))
    levels = (150, 155, 160)
    out = run_all([("steady", gaps, kw, level) for level in levels for _, gaps, kw in tubes])
    print(f"\nCOMPARISON  5 kHz, {N_RINGS} rings, tube length {L:.3f} m, exit levels (dB re 20 uPa, peak)")
    print("  level   x/x_s   tube         f       2f      3f     2f-f    3f-f")
    wave = {}
    for (level, (name, _, _)), (sig, dt) in zip(((lv, t) for lv in levels for t in tubes), out):
        xs = 1 / (BETA * spl_to_eps(level) * k)
        h = harmonics(sig, dt, F0)
        hprev = harmonics(sig[:-int(round(10 / F0 / dt))], dt, F0)
        Lh = spl(h[:3])
        drift = np.max(np.abs(Lh - spl(hprev[:3])))
        print(f"  {level} dB  {L/xs:5.2f}   {name:10s} {Lh[0]:7.1f} {Lh[1]:7.1f} {Lh[2]:7.1f} "
              f"{Lh[1]-Lh[0]:7.1f} {Lh[2]-Lh[0]:7.1f}   (steady to {drift:.2f} dB)")
        nper = int(round(2 / F0 / dt))
        wave[(level, name)] = (sig[-nper:] / spl_to_eps(level), Lh)
    plot_waveforms(wave, [n for n, _, _ in tubes], L)
    print(f"\nrun time {time.time()-t_start:.0f} s")
    return 0


def plot_validation(l1):
    fig, ax = plt.subplots(2, 2, figsize=(12, 6.5), sharex=True, sharey=True)
    for a_, key in zip(ax.ravel(), sorted(l1)):
        f, Ttd, Ttm = l1[key]
        a_.plot(f / 1e3, Ttm, color="0.6", lw=2.5, label="transfer matrix")
        a_.plot(f / 1e3, Ttd, color="#2b6cb0" if key[1] == "periodic" else "#b7791f", lw=0.9, label="time domain")
        a_.set_ylim(-80, 3); a_.set_title(f"{key[0]} rings, {key[1]}", fontsize=10); a_.legend(fontsize=8, loc="lower right")
    for a_ in ax[:, 0]: a_.set_ylabel("transmission (dB)")
    for a_ in ax[1]: a_.set_xlabel("frequency (kHz)")
    fig.suptitle("L1: linear limit of the time-domain solver vs transfer matrices (same loss)")
    fig.tight_layout(); fig.savefig("tube_shock_validation.png", dpi=140)
    print("saved tube_shock_validation.png")


def plot_waveforms(wave, names, L):
    levels = sorted({k[0] for k in wave})
    fig, ax = plt.subplots(len(levels), len(names), figsize=(13, 8), sharex=True, sharey=True)
    cols = {"plain": "#c05621", "periodic": "#2b6cb0", "Fibonacci": "#b7791f"}
    for i, lev in enumerate(levels):
        for j, nm in enumerate(names):
            y, Lh = wave[(lev, nm)]
            t = np.arange(len(y)) / len(y) * 2
            a_ = ax[i, j]; a_.plot(t, y, color=cols[nm], lw=1.2); a_.axhline(0, color="0.8", lw=0.6)
            a_.text(0.02, 0.04, f"2f {Lh[1]-Lh[0]:+.1f} dB, 3f {Lh[2]-Lh[0]:+.1f} dB re f",
                    transform=a_.transAxes, fontsize=8)
            if i == 0: a_.set_title(f"{nm} tube", fontsize=11)
            if j == 0: a_.set_ylabel(f"{lev} dB in\np_exit / p_in")
            if i == len(levels) - 1: a_.set_xlabel("time (periods)")
    fig.suptitle(f"Exit waveforms after {L:.2f} m at 5 kHz: plain vs resonator-loaded tubes ({N_RINGS} rings)")
    fig.tight_layout(); fig.savefig("tube_shock.png", dpi=140)
    print("saved tube_shock.png")


if __name__ == "__main__":
    sys.exit(main())
