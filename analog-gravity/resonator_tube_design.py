#!/usr/bin/env python3
"""
Feasibility + geometry for a Sugimoto-style resonator-loaded tube (shock vs no shock A/B).

Design logic
------------
* Baseline tube must actually SHOCK: Gol'dberg number  G = 1/(alpha * x_s) > ~3,
  where x_s = shock distance and alpha = wall boundary-layer attenuation.
* Plane-wave tube: the axisymmetric (0,1) mode cutoff 3.832 c/(2 pi a) must sit above
  the 3rd harmonic so harmonics stay 1-D (a plane source can't excite asymmetric modes).
* Side resonators tuned so the 2nd harmonic falls in their band gap
  f_res < 2f < f_res*sqrt(1+kappa) (approximate): the energy a shock needs can't propagate.
  Lumped Helmholtz cavities turn out too small to tune this high at sub-wavelength
  spacing, so we use quarter-wave side stubs (closed tubes, depth ~ lambda_res/4).
  kappa = stub volume per unit tube volume. Ring spacing d = lambda/8.
"""
import math
import sys
import numpy as np

c, rho, nu, gam, Pr, beta = 343.0, 1.204, 1.5e-5, 1.4, 0.71, 1.2


def spl_to_eps(spl):  # acoustic Mach number u/c of a plane wave
    p = 20e-6 * 10 ** (spl / 20)
    return p / (rho * c * c)


