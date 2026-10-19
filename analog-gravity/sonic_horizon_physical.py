#!/usr/bin/env python3
"""
Sonic horizon solver, phase 2: real-medium effects added to the Unruh metric.

Builds on sonic_horizon.py (same folder). Adds three physical effects, each
with a validation test against a known textbook answer:

  1. DISPERSION   d_xx -> d_xx - xi^2 d_xxxx
     Dispersion relation becomes omega^2 = c^2 k^2 + xi^2 k^4 (Bogoliubov /
     BEC-type, "superluminal"). Short waves outrun c, so infinite blueshift at
     a horizon is impossible. TEST: measured phase speed vs omega/k formula.

  2. NONLINEAR STEEPENING  v -> v + beta * u, with u = psi_x the acoustic
     particle velocity in units of c (the acoustic Mach number).
     IMPORTANT FIX vs the suggested code: the nonlinearity only means something
     if psi is in PHYSICAL units. psi_x must equal u/c (about 0.014 at 160 dB in
     air), not the arbitrary amplitude-1 packets of the linear solver; plugging
     beta*psi_x into an amplitude-1 field gives v_eff ~ hundreds of c and
     instant blow-up. This form is also only correct for right-moving waves
     (Burgers' simple-wave limit).
     TEST: shock (gradient catastrophe) time must match Burgers' formula
     t_s = 1 / (beta * eps * k * c).

  3. VISCOSITY  + nu * d_xx(pi). Damps the shortest waves.
     TEST: decay rate of a single mode must equal nu k^2 / 2.

Then the main experiment: the white-hole run from phase 1 repeated with
dispersion on, to see what happens instead of infinite blueshift.
"""

import math
import sys
import torch
from sonic_horizon import (AcousticMetricSolver, packet, horizon_profile,
                           check, DEV, DT_)


class PhysicalSolver(AcousticMetricSolver):
    def __init__(self, v, L=1.0, c=1.0, xi=0.0, beta=0.0, nu=0.0):
        super().__init__(v, L, c)
        self.xi, self.beta, self.nu = xi, beta, nu
        self.ikm2 = self.ikm * self.ikm
        self.ikm4 = self.ikm2 * self.ikm2

    def dxx_(self, f):
        return torch.fft.irfft(self.ikm2 * torch.fft.rfft(f), n=self.N)

    def rhs(self, psi, pi):
        # 4 real FFTs (5 with viscosity): every linear term is assembled in Fourier
        # space from the spectra of psi, v_eff*pi (and pi) -- was 14 complex FFTs.
        P = torch.fft.rfft(psi)
        psix = torch.fft.irfft(self.ikm * P, n=self.N)
        # v_eff appears in BOTH advection terms below, so a coefficient of
        # beta/2 gives a total steepening rate of beta (Burgers). Using beta
        # here steepens shocks twice as fast as real air (caught by test B1).
        v_eff = self.v + 0.5 * self.beta * psix
        dpsi = pi - v_eff * psix
        spec = -self.ikm * torch.fft.rfft(v_eff * pi) + self.c ** 2 * self.ikm2 * P
        if self.xi:
            spec = spec - self.xi ** 2 * self.ikm4 * P
        if self.nu:
            spec = spec + self.nu * self.ikm2 * torch.fft.rfft(pi)
        return dpsi, torch.fft.irfft(spec, n=self.N)

    def stable_dt(self, cfl=0.25):
        kmax = self.k.abs().max().item() * 2 / 3
        w = (self.v.abs().max().item() + self.c) * kmax + self.xi * kmax ** 2
        return cfl * 2.0 / max(w, 1e-12) * 1.4

    def energy(self, psi, pi):
        psix = self.dx_(psi)
        h = (0.5 * pi ** 2 - self.v * pi * psix + 0.5 * self.c ** 2 * psix ** 2
             + 0.5 * self.xi ** 2 * self.dx_(psix) ** 2)
        return (h.sum() * self.dx).item()


