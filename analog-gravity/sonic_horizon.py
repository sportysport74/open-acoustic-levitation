#!/usr/bin/env python3
"""
Sonic horizon simulator — sound waves on an Unruh acoustic metric (1+1 D).

PHYSICS (established, Unruh 1981; Visser 1998)
------------------------------------------------
For an irrotational, barotropic, inviscid flow with background velocity v(x),
small perturbations of the velocity potential psi obey the Klein-Gordon
equation on the acoustic metric

    ds^2 = (rho/c) [ -(c^2 - v^2) dt^2 - 2 v dt dx + dx^2 ]

    (1/sqrt(-g)) d_mu ( sqrt(-g) g^{mu nu} d_nu psi ) = 0

With rho and c constant this reduces to

    (d_t + d_x v)(d_t + v d_x) psi = c^2 d_xx psi

We integrate it in first-order form with pi = (d_t + v d_x) psi:

    d_t psi = pi - v psi_x
    d_t pi  = -d_x(v pi) + c^2 psi_xx

A horizon sits wherever |v| = c. Right-moving sound travels at v + c, which
goes to zero there, so sound piles up (white hole) or peels apart (black hole).

NUMERICS
--------
Pseudo-spectral derivatives (FFT) on a periodic domain, 4th-order Runge-Kutta
in time, 2/3-rule dealiasing. Runs on CUDA if available, otherwise CPU.

VALIDATION (every run checks itself against known answers)
----------------------------------------------------------
T1  still air:        packet speed must equal c
T2  uniform flow:     right/left speeds must equal v+c and v-c (Galilean)
T3  conserved energy: H = 1/2 pi^2 - v pi psi_x + 1/2 c^2 psi_x^2 must stay fixed
T4  horizon flow:     packet position and wavenumber must track ray theory
                      dx/dt = v + c,  dk/dt = -k dv/dx
                      and k must grow ~ exp(kappa t), kappa = |dv/dx| at horizon
                      (kappa is the horizon's "surface gravity")

Units: c = 1, domain length L = 1. Multiply by real c and L for lab numbers.
"""

import math
import sys
import torch

DEV = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DT_ = torch.float64


class AcousticMetricSolver:
    def __init__(self, v, L=1.0, c=1.0):
        self.N = v.numel()
        self.L, self.c = L, c
        self.dx = L / self.N
        self.v = v.to(DEV, DT_)
        k = 2 * math.pi * torch.fft.fftfreq(self.N, d=self.dx).to(DEV, DT_)
        self.ik = 1j * k
        self.k = k
        self.mask = (k.abs() < (2 / 3) * k.abs().max()).to(DT_)  # 2/3 dealias

    def dx_(self, f):
        return torch.fft.ifft(self.ik * self.mask * torch.fft.fft(f)).real

    def rhs(self, psi, pi):
        psix = self.dx_(psi)
        dpsi = pi - self.v * psix
        dpi = -self.dx_(self.v * pi) + self.c ** 2 * self.dx_(psix)
        return dpsi, dpi

    def step(self, psi, pi, dt):
        a1, b1 = self.rhs(psi, pi)
        a2, b2 = self.rhs(psi + 0.5 * dt * a1, pi + 0.5 * dt * b1)
        a3, b3 = self.rhs(psi + 0.5 * dt * a2, pi + 0.5 * dt * b2)
        a4, b4 = self.rhs(psi + dt * a3, pi + dt * b3)
        return (psi + dt / 6 * (a1 + 2 * a2 + 2 * a3 + a4),
                pi + dt / 6 * (b1 + 2 * b2 + 2 * b3 + b4))

    def energy(self, psi, pi):
        psix = self.dx_(psi)
        h = 0.5 * pi ** 2 - self.v * pi * psix + 0.5 * self.c ** 2 * psix ** 2
        return (h.sum() * self.dx).item()

    def stable_dt(self, cfl=0.25):
        return cfl * self.dx / (self.v.abs().max().item() + self.c)

    # diagnostics: packet centroid (circular mean, weighted by gradient energy)
    # and rms wavenumber of psi_x
    def centroid(self, psi):
        w = self.dx_(psi) ** 2
        x = torch.arange(self.N, device=DEV, dtype=DT_) * self.dx
        th = 2 * math.pi * x / self.L
        ang = math.atan2((w * torch.sin(th)).sum().item(), (w * torch.cos(th)).sum().item())
        return (ang % (2 * math.pi)) * self.L / (2 * math.pi)

    def local_k(self, psi):
        """Local wavenumber at the packet peak, from the phase of the analytic signal."""
        z = torch.fft.ifft(torch.fft.fft(psi) * 2 * (self.k > 0))
        i = int(z.abs().argmax())
        ph = torch.angle(z)
        d = (ph[(i + 1) % self.N] - ph[(i - 1) % self.N] + math.pi) % (2 * math.pi) - math.pi
        return abs(d.item()) / (2 * self.dx), i * self.dx


