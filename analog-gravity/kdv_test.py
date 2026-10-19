"""Coupled steepening + dispersion test (the other AI's suggested Step 2), extended:
compare the same 160 dB wave with and without dispersion, track the max gradient,
and count the pulses that form."""
import math, sys, torch
import numpy as np
from sonic_horizon_physical import PhysicalSolver, advance
from sonic_horizon import DEV, DT_
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

# exact escape wavenumber for the H test: v_g(k) = 1.4c, xi = 3e-4
s_ = 0.0; 
for _ in range(200):  # solve (1+2s)/sqrt(1+s) = 1.4 for s = (xi k)^2
    f = (1+2*s_)/math.sqrt(1+s_) - 1.4
    df = (2*math.sqrt(1+s_) - (1+2*s_)/(2*math.sqrt(1+s_)))/(1+s_)
    s_ -= f/df
print(f"escape wavenumber (exact): k* = {math.sqrt(s_)/3e-4:.0f}   "
      f"other AI's estimate sqrt(v^2-c^2)/xi = {math.sqrt(1.4**2-1)/3e-4:.0f}   "
      f"measured in H test at t=0.55: ~{150*12.0:.0f}")


def check(name, ok, detail):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return ok


results = []
print("\nK1  escape wavenumber: group velocity at k* must be 1.4c")
xi_h, k_star = 3e-4, math.sqrt(s_) / 3e-4
omega = lambda kk: kk * (1 + xi_h**2 * kk**2) ** 0.5   # omega(k), c = 1
vg = (omega(complex(k_star, 1e-20)).imag / 1e-20)       # complex-step derivative, exact to rounding
results.append(check("v_g(k*) = 1.4", abs(vg - 1.4) < 1e-9, f"v_g = {vg:.15f} (error {abs(vg-1.4):.1e})"))

def count_pulses(u, min_prom):
    """Peaks of a periodic signal whose topographic prominence exceeds min_prom.
    Grid-scale wiggles on a shock front are local maxima with tiny prominence,
    so they are not counted; a real pulse (e.g. a soliton) stands out by ~its amplitude."""
    n = len(u); count = 0
    for i in range(n):
        if not (u[i] > u[i - 1] and u[i] >= u[(i + 1) % n]):
            continue
        bases = []
        for step in (-1, 1):  # walk each way until a higher point; lowest point passed is the base
            j, lo = i, u[i]
            for _ in range(n - 1):
                j = (j + step) % n
                if u[j] > u[i]:
                    break
                lo = min(lo, u[j])
            bases.append(lo)
        if u[i] - max(bases) > min_prom:
            count += 1
    return count


N, L, c = 1024, 1.0, 1.0
x = torch.arange(N, device=DEV, dtype=DT_) / N
beta, eps, m = 1.2, 0.014, 20; k = 2*math.pi*m
ts = 1/(beta*eps*k)
res = {}
for xi in (0.0, 1e-3):
    s = PhysicalSolver(torch.zeros(N), L, c, xi=xi, beta=beta, nu=1e-5)
    psi = -(eps/k)*torch.cos(k*x); pi = -c*s.dx_(psi)
    mon = lambda p, q: s.dxx_(p).abs().max()
    psi, pi, fr, tm, hist = advance(s, psi, pi, 1.5*ts, record_every=50, monitor=mon)
    u = s.dx_(psi).cpu()
    peaks = count_pulses(u.tolist(), 0.3*eps) / m  # whole domain, per original wavelength
    g = [h[1] for h in hist]
    res[xi] = (u, hist, peaks)
    print(f"xi={xi:g}: max gradient {max(g)/(eps*k):.1f}x initial; "
          f"pulses per original wavelength at t=1.5 t_s: {peaks:g} (prominence > 0.3 u0)")

print("\nK2  no dispersion, inviscid: steepening must track Burgers (B1 method: gradient 5x at 0.8 t_s)")
# Separate run: the comparison runs above use nu = 1e-5, which is not inviscid
# Burgers (Gol'dberg number ~13; on that run this check fails, 0.4762 vs 0.3789).
N2 = 4096
x2 = torch.arange(N2, device=DEV, dtype=DT_) / N2
s = PhysicalSolver(torch.zeros(N2), L, c, beta=beta)
psi = -(eps/k)*torch.cos(k*x2); pi = -c*s.dx_(psi)
*_, hist0 = advance(s, psi, pi, 0.85*ts, monitor=lambda p, q: s.dxx_(p).abs().max())
t5 = next((t for t, gi in hist0 if gi > 5 * eps * k), float("nan"))
results.append(check("steepening time (gradient 5x)", abs(t5 / (0.8 * ts) - 1) < 0.05,
                     f"sim {t5:.4f} vs Burgers {0.8*ts:.4f} (N={N2}, nu=0)"))


