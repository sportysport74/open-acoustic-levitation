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

if __name__ == "__main__":
    for f in (40e3, 10e3, 5e3, 2e3):
        show(design(f))