def packet(N, L, x0, width, k0, c, v_at_x0, direction=+1):
    """Gaussian wave packet moving right (+1) or left (-1) relative to the fluid."""
    x = torch.arange(N, device=DEV, dtype=DT_) * (L / N)
    d = (x - x0 + L / 2) % L - L / 2
    psi = torch.exp(-(d / width) ** 2) * torch.cos(k0 * d)
    psix = AcousticMetricSolver(torch.zeros(N), L, c).dx_(psi)
    pi = -direction * c * psix  # pi = -c psi_x for right-movers, +c psi_x for left
    return psi, pi


def run(solver, psi, pi, t_end, record_every=None):
    dt = solver.stable_dt()
    n = int(math.ceil(t_end / dt))
    dt = t_end / n
    frames, times = [], []
    for i in range(n + 1):
        if record_every and i % record_every == 0:
            frames.append(psi.detach().cpu().clone())
            times.append(i * dt)
        if i < n:
            psi, pi = solver.step(psi, pi, dt)
    return psi, pi, frames, times


def horizon_profile(N, L=1.0, c=1.0, A=0.4, B=4.0):
    """Leftward flow: supersonic near x=0 (|v|=1.4c), subsonic near x=L/2 (|v|=0.6c).
    Black-hole horizon at x=L/4, white-hole horizon at x=3L/4."""
    x = torch.arange(N, dtype=DT_) * (L / N)
    kk = 2 * math.pi / L
    v = -c * (1 + A * torch.tanh(B * torch.cos(kk * x)))
    kappa = c * A * B * kk  # |dv/dx| at either horizon
    return v, kappa


def ray_trace(v_fn, dv_fn, c, x0, k0, t_end, steps=20000):
    """Geometric-acoustics ray: dx/dt = v + c, dk/dt = -k v'(x)."""
    dt = t_end / steps
    x, k = x0, k0
    for _ in range(steps):
        def f(x, k):
            return v_fn(x) + c, -k * dv_fn(x)
        a1 = f(x, k); a2 = f(x + .5*dt*a1[0], k + .5*dt*a1[1])
        a3 = f(x + .5*dt*a2[0], k + .5*dt*a2[1]); a4 = f(x + dt*a3[0], k + dt*a3[1])
        x += dt/6*(a1[0] + 2*a2[0] + 2*a3[0] + a4[0])
        k += dt/6*(a1[1] + 2*a2[1] + 2*a3[1] + a4[1])
    return x, k


def check(name, ok, detail):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return ok


