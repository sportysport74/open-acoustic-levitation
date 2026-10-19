"""Coupled steepening + dispersion test (the other AI's suggested Step 2), extended:
compare the same 160 dB wave with and without dispersion, track the max gradient,
and count the pulses that form."""
import math, torch
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

N, L, c = 1024, 1.0, 1.0
x = torch.arange(N, device=DEV, dtype=DT_) / N
beta, eps, m = 1.2, 0.014, 20; k = 2*math.pi*m
ts = 1/(beta*eps*k)
res = {}
for xi in (0.0, 1e-3):
    s = PhysicalSolver(torch.zeros(N), L, c, xi=xi, beta=beta, nu=1e-5)
    psi = -(eps/k)*torch.cos(k*x); pi = -c*s.dx_(psi)
    mon = lambda p, q: s.dx_(s.dx_(p)).abs().max().item()
    psi, pi, fr, tm, hist = advance(s, psi, pi, 1.5*ts, record_every=50, monitor=mon)
    u = s.dx_(psi).cpu()
    one = u[: N//m * 1]  # one original wavelength
    peaks = int(((one > torch.roll(one, 1)) & (one > torch.roll(one, -1)) & (one > 0.3*eps)).sum())
    g = [h[1] for h in hist]
    res[xi] = (u, hist, peaks)
    print(f"xi={xi:g}: max gradient {max(g)/(eps*k):.1f}x initial; "
          f"pulses per original wavelength at t=1.5 t_s: {peaks}")

fig, (a, b) = plt.subplots(1, 2, figsize=(12, 4.5))
for xi, col, lab in ((0.0, "#c05621", "no dispersion: shock"), (1e-3, "#2b6cb0", "with dispersion ξ=1e-3")):
    u, hist, _ = res[xi]
    a.plot(x.cpu()[:3*N//m]*m, u[:3*N//m]/eps, color=col, lw=1.4, label=lab)
    t, g = zip(*hist); b.plot([ti/ts for ti in t], [gi/(eps*k) for gi in g], color=col, label=lab)
a.set_xlabel("x / (original wavelength)"); a.set_ylabel("u / u₀"); a.set_title("Waveform at t = 1.5 × shock time"); a.legend(fontsize=8)
b.axvline(1, color="gray", ls="--", lw=0.8); b.text(1.02, 1.5, "Burgers\nshock time", fontsize=8)
b.set_xlabel("t / t_shock"); b.set_ylabel("max |∂u/∂x| / initial"); b.set_title("Steepening over time"); b.set_yscale("log"); b.legend(fontsize=8)
fig.tight_layout(); fig.savefig("shock_vs_dispersion.png", dpi=140); print("saved shock_vs_dispersion.png")