def viscous_burgers(xi_pts, t, delta, nmax=200):
    """Exact solution of u_t + beta u u_x = delta u_xx, u(x,0) = eps sin(kx) (Cole-Hopf):
    u = -(2 delta/beta) phi_x/phi, phi = sum_n w_n cos(n k x) with
    w_n = (2 - [n=0]) I_n(R) e^{-R} e^{-delta (nk)^2 t}, R = beta eps / (2 delta k).
    I_n(R) e^{-R} = (1/pi) int_0^pi e^{R (cos th - 1)} cos(n th) dth (trapezoid, spectrally exact).
    Returns u at xi_pts and u_x at the shock centre x = pi/k, for each t (array)."""
    R = beta*eps/(2*delta*k)
    th = np.linspace(0, np.pi, 8193); n = np.arange(nmax)
    a = np.trapezoid(np.exp(R*(np.cos(th)[None, :] - 1))*np.cos(n[:, None]*th[None, :]), th, axis=1)/np.pi
    a[1:] *= 2
    w = a[None, :]*np.exp(-delta*(n*k)**2*np.atleast_1d(t)[:, None])
    sgn = (-1.0)**n                                   # cos(n pi)
    ux_c = (2*delta/beta)*((w*sgn*(n*k)**2).sum(1)/(w*sgn).sum(1))
    nk = np.outer(xi_pts, n*k)
    u = -(2*delta/beta)*((np.sin(nk)*(-(n*k))) @ w[-1])/(np.cos(nk) @ w[-1])
    return u, np.abs(ux_c)


print("\nK3  the nu = 1e-5 shock run vs the exact viscous Burgers solution (delta = nu/2, see V1)")
u_sim, hist_v, _ = res[0.0]
t_end = 1.5*ts
xs_ = x.cpu().numpy()
u_ex, _ = viscous_burgers((xs_ - c*t_end) % L, t_end, 0.5e-5)
rms = np.sqrt(np.mean((u_sim.numpy() - u_ex)**2))/eps
_, gex = viscous_burgers(xs_[:1], np.array([t for t, _ in hist_v]), 0.5e-5)
gsim = max(gi for _, gi in hist_v)
results.append(check("waveform at t = 1.5 t_s", rms < 0.01, f"rms error {rms:.2%} of u0"))
results.append(check("peak max gradient", abs(gsim/gex.max() - 1) < 0.02,
                     f"sim {gsim/(eps*k):.2f}x vs exact {gex.max()/(eps*k):.2f}x initial"))

fig, (a, b) = plt.subplots(1, 2, figsize=(12, 4.5))
for xi, col, lab in ((0.0, "#c05621", "no dispersion: shock"), (1e-3, "#2b6cb0", "with dispersion ξ=1e-3")):
    u, hist, _ = res[xi]
    a.plot(x.cpu()[:3*N//m]*m, u[:3*N//m]/eps, color=col, lw=1.4, label=lab)
    t, g = zip(*hist); b.plot([ti/ts for ti in t], [gi/(eps*k) for gi in g], color=col, label=lab)
a.set_xlabel("x / (original wavelength)"); a.set_ylabel("u / u₀"); a.set_title("Waveform at t = 1.5 × shock time"); a.legend(fontsize=8)
b.axvline(1, color="gray", ls="--", lw=0.8); b.text(1.02, 1.5, "Burgers\nshock time", fontsize=8)
b.set_xlabel("t / t_shock"); b.set_ylabel("max |∂u/∂x| / initial"); b.set_title("Steepening over time"); b.set_yscale("log"); b.legend(fontsize=8)
fig.tight_layout(); fig.savefig("shock_vs_dispersion.png", dpi=140); print("saved shock_vs_dispersion.png")
print("\nSUMMARY:", "ALL TESTS PASS" if all(results) else "SOME TESTS FAILED")
sys.exit(0 if all(results) else 1)