def design(f, n_harm=3, res_ratio=1.9):
    lam = c / f; w = 2 * math.pi * f
    a = 0.95 * 3.832 * c / (2 * math.pi * n_harm * f)       # tube radius
    A = math.pi * a * a
    # boundary-layer attenuation (Kirchhoff), Np/m, at the fundamental
    alpha = math.sqrt(w * nu / 2) * (1 + (gam - 1) / math.sqrt(Pr)) / (a * c)
    rows = []
    for spl in (145, 150, 155, 160):
        eps = spl_to_eps(spl)
        xs = 1 / (beta * eps * w / c)
        rows.append((spl, xs, 1 / (alpha * xs)))
    # Quarter-wave side stubs (closed tubes branching off the duct), n per ring.
    d = lam / 8                                   # ring spacing
    f_res = res_ratio * f                         # stub resonance
    r_s = 0.15 * 2 * a                            # stub radius
    l_s = c / (4 * f_res) - 0.85 * r_s            # stub depth incl. end correction
    n_ring = max(1, int((2 * math.pi * a) // (2 * r_s * 1.6)))
    V = n_ring * math.pi * r_s ** 2 * l_s
    kap = V / (A * d)
    return dict(f=f, lam=lam, a=a, alpha=alpha, rows=rows, d=d, f_res=f_res,
                r_s=r_s, l_s=l_s, n=n_ring, kappa=kap,
                gap=(f_res, f_res * math.sqrt(1 + kap)))


def show(D):
    mm = 1e3
    print(f"\n=== fundamental {D['f']/1e3:g} kHz  (wavelength {D['lam']*mm:.1f} mm) ===")
    print(f" tube inner diameter      {2*D['a']*mm:7.2f} mm   (plane-wave through 3rd harmonic)")
    print(f" wall loss                {D['alpha']:7.3f} Np/m  (1/e length {1/D['alpha']:.2f} m)")
    print("   SPL in tube   shock distance   Gol'dberg G   shocks?")
    for spl, xs, G in D['rows']:
        print(f"   {spl} dB       {xs:8.2f} m        {G:6.2f}       {'yes' if G > 3 else 'marginal' if G > 1 else 'NO'}")
    print(f" resonator tuning         {D['f_res']/1e3:.1f} kHz; band gap {D['gap'][0]/1e3:.1f}-{D['gap'][1]/1e3:.1f} kHz"
          f" (2nd harmonic {2*D['f']/1e3:g} kHz {'inside' if D['gap'][0] < 2*D['f'] < D['gap'][1] else 'OUTSIDE'})")
    print(f" ring spacing d           {D['d']*mm:7.2f} mm")
    print(f" stubs per ring           {D['n']:7d}     radius {D['r_s']*mm:.2f} mm, depth {D['l_s']*mm:.2f} mm")
    print(f" coupling kappa           {D['kappa']:7.2f}")

def check(name, ok, detail):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return ok


def j1_first_zero():
    """First zero of the Bessel function J1 (the (0,1) duct mode, J0' = -J1), from
    J1(x) = (1/pi) int_0^pi cos(t - x sin t) dt and bisection; independent of 3.832."""
    t = np.linspace(0, np.pi, 4001)
    j1 = lambda x: np.trapezoid(np.cos(t - x * np.sin(t)), t) / np.pi
    lo, hi = 3.5, 4.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if j1(lo) * j1(mid) > 0 else (lo, mid)
    return 0.5 * (lo + hi)


def validate():
    """Hand-checkable values (derivations in the comments) against the calculator."""
    print("\nCHECKS (expected values worked by hand)")
    r = []
    D40, D5 = design(40e3), design(5e3)
    # shock distance in wavelengths: x_s / lambda = 1 / (2 pi beta eps) = rho c^2 / (2 pi beta p0)
    #   160 dB: p0 = 2000 Pa  ->  141649.4 / (2 pi * 1.2 * 2000) = 9.393
    # (9.47, printed by sonic_horizon_physical.py, uses the rounded eps = 0.014, i.e. 159.9 dB;
    #  this check expected 9.47 on its first run and failed)
    xs_lam = D40['rows'][3][1] / D40['lam']
    r.append(check("shock distance, 160 dB at 40 kHz", abs(xs_lam - 9.393) < 0.005,
                   f"{xs_lam:.3f} wavelengths (hand: 9.393)"))
    # (0,1) mode cutoff 3.832 c / (2 pi a): 3.832 is the first zero of J1
    z = j1_first_zero()
    r.append(check("(0,1) cutoff constant", abs(3.832 / z - 1) < 1e-4, f"3.832 vs J1 zero {z:.6f}"))
    # design sets a = 0.95 * 3.832 c / (2 pi 3f)  =>  cutoff = 3f / 0.95 = 15.789 kHz at 5 kHz
    fc = 3.832 * c / (2 * math.pi * D5['a'])
    r.append(check("(0,1) cutoff of the 5 kHz tube", abs(fc - 15789.47) < 0.01 and fc > 15e3,
                   f"{fc/1e3:.5f} kHz (hand: 15/0.95 = 15.78947 kHz, above 3f)"))
    # ID = 0.95 * 3.832 * 343 / (pi * 15000) = 1248.657 / 47123.89 m = 26.497 mm
    r.append(check("5 kHz tube inner diameter", abs(2 * D5['a'] * 1e3 - 26.50) < 0.01,
                   f"{2*D5['a']*1e3:.3f} mm (hand: 26.50 mm)"))
    # wall loss: sqrt(pi 5000 * 1.5e-5) * (1 + 0.4/sqrt(0.71)) / (a c)
    #          = 0.485406 * 1.474713 / (0.0132487 * 343) = 0.15752 Np/m
    r.append(check("5 kHz wall loss", abs(D5['alpha'] - 0.1575) < 0.0005,
                   f"{D5['alpha']:.5f} Np/m (hand: 0.1575)"))
    # 155 dB: p0 = 1124.68 Pa, eps = p0 / (1.204 * 343^2) = 0.0079399,
    # x_s = 343 / (1.2 * 0.0079399 * 2 pi 5000) = 1.1459 m, G = 1 / (0.15752 * 1.1459) = 5.540
    _, xs155, G155 = D5['rows'][2]
    r.append(check("5 kHz shock distance at 155 dB", abs(xs155 - 1.146) < 0.001, f"{xs155:.4f} m (hand: 1.146 m)"))
    r.append(check("5 kHz Gol'dberg number at 155 dB", abs(G155 - 5.540) < 0.01, f"{G155:.3f} (hand: 5.540)"))
    # stub depth: 343 / (4 * 9500) - 0.85 * 0.3 * a = 9.0263 - 3.3784 = 5.648 mm
    r.append(check("5 kHz stub depth", abs(D5['l_s'] * 1e3 - 5.648) < 0.005, f"{D5['l_s']*1e3:.4f} mm (hand: 5.648 mm)"))
    for f in (40e3, 10e3, 5e3, 2e3):
        D = design(f)
        r.append(check(f"{f/1e3:g} kHz: 2nd harmonic inside the band gap", D['gap'][0] < 2 * f < D['gap'][1],
                       f"{D['gap'][0]/1e3:.2f} < {2*f/1e3:g} < {D['gap'][1]/1e3:.2f} kHz"))
    print("\nSUMMARY:", "ALL TESTS PASS" if all(r) else "SOME TESTS FAILED")
    return all(r)


if __name__ == "__main__":
    for f in (40e3, 10e3, 5e3, 2e3):
        show(design(f))
    sys.exit(0 if validate() else 1)