def advance(s, psi, pi, t, record_every=None, monitor=None):
    """monitor(psi, pi) must return a 0-d tensor (no .item()): frames and monitor
    values stay on the GPU during the loop and are transferred once at the end."""
    dt = s.stable_dt(); n = int(math.ceil(t / dt)); dt = t / n
    frames, times, mon = [], [], []
    for i in range(n + 1):
        if record_every and i % record_every == 0:
            frames.append(psi.clone()); times.append(i * dt)
        if monitor:
            mon.append(monitor(psi, pi))
        if i < n:
            psi, pi = s.step(psi, pi, dt)
    if frames:
        frames = list(torch.stack(frames).cpu())
    if mon:
        mon = list(zip((i * dt for i in range(n + 1)), torch.stack(mon).cpu().tolist()))
    return psi, pi, frames, times, mon


def main():
    c, L, N = 1.0, 1.0, 4096
    x = torch.arange(N, device=DEV, dtype=DT_) * (L / N)
    results = []
    print(f"Device: {DEV}   grid N={N}")

    # ---- D1: dispersion relation -------------------------------------------
    print("\nD1  dispersion: phase speed must equal sqrt(c^2 + xi^2 k^2)")
    xi = 3e-4
    s = PhysicalSolver(torch.zeros(N), L, c, xi=xi)
    m = 400; k = 2 * math.pi * m / L
    psi = torch.cos(k * x)
    w = k * math.sqrt(c ** 2 + xi ** 2 * k ** 2)
    pi = -w / k * s.dx_(psi)  # exact right-moving eigenmode
    T = 0.05
    psi, pi, *_ = advance(s, psi, pi, T)
    z = torch.fft.fft(psi)[m]
    phase_shift = -math.atan2(z.imag.item(), z.real.item())  # = -omega T mod 2pi
    w_meas = (2 * math.pi * round((w * T - phase_shift) / (2 * math.pi)) + phase_shift) / T
    results.append(check("phase speed", abs(w_meas / w - 1) < 1e-4,
                         f"{w_meas/k:.5f} c vs formula {w/k:.5f} c (k={k:.0f})"))

    # ---- V1: viscosity -----------------------------------------------------
    print("\nV1  viscosity: amplitude decay rate must equal nu k^2 / 2")
    nu = 2e-6
    s = PhysicalSolver(torch.zeros(N), L, c, nu=nu)
    m = 300; k = 2 * math.pi * m / L
    psi = torch.cos(k * x); pi = -c * s.dx_(psi)
    a0 = torch.fft.fft(psi)[m].abs().item()
    T = 0.2
    psi, pi, *_ = advance(s, psi, pi, T)
    rate = -math.log(torch.fft.fft(psi)[m].abs().item() / a0) / T
    results.append(check("decay rate", abs(rate / (nu * k * k / 2) - 1) < 0.02,
                         f"{rate:.3f} vs {nu*k*k/2:.3f} per unit time"))

    # ---- B1: Burgers shock time -------------------------------------------
    print("\nB1  nonlinear steepening: shock time must match Burgers t_s = 1/(beta eps k c)")
    beta = 1.2
    eps = 0.014                     # acoustic Mach number at ~160 dB in air
    m = 20; k = 2 * math.pi * m / L
    s = PhysicalSolver(torch.zeros(N), L, c, beta=beta)
    psi = -(eps / k) * torch.cos(k * x)       # u = psi_x = eps sin(kx)
    pi = -c * s.dx_(psi)
    g0 = eps * k
    ts_theory = 1.0 / (beta * eps * k * c)
    # inviscid Burgers: max gradient = g0 / (1 - t/t_s); reaches 5*g0 at t = 0.8 t_s
    mon = lambda p, q: s.dxx_(p).abs().max()
    psi, pi, _, _, hist = advance(s, psi, pi, 0.85 * ts_theory, monitor=mon)
    t5 = next((t for t, g in hist if g > 5 * g0), float("nan"))
    results.append(check("steepening time (gradient 5x)", abs(t5 / (0.8 * ts_theory) - 1) < 0.05,
                         f"sim {t5:.4f} vs Burgers {0.8*ts_theory:.4f}"))
    lam = 1.0 / m
    print(f"  -> in lab units, shock forms after {1/(beta*eps*2*math.pi):.2f} wavelengths"
          f" ({343/40e3/(beta*eps*2*math.pi)*100:.1f} cm at 40 kHz, 160 dB)")

    # ---- H: white hole with dispersion ------------------------------------
    print("\nH   white-hole horizon, linear, with vs without dispersion")
    N = 2048
    x = torch.arange(N, device=DEV, dtype=DT_) * (L / N)
    v, kappa = horizon_profile(N, L, c)
    A, B, kk = 0.4, 4.0, 2 * math.pi / L
    supersonic = ((x > 0.755) | (x < 0.245)).to(DT_)   # region beyond the white hole

    def past_horizon(s, psi):
        w2 = s.dx_(psi) ** 2  # gradient energy (|u|^2) as a position weight
        return (w2 * supersonic).sum().item() / w2.sum().item()

    out = {}
    for xi, t_more in ((0.0, 0.0), (3e-4, 0.35)):
        s = PhysicalSolver(v, L, c, xi=xi)
        psi, pi = packet(N, L, 0.62, 0.025, 150.0, c, None, +1)
        E0 = s.energy(psi, pi)
        k0, _ = s.local_k(psi)
        psi, pi, fr, tm, _ = advance(s, psi, pi, 0.55, record_every=40)
        k55, _ = s.local_k(psi)
        f55 = past_horizon(s, psi)
        f90 = None
        if t_more:
            psi, pi, fr2, tm2, _ = advance(s, psi, pi, t_more, record_every=40)
            fr = fr + fr2[1:]; tm = tm + [0.55 + t for t in tm2[1:]]
            f90 = past_horizon(s, psi)
        E1 = s.energy(psi, pi)
        out[xi] = (fr, tm, k55 / k0, f55, f90)
        results.append(check(f"energy conserved (xi={xi:g})", abs(E1 / E0 - 1) < 1e-3,
                             f"drift {abs(E1/E0-1):.1e}"))
        msg = f"    xi={xi:g}: at t=0.55 blueshift x{k55/k0:.1f}, energy past horizon {f55:.0%}"
        if f90 is not None:
            msg += f"; at t=0.90 energy past horizon {f90:.0%}"
        print(msg)
    results.append(check("dispersion caps the blueshift (same time, t=0.55)",
                         out[3e-4][2] < out[0.0][2],
                         f"x{out[3e-4][2]:.1f} with dispersion vs x{out[0.0][2]:.1f} without"))
    results.append(check("ideal metric: wave never crosses", out[0.0][3] < 0.05,
                         f"{out[0.0][3]:.0%} past horizon"))
    results.append(check("dispersive: wave escapes through the horizon",
                         out[3e-4][4] > 0.5, f"{out[3e-4][4]:.0%} past horizon by t=0.90"))

    print("\nSUMMARY:", "ALL TESTS PASS" if all(results) else "SOME TESTS FAILED")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    for a, xi, title in ((axs[0], 0.0, "Ideal Unruh metric (no dispersion)"),
                         (axs[1], 3e-4, "With dispersion  ξ = 3×10⁻⁴ L")):
        fr, tm, *_ = out[xi]
        img = torch.stack(fr).numpy()
        a.imshow(img, aspect="auto", origin="lower", cmap="RdBu_r",
                 extent=[0, L, 0, tm[-1]], vmin=-1, vmax=1, interpolation="nearest")
        a.axvline(0.75, color="k", lw=0.8, ls="--")
        a.set_xlim(0.55, 0.95); a.set_xlabel("x / L"); a.set_title(title)
    axs[0].set_ylabel("time (L/c)")
    axs[0].text(0.755, 0.05, "white-hole\nhorizon", fontsize=8)
    fig.tight_layout()
    fig.savefig("sonic_horizon_dispersion.png", dpi=140)
    print("Figure saved: sonic_horizon_dispersion.png")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