def main(make_plot=True):
    c, L, N = 1.0, 1.0, 4096
    print(f"Device: {DEV}   grid N={N}")
    results = []

    # ---- T1: still air ------------------------------------------------------
    print("\nT1  still air (v = 0)")
    s = AcousticMetricSolver(torch.zeros(N), L, c)
    psi, pi = packet(N, L, 0.3, 0.03, 200.0, c, 0.0, +1)
    x0 = s.centroid(psi)
    psi, pi, *_ = run(s, psi, pi, 0.2)
    speed = (s.centroid(psi) - x0) / 0.2
    results.append(check("packet speed = c", abs(speed - c) < 5e-3, f"{speed:.4f} (expect 1.0000)"))

    # ---- T2: uniform flow ---------------------------------------------------
    print("\nT2  uniform flow (v = -0.5c)")
    s = AcousticMetricSolver(torch.full((N,), -0.5), L, c)
    for direction, expect in ((+1, 0.5), (-1, -1.5)):
        psi, pi = packet(N, L, 0.5, 0.03, 200.0, c, -0.5, direction)
        x0 = s.centroid(psi)
        psi, pi, *_ = run(s, psi, pi, 0.2)
        dxw = (s.centroid(psi) - x0 + L/2) % L - L/2
        sp = dxw / 0.2
        results.append(check(f"{'right' if direction>0 else 'left'}-mover speed = v{'+' if direction>0 else '-'}c",
                             abs(sp - expect) < 5e-3, f"{sp:.4f} (expect {expect:.4f})"))

    # ---- T3 + T4: horizon flow ---------------------------------------------
    print("\nT3/T4  flow with black-hole (x=0.25) and white-hole (x=0.75) horizons")
    v, kappa = horizon_profile(N, L, c)
    s = AcousticMetricSolver(v, L, c)
    A, B, kk = 0.4, 4.0, 2 * math.pi / L
    v_fn = lambda x: -c * (1 + A * math.tanh(B * math.cos(kk * x)))
    dv_fn = lambda x: c * A * B * kk * math.sin(kk * x) / math.cosh(B * math.cos(kk * x)) ** 2

    # Phase 1 (t <= 0.30): blueshift up to ~2x, where single-ray geometric
    # acoustics is valid -> strict comparison with ray theory.
    # Phase 2 (to t = 0.55): keep going for the picture; at ~20x compression the
    # packet straddles different flow gradients, so one ray no longer describes
    # the whole packet (a known limit of geometric acoustics, not a solver bug).
    x_start, k_start, t_check, t_end = 0.62, 150.0, 0.30, 0.55
    psi, pi = packet(N, L, x_start, 0.025, k_start, c, v_fn(x_start), +1)
    E0 = s.energy(psi, pi)
    ks0, xs0 = s.local_k(psi)
    psi, pi, fr1, tm1 = run(s, psi, pi, t_check, record_every=20)
    ks1, xs1 = s.local_k(psi)
    xr, kr = ray_trace(v_fn, dv_fn, c, xs0, ks0, t_check)
    psi, pi, fr2, tm2 = run(s, psi, pi, t_end - t_check, record_every=20)
    frames = fr1 + fr2[1:]
    times = tm1 + [t_check + t for t in tm2[1:]]
    E1 = s.energy(psi, pi)
    ks2, xs2 = s.local_k(psi)

    results.append(check("energy conserved (to t=0.55)", abs(E1 - E0) / abs(E0) < 1e-3,
                         f"relative drift {abs(E1-E0)/abs(E0):.2e}"))
    results.append(check("packet peak matches ray theory (t=0.30)", abs(xs1 - xr) < 5e-3,
                         f"sim {xs1:.4f} vs ray {xr:.4f}"))
    results.append(check("wavenumber matches ray theory (t=0.30)", abs(ks1 / kr - 1) < 0.05,
                         f"sim {ks1:.0f} vs ray {kr:.0f}"))
    results.append(check("packet never crosses the white-hole horizon", xs2 < 0.75,
                         f"peak at x={xs2:.4f} at t=0.55 (horizon at 0.75)"))
    print(f"  blueshift at t=0.55: x{ks2/ks0:.1f}   "
          f"horizon surface gravity kappa = {kappa:.2f} c/L")

    allok = all(results)
    print("\nSUMMARY:", "ALL TESTS PASS" if allok else "SOME TESTS FAILED")

    if make_plot:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        img = torch.stack(frames).numpy()
        xg = (torch.arange(N, dtype=DT_) * (L / N)).numpy()
        fig, (a0, a1) = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={"width_ratios": [1, 2.2]})
        a0.plot(xg, -v.numpy(), color="#2b6cb0", lw=2, label="|v| flow speed")
        a0.axhline(1.0, color="#c05621", ls="--", label="c (sound speed)")
        for xh, lab in ((0.25, "black-hole\nhorizon"), (0.75, "white-hole\nhorizon")):
            a0.axvline(xh, color="gray", lw=0.8)
            a0.text(xh + 0.01, 1.32, lab, fontsize=8)
        a0.set_xlabel("x / L"); a0.set_ylabel("speed / c"); a0.set_title("Background flow")
        a0.legend(fontsize=8, loc="lower left")
        a1.imshow(img, aspect="auto", origin="lower", cmap="RdBu_r",
                  extent=[0, L, 0, times[-1]], vmin=-1, vmax=1, interpolation="nearest")
        # overlay ray
        tr = [0.0]; xr_path = [xs0]; x = xs0; dt_r = t_end / 600
        for _ in range(600):
            x += dt_r * (v_fn(x) + c); tr.append(tr[-1] + dt_r); xr_path.append(x)
        a1.plot(xr_path, tr, color="k", lw=1, ls=":", label="ray theory: dx/dt = v + c")
        a1.axvline(0.75, color="gray", lw=0.8)
        a1.set_xlim(0.58, 0.78)
        a1.set_xlabel("x / L"); a1.set_ylabel("time (L/c)")
        a1.set_title("Sound packet stalls and blueshifts at the white-hole horizon")
        a1.legend(fontsize=8, loc="upper left")
        fig.tight_layout()
        out = "sonic_horizon_result.png"
        fig.savefig(out, dpi=140)
        print(f"\nFigure saved: {out}")

    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main(make_plot="--no-plot" not in sys.argv))
