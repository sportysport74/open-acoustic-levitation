#!/usr/bin/env python3
"""
Kohmoto-Kadanoff-Tang trace map for the Fibonacci stub tube: is it a critical quasicrystal?

Each cell of fibonacci_tube.py's model (a duct segment, then a ring of stubs) has a
lossless 2x2 transfer matrix with det = 1. With S = d / (1 + phi^-2) and L = phi S
(the infinite chain's gaps, mean spacing d), the Fibonacci words w0 = S, w1 = L,
w_{j+1} = w_j w_{j-1} (= the substitution L -> LS, S -> L of fibonacci_tube.py) give
    M_{j+1} = M_j M_{j-1}    and, for x_j = Tr(M_j) / 2,
    x_{j+1} = 2 x_j x_{j-1} - x_{j-2}                        (KKT trace map)
with the invariant
    I = x_{j+1}^2 + x_j^2 + x_{j-1}^2 - 2 x_{j+1} x_j x_{j-1} - 1,
the same for every j at a given frequency. The periodic approximant built from block
w_j passes frequencies with |x_j| <= 1; their total width B_j is tracked vs the block
length F_j and compared with two controls: the same L/S counts in random order, and
periodic d-spacing.

Matrices act on the dimensionless state (p, Z0 U), Z0 = rho c / S: M' = S^-1 M S with
S = diag(1, 1/Z0), i.e. [[A, B/Z0], [C Z0, D]]. Traces and determinants are unchanged;
the SI form (p, U) put Z0 ~ 7.5e5 into the entries.

CHECKS
T1  det(M'_j) = 1 within 1e-12, j = 1..6, at frequencies where all entries |M'_j| <= 10.
    In stop bands products grow as exp(gamma N) (to ~1e70 at 13 cells), and FP64 cannot
    evaluate AD - BC = 1 there without cancellation; those frequencies are excluded
    and the excluded fraction is reported. (First run, SI units, whole range: FAIL,
    1.6e119.)
T2  trace recursion vs explicit products: |x_rec - x_prod| / max(1, |x_prod|) <= 1e-9
    wherever the explicit product is finite. (First run, absolute < 1e-10: FAIL.)
T3  I constant along j: |I_j - I_1| <= 1e-9 max(1, |I_1|) where |x| <= 10 for all three
    traces involved; and I > 0 on the whole grid (it vanishes only where the stubs are
    half a wavelength deep, Y = 0, f_t = c / (2 l_eff) = 19.004 kHz)
T4  approximant band width B_j agrees within 0.5% between two frequency grids
T5  6-cycle (0, 0, sqrt(I+1)) of the trace map: the linearization of Phi^6 has
    eigenvalues mu, 1, 1/mu with mu + 1/mu = 16 (1 + I)^2 + 2, relative error <= 1e-9,
    for I spanning the tube's I(f) range
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fibonacci_tube import wavenumbers, stub_admittance, Z, d, phi, c, l_s, r_s, fibonacci

SG = d / (1 + phi ** -2)              # S gap of the infinite chain; L = phi * SG
F_T = c / (2 * (l_s + 0.85 * r_s))    # stubs half a wavelength deep: Y = 0, tube transparent
J_MAX = 18                            # w_18 has 4181 cells
J_RANDOM = 14                         # random control up to 610 cells (explicit products)
N_SHUFFLE, SEED = 10, 7
GRIDS = (245001, 980001)              # 0.1 Hz and 0.025 Hz over 0.5-25 kHz
GRIDS_RANDOM = (49001, 245001)        # 0.5 Hz and 0.1 Hz


def length(j):
    a, b = 1, 1
    for _ in range(j):
        a, b = b, a + b
    return a                          # |w_j|: 1, 1, 2, 3, 5, ...


def word(j):
    w = ["S", "L"]
    while len(w) <= j:
        w.append(w[-1] + w[-2])
    return w[j]


def cells(F):
    """Normalized cell matrices [A, B, C, D] on (p, Z0 U) (segment, then ring of stubs)
    for S, L and periodic d. Yn = Z0 Y = i (S_b / S) tan(k l_eff) is dimensionless."""
    k, ks = wavenumbers(F, (0.0, 0.0))
    Yn = Z * stub_admittance(ks)

    def cell(g):
        cs, sn = np.cos(k * g), np.sin(k * g)
        return np.array([cs + 1j * sn * Yn, 1j * sn, 1j * sn + cs * Yn, cs])
    return cell(SG), cell(phi * SG), cell(d)


def mul(P, Q):
    return np.array([P[0] * Q[0] + P[1] * Q[2], P[0] * Q[1] + P[1] * Q[3],
                     P[2] * Q[0] + P[3] * Q[2], P[2] * Q[1] + P[3] * Q[3]])


def half_trace(M):
    return 0.5 * (M[0] + M[3]).real


def product(letters, MS, ML):
    M = np.array([np.ones(MS.shape[1]), np.zeros(MS.shape[1]), np.zeros(MS.shape[1]),
                  np.ones(MS.shape[1])], dtype=complex)
    for ch in letters:
        M = mul(M, ML if ch == "L" else MS)
    return M


def traces(MS, ML, jmax):
    x = [half_trace(MS), half_trace(ML), half_trace(mul(ML, MS))]
    for j in range(3, jmax + 1):
        x.append(2 * x[j - 1] * x[j - 2] - x[j - 3])
    return x


def invariant(x, j):
    return x[j + 1] ** 2 + x[j] ** 2 + x[j - 1] ** 2 - 2 * x[j + 1] * x[j] * x[j - 1] - 1


def band_width(mask, F):
    return np.count_nonzero(mask) * (F[1] - F[0]) / 1e3      # kHz


def check(name, ok, detail):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return ok


def fit(n, B):
    n, B = np.asarray(n, float), np.asarray(B, float)
    out = {}
    for name, X in (("power", np.log(n)), ("exp", n)):
        p, res = np.polyfit(X, np.log(B), 1, full=True)[:2]
        out[name] = (p[0], np.sqrt(res[0] / len(n)) if len(res) else 0.0)
    return out


def main():
    results = []
    np.seterr(all="ignore")           # overflow in stop bands is expected; checks mask it
    assert word(11) == fibonacci(144), "w_11 must be fibonacci_tube's 144-ring sequence"
    F = np.linspace(500, 25000, GRIDS[0])
    MS, ML, MD = cells(F)
    print(f"cells: S = {SG*1e3:.4f} mm, L = phi S = {phi*SG*1e3:.4f} mm (mean spacing d = {d*1e3:.2f} mm); "
          f"grid {len(F)} points over 0.5-25 kHz")

    print("\nT1  det(M'_j) = 1, j = 1..6, where all entries |M'_j| <= 10")
    dev, cover = 0.0, []
    for j in range(1, 7):
        M = product(word(j), MS, ML)
        ok = np.max(np.abs(M), axis=0) <= 10
        dev = max(dev, np.max(np.abs(M[0] * M[3] - M[1] * M[2] - 1)[ok]))
        cover.append(np.mean(ok))
    results.append(check("|det - 1| < 1e-12", dev < 1e-12,
                         f"max deviation {dev:.1e}; entries <= 10 at {min(cover):.0%}-{max(cover):.0%} of frequencies"))

    print("\nT2  trace recursion vs explicit products (relative)")
    x = traces(MS, ML, J_MAX)
    errs, jlast = [], 0
    for j in range(2, J_MAX + 1):
        xp = half_trace(product(word(j), MS, ML))
        ok = np.isfinite(xp) & np.isfinite(x[j])
        if ok.any():
            errs.append((j, np.max(np.abs(x[j][ok] - xp[ok]) / np.maximum(1, np.abs(xp[ok]))), np.mean(ok)))
            jlast = j
    worst = max(errs, key=lambda e: e[1])
    results.append(check("|x_rec - x_prod| / max(1, |x_prod|) <= 1e-9", worst[1] <= 1e-9,
                         f"max {worst[1]:.1e} (at {length(worst[0])} cells); compared up to {length(jlast)} cells, "
                         f"finite at {errs[-1][2]:.0%} of frequencies there"))
    print("    by length: " + ", ".join(f"{length(j)}: {e:.1e}" for j, e, _ in errs if j in (5, 8, 11, 14, 16, 18)))

    print("\nT3  KKT invariant")
    I1 = invariant(x, 1)
    worst_rel = 0.0
    for j in range(2, J_MAX):
        ok = (np.abs(x[j + 1]) <= 10) & (np.abs(x[j]) <= 10) & (np.abs(x[j - 1]) <= 10)
        if ok.any():
            worst_rel = max(worst_rel, np.max(np.abs(invariant(x, j)[ok] - I1[ok]) / np.maximum(1, np.abs(I1[ok]))))
    results.append(check("I constant along j", worst_rel <= 1e-9, f"max relative change {worst_rel:.1e}"))
    i0 = np.argmin(I1)
    results.append(check("I > 0 over 0.5-25 kHz", np.all(I1 > 0),
                         f"min {I1[i0]:.1e} at {F[i0]/1e3:.4f} kHz (transparency point f_t = {F_T/1e3:.4f} kHz); "
                         f"max {I1.max():.1e}"))

    print("\nT4  approximant band width, grid convergence (Fibonacci)")
    Bf = {}
    for n in GRIDS:
        Fg = np.linspace(500, 25000, n)
        xs = traces(*cells(Fg)[:2], J_MAX)
        Bf[n] = [band_width(np.abs(xs[j]) <= 1, Fg) for j in range(J_MAX + 1)]
    dev4 = max(abs(Bf[GRIDS[0]][j] / Bf[GRIDS[1]][j] - 1) for j in range(1, J_MAX + 1))
    results.append(check("B_j within 0.5% between grids", dev4 <= 0.005,
                         f"max difference {dev4:.3%} (0.1 vs 0.025 Hz grid, up to {length(J_MAX)} cells)"))

    # ---- controls ----------------------------------------------------------------
    rng = np.random.default_rng(SEED)
    perms = [[rng.permutation(list(word(j))) for j in range(J_RANDOM + 1)] for _ in range(N_SHUFFLE)]
    Br = {}
    for n in GRIDS_RANDOM:
        Fg = np.linspace(500, 25000, n)
        cS, cL, _ = cells(Fg)
        Br[n] = [np.mean([band_width(np.abs(half_trace(product(p[j], cS, cL))) <= 1, Fg) for p in perms])
                 for j in range(J_RANDOM + 1)]
    devr = max(abs(Br[GRIDS_RANDOM[0]][j] / Br[GRIDS_RANDOM[1]][j] - 1) for j in range(5, J_RANDOM + 1))
    Bp = band_width(np.abs(half_trace(MD)) <= 1, F)

    print(f"\nSCALING  total pass-band width B of periodic approximants vs block length"
          f" (random control grid agreement {devr:.2%})")
    print("   cells | Fibonacci    | random (mean of 10) | periodic")
    for j in range(5, J_MAX + 1):
        r = f"{Br[GRIDS_RANDOM[1]][j]:9.3f} kHz" if j <= J_RANDOM else "      -      "
        print(f"   {length(j):5d} | {Bf[GRIDS[1]][j]:7.3f} kHz  |   {r}     | {Bp:.3f} kHz")
    jf, jr = range(5, J_MAX + 1), range(5, J_RANDOM + 1)
    ff = fit([length(j) for j in jf], [Bf[GRIDS[1]][j] for j in jf])
    fr = fit([length(j) for j in jr], [Br[GRIDS_RANDOM[1]][j] for j in jr])
    alpha = -ff["power"][0]
    for name, fx, rng_ in (("Fibonacci", ff, f"{length(5)}-{length(J_MAX)}"), ("random", fr, f"{length(5)}-{length(J_RANDOM)}")):
        print(f"  {name:9s} ({rng_} cells): power law B ~ F^{fx['power'][0]:+.4f} (rms residual in ln B "
              f"{fx['power'][1]:.3f}); exponential B ~ exp({fx['exp'][0]:+.2e} F) (rms residual {fx['exp'][1]:.3f})")
    print(f"  periodic: B = {Bp:.3f} kHz at every length")
    print(f"  Fibonacci alpha = {alpha:.4f} (aggregate over 0.5-25 kHz): B shrinks by phi^-alpha = "
          f"{phi**-alpha:.4f} per generation ({1 - phi**-alpha:.1%})")

    # ---- local exponent vs I ----------------------------------------------------------
    print("\nLOCAL EXPONENT  B ~ F^-alpha in 1 kHz windows (34-4181 cells) vs the window's median I")
    js = range(8, J_MAX + 1)
    loc = []
    for lo in range(1, 25, 2):
        w = (F >= lo * 1e3) & (F < (lo + 1) * 1e3)
        B = [np.count_nonzero(np.abs(x[j][w]) <= 1) for j in js]
        if min(B) == 0:
            print(f"   {lo:2d}-{lo+1:2d} kHz: pass band vanishes")
            continue
        a_loc = -np.polyfit(np.log([length(j) for j in js]), np.log(B), 1)[0]
        loc.append((lo, np.median(I1[w]), a_loc))
        print(f"   {lo:2d}-{lo+1:2d} kHz: median I {loc[-1][1]:.1e}   alpha {a_loc:.4f}")
    lI, la = np.log([v[1] for v in loc]), np.log([v[2] for v in loc])
    (p_al, _), res = np.polyfit(lI, la, 1, full=True)[:2]
    ratio = np.array([v[2] for v in loc]) / np.sqrt([v[1] for v in loc])
    print(f"  alpha ~ I^{p_al:.3f} (rms residual in ln alpha {np.sqrt(res[0]/len(loc)):.3f}); "
          f"alpha / sqrt(I) = {ratio.min():.2f}-{ratio.max():.2f}")

    print("\nT5  6-cycle linearization: mu + 1/mu = 16 (1 + I)^2 + 2")
    worst5 = 0.0
    for Iv in np.geomspace(max(I1.min(), 1e-12), I1.max(), 25):
        v = np.array([0.0, 0.0, np.sqrt(Iv + 1)]); J = np.eye(3)
        for _ in range(6):
            J = np.array([[0, 1, 0], [0, 0, 1], [-1, 2 * v[2], 2 * v[1]]]) @ J
            v = np.array([v[1], v[2], 2 * v[1] * v[2] - v[0]])
        mu = np.max(np.abs(np.linalg.eigvals(J)))
        worst5 = max(worst5, abs((mu + 1 / mu) / (16 * (1 + Iv) ** 2 + 2) - 1))
    results.append(check("relation holds", worst5 <= 1e-9,
                         f"max relative error {worst5:.1e} over 25 values of I in [{max(I1.min(), 1e-12):.0e}, {I1.max():.0e}]"))

    plot(F, I1, Bf[GRIDS[1]], Br[GRIDS_RANDOM[1]], Bp, ff, loc)
    print("\nSUMMARY:", "ALL TESTS PASS" if all(results) else "SOME TESTS FAILED")
    return 0 if all(results) else 1


def plot(F, I1, Bf, Br, Bp, ff, loc):
    fig, (a, b, e) = plt.subplots(1, 3, figsize=(17, 4.6))
    a.semilogy(F / 1e3, I1, color="#b7791f", lw=1)
    a.axvline(F_T / 1e3, color="0.5", ls="--", lw=0.8)
    a.text(F_T / 1e3 + 0.2, I1.max() / 30, f"stubs half a wavelength\n(Y = 0, I = 0) {F_T/1e3:.4f} kHz", fontsize=8)
    a.set_xlabel("frequency (kHz)"); a.set_ylabel("KKT invariant I(f)")
    a.set_title("KKT invariant: I(f) > 0 except where the stubs are transparent", fontsize=10)
    nf = [length(j) for j in range(5, J_MAX + 1)]; nr = [length(j) for j in range(5, J_RANDOM + 1)]
    b.loglog(nf, [Bf[j] for j in range(5, J_MAX + 1)], "o-", color="#b7791f", ms=4,
             label=f"Fibonacci: B ~ F^{ff['power'][0]:.3f}")
    b.loglog(nr, [Br[j] for j in range(5, J_RANDOM + 1)], "s-", color="#4a5568", ms=4,
             label="same L/S counts, random order (mean of 10)")
    b.loglog([nf[0], nf[-1]], [Bp, Bp], "-", color="#2b6cb0", label="periodic")
    b.set_xlabel("block length F (cells)"); b.set_ylabel("total pass-band width B (kHz)")
    b.set_title("Pass-band width of periodic approximants", fontsize=10); b.legend(fontsize=8, loc="lower left")
    Iv, av = np.array([v[1] for v in loc]), np.array([v[2] for v in loc])
    e.loglog(Iv, av, "o", color="#b7791f", ms=5, label="1 kHz windows (34-4181 cells)")
    for (lo, Ii, ai) in loc:
        e.annotate(f"{lo}-{lo+1}", (Ii, ai), textcoords="offset points", xytext=(4, -9), fontsize=7)
    g = np.geomspace(Iv.min(), Iv.max(), 20)
    e.loglog(g, np.sqrt(g) * np.median(av / np.sqrt(Iv)), "--", color="0.5", lw=0.9, label="∝ √I (guide)")
    e.set_xlabel("median KKT invariant I in the window"); e.set_ylabel("local exponent α")
    e.set_title("Local scaling exponent grows with I", fontsize=10); e.legend(fontsize=8)
    fig.tight_layout(); fig.savefig("fibonacci_trace_map.png", dpi=140)
    print("saved fibonacci_trace_map.png")


if __name__ == "__main__":
    sys.exit(main())
