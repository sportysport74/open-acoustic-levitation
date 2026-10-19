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
T2  FP64 trace recursion vs a 50-digit (mpmath) evaluation of the same chain built from
    the same FP64 cell matrices: |x_rec - x_ref| / max(1, |x_ref|) <= 1e-9, j = 2..18,
    at 4001 uniform frequencies plus dense samples around the stub pole and f_t.
    This isolates the recursion's own rounding. It does not cover the FP64 error of the
    cell matrices themselves (tan() near the stub pole), which any method inherits; that
    floor is reported alongside (vs a 50-digit evaluation of the cells too).
    History: as |x_rec - x_prod| < 1e-10 (absolute) it FAILED (4e292); as
    |x_rec - x_prod| / max(1, |x_prod|) <= 1e-9 it FAILED (3.0e-9 at 2584 cells). The
    50-digit reference showed that 3.0e-9 is the explicit FP64 matrix product's own
    rounding; the recursion's is ~20-50x smaller.
T3  I constant along j: |I_j - I_1| <= 1e-9 max(1, |I_1|) where |x| <= 10 for all three
    traces involved; and I > 0 on the whole grid (it vanishes only where the stubs are
    half a wavelength deep, Y = 0, f_t = c / (2 l_eff) = 19.004 kHz)
T4  approximant band width B_j agrees within 0.5% between two frequency grids
T5  6-cycle (0, 0, sqrt(I+1)) of the trace map: the linearization of Phi^6 has
    eigenvalues mu, 1, 1/mu with mu + 1/mu = 16 (1 + I)^2 + 2, relative error <= 1e-9,
    for I spanning the tube's I(f) range
"""
import sys
import mpmath
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fibonacci_tube import (wavenumbers, stub_admittance, Z, d, phi, c, rho, S_b, l_s, r_s,
                            fibonacci)

SG = d / (1 + phi ** -2)              # S gap of the infinite chain; L = phi * SG
F_T = c / (2 * (l_s + 0.85 * r_s))    # stubs half a wavelength deep: Y = 0, tube transparent
J_MAX = 18                            # w_18 has 4181 cells
J_RANDOM = 14                         # random control up to 610 cells (explicit products)
N_SHUFFLE, SEED = 10, 7
GRIDS = (245001, 980001)              # 0.1 Hz and 0.025 Hz over 0.5-25 kHz
GRIDS_RANDOM = (49001, 245001)        # 0.5 Hz and 0.1 Hz
F_STUB = c / (4 * (l_s + 0.85 * r_s)) # stub quarter-wave resonance (Y -> infinity), ~9.5 kHz
REF_FREQS = np.unique(np.concatenate([np.linspace(500, 25000, 4001),
                                      np.linspace(F_STUB - 200, F_STUB + 200, 401),
                                      np.linspace(F_T - 100, F_T + 100, 201)]))
BOX_EPS = (1.0, 50.0)                 # windowed box counting: fit range (Hz), >= 20 boxes per window


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


def mp_traces(F, MS, ML, jmax, exact_cells=False, dps=50):
    """Half-traces x_0..x_jmax at 50 digits via M_j = M_{j-1} M_{j-2}. The cells are the
    given FP64 matrices taken as exact inputs, or (exact_cells) the cell formula evaluated
    at 50 digits from the same FP64 constants."""
    mpmath.mp.dps = dps
    I = mpmath.mpc(0, 1)
    if exact_cells:
        cm, Zm, Sbm, rhom = (mpmath.mpf(v) for v in (c, Z, S_b, rho))
        leff, pim = mpmath.mpf(l_s + 0.85 * r_s), mpmath.mpf(np.pi)
    out = np.empty((jmax + 1, len(F)))
    for i, f in enumerate(F):
        if exact_cells:
            k = 2 * pim * mpmath.mpf(f) / cm
            Yn = Zm * I * Sbm / (rhom * cm) * mpmath.tan(k * leff)

            def cell(g):
                cs, sn = mpmath.cos(k * g), mpmath.sin(k * g)
                return mpmath.matrix([[cs + I * sn * Yn, I * sn], [I * sn + cs * Yn, cs]])
            M = [cell(mpmath.mpf(SG)), cell(mpmath.mpf(phi * SG))]
        else:
            M = [mpmath.matrix([[mpmath.mpc(X[0][i]), mpmath.mpc(X[1][i])],
                                [mpmath.mpc(X[2][i]), mpmath.mpc(X[3][i])]]) for X in (MS, ML)]
        for j in range(2, jmax + 1):
            M.append(M[j - 1] * M[j - 2])
        out[:, i] = [float(mpmath.re(m[0, 0] + m[1, 1]) / 2) for m in M]
    return out


def box_counts(mask, df, eps):
    """Grid-aligned box counts N(eps) of a set given as a boolean mask on a uniform grid."""
    out = []
    for e in eps:
        m = int(round(e / df)); nb = -(-len(mask) // m)
        pad = np.zeros(nb * m, bool); pad[:len(mask)] = mask
        out.append(pad.reshape(nb, m).any(1).sum())
    return np.array(out, float)


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

    print(f"\nT2  FP64 trace recursion vs 50-digit chain of the same FP64 cells ({len(REF_FREQS)} frequencies)")
    x = traces(MS, ML, J_MAX)
    rS, rL, _ = cells(REF_FREQS)
    xr = traces(rS, rL, J_MAX)
    ref = mp_traces(REF_FREQS, rS, rL, J_MAX)
    ref_x = mp_traces(REF_FREQS, rS, rL, J_MAX, exact_cells=True)
    def rel_err(a, b):
        """max |a - b| / max(1, |b|) where both are finite (deep in stop bands the traces
        overflow FP64); a NaN from finite inputs would make the result NaN and fail."""
        ok = np.isfinite(a) & np.isfinite(b)
        e = np.abs(a[ok] - b[ok]) / np.maximum(1, np.abs(b[ok]))
        return (np.max(e) if e.size else np.nan), np.mean(ok)
    e_rec = [rel_err(xr[j], ref[j]) for j in range(2, J_MAX + 1)]
    worst2 = max(e_rec, key=lambda t: t[0] if np.isfinite(t[0]) else np.inf)
    ok2 = all(np.isfinite(e) and e <= 1e-9 for e, _ in e_rec)
    results.append(check("|x_rec - x_ref| / max(1, |x_ref|) <= 1e-9", ok2,
                         f"max {worst2[0]:.1e} (at {length(2 + e_rec.index(worst2))} cells), j = 2..{J_MAX}; "
                         f"finite at {min(f for _, f in e_rec):.0%}-{max(f for _, f in e_rec):.0%} of frequencies"))
    show = (5, 8, 11, 14, 16, 17, 18)
    print("    recursion arithmetic, by length:   " + ", ".join(f"{length(j)}: {e_rec[j-2][0]:.1e}" for j in show))
    print("    (explicit FP64 product, same reference: " + ", ".join(
        f"{length(j)}: {rel_err(half_trace(product(word(j), rS, rL)), ref[j])[0]:.1e}" for j in show) + ")")
    away = np.abs(REF_FREQS - F_STUB) > 50
    print("    (floor any method inherits -- FP64 cells vs 50-digit cells, propagated; excluding +-50 Hz of the "
          "stub pole, where tan() is ill-conditioned: " + ", ".join(
              f"{length(j)}: {rel_err(ref[j][away], ref_x[j][away])[0]:.1e}" for j in show) + "; within it: "
          + f"{rel_err(ref[6][~away], ref_x[6][~away])[0]:.1e} already at {length(6)} cells)")

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
    Bf, masks = {}, {}
    for n in GRIDS:
        Fg = np.linspace(500, 25000, n)
        xs = traces(*cells(Fg)[:2], J_MAX)
        Bf[n] = [band_width(np.abs(xs[j]) <= 1, Fg) for j in range(J_MAX + 1)]
        masks[n] = {j: np.abs(xs[j]) <= 1 for j in (J_MAX - 1, J_MAX)}    # for windowed box counting
    dev4 = max(abs(Bf[GRIDS[0]][j] / Bf[GRIDS[1]][j] - 1) for j in range(1, J_MAX + 1))
    results.append(check("B_j within 0.5% between grids", dev4 <= 0.005,
                         f"max difference {dev4:.3%} (0.1 vs 0.025 Hz grid, up to {length(J_MAX)} cells)"))

    # ---- controls ----------------------------------------------------------------
    rng = np.random.default_rng(SEED)
    perms = [[rng.permutation(list(word(j))) for j in range(J_RANDOM + 1)] for _ in range(N_SHUFFLE)]
    Br, rmask = {}, {}
    for n in GRIDS_RANDOM:
        Fg = np.linspace(500, 25000, n)
        cS, cL, _ = cells(Fg)
        Br[n] = []
        for j in range(J_RANDOM + 1):
            ms = [np.abs(half_trace(product(p[j], cS, cL))) <= 1 for p in perms]
            Br[n].append(np.mean([band_width(mk, Fg) for mk in ms]))
            if j == J_RANDOM and n == GRIDS[0]:
                rmask[n] = ms                                   # 0.1 Hz, for box counting
    cS, cL, _ = cells(np.linspace(500, 25000, GRIDS[1]))       # 0.025 Hz, box counting only
    rmask[GRIDS[1]] = [np.abs(half_trace(product(p[J_RANDOM], cS, cL))) <= 1 for p in perms]
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
    print(f"\nLOCAL  1 kHz windows: band-width exponent alpha (B ~ F^-alpha, 34-4181 cells) and box-counting"
          f"\n       dimension D0 of the 4181-cell band set (eps = {BOX_EPS[0]:g}-{BOX_EPS[1]:g} Hz; converged = grids"
          f" and 2584 vs 4181 cells agree within 2%)")
    js = range(8, J_MAX + 1)
    eps_w = np.unique(np.round(np.geomspace(*BOX_EPS, 12), 1))
    loc = []
    for lo in range(1, 25, 2):
        w = (F >= lo * 1e3) & (F < (lo + 1) * 1e3)
        B = [np.count_nonzero(np.abs(x[j][w]) <= 1) for j in js]
        if min(B) == 0:
            print(f"   {lo:2d}-{lo+1:2d} kHz: pass band vanishes")
            continue
        a_loc = -np.polyfit(np.log([length(j) for j in js]), np.log(B), 1)[0]
        N = {}
        for n in GRIDS:
            Fg = np.linspace(500, 25000, n); wg = (Fg >= lo * 1e3) & (Fg < (lo + 1) * 1e3)
            for j in (J_MAX - 1, J_MAX):
                N[(n, j)] = box_counts(masks[n][j][wg], Fg[1] - Fg[0], eps_w)
        d0 = -np.polyfit(np.log(eps_w), np.log(N[(GRIDS[1], J_MAX)]), 1)[0]
        conv = max(np.max(np.abs(N[(GRIDS[0], J_MAX)] / N[(GRIDS[1], J_MAX)] - 1)),
                   np.max(np.abs(N[(GRIDS[1], J_MAX - 1)] / N[(GRIDS[1], J_MAX)] - 1)))
        loc.append((lo, np.median(I1[w]), a_loc, d0, conv <= 0.02))
        print(f"   {lo:2d}-{lo+1:2d} kHz: median I {loc[-1][1]:.1e}   alpha {a_loc:.4f}   D0 {d0:.4f}"
              f"   ({'converged' if conv <= 0.02 else 'NOT converged'}, max diff {conv:.1%})")
    lI, la = np.log([v[1] for v in loc]), np.log([v[2] for v in loc])
    (p_al, _), res = np.polyfit(lI, la, 1, full=True)[:2]
    ratio = np.array([v[2] for v in loc]) / np.sqrt([v[1] for v in loc])
    print(f"  alpha ~ I^{p_al:.3f} (rms residual in ln alpha {np.sqrt(res[0]/len(loc)):.3f}); "
          f"alpha / sqrt(I) = {ratio.min():.2f}-{ratio.max():.2f}")
    cv = [v for v in loc if v[4]]
    if len(cv) > 2:
        (p_d, _), res_d = np.polyfit(np.log([v[1] for v in cv]), np.log([1 - v[3] for v in cv]), 1, full=True)[:2]
        print(f"  converged windows: 1 - D0 ~ I^{p_d:.3f} (rms residual in ln(1 - D0) {np.sqrt(res_d[0]/len(cv)):.3f})")

    # ---- global box counting (Fibonacci vs controls) --------------------------------
    print("\nGLOBAL BOX COUNTING  over 0.5-25 kHz, fit eps = 1-100 Hz (converged = grids agree within 2%)")
    eps_g = np.unique(np.round(np.geomspace(0.1, 24500, 60), 1)); fit_g = (eps_g >= 1) & (eps_g <= 100)
    dfs = {n: 24500 / (n - 1) for n in GRIDS}
    def d0_g(Nf, Nc):
        return (-np.polyfit(np.log(eps_g[fit_g]), np.log(Nf[fit_g]), 1)[0],
                np.max(np.abs(Nc[fit_g] / Nf[fit_g] - 1)))
    fN = {n: box_counts(masks[n][J_MAX], dfs[n], eps_g) for n in GRIDS}
    pN = {n: box_counts(np.abs(half_trace(cells(np.linspace(500, 25000, n))[2])) <= 1, dfs[n], eps_g) for n in GRIDS}
    rN = {n: np.mean([box_counts(mk, dfs[n], eps_g) for mk in rmask[n]], 0) for n in GRIDS}
    jconv = np.max(np.abs(box_counts(masks[GRIDS[1]][J_MAX - 1], dfs[GRIDS[1]], eps_g)[fit_g] / fN[GRIDS[1]][fit_g] - 1))
    for name, NN, extra in ((f"Fibonacci {length(J_MAX)} cells", fN, f"; 2584 vs 4181 cells {jconv:.2%}"),
                            ("periodic", pN, ""), (f"random {length(J_RANDOM)} cells (mean of {N_SHUFFLE})", rN, "")):
        dv, gc = d0_g(NN[GRIDS[1]], NN[GRIDS[0]])
        print(f"  {name:28s} D0 = {dv:.4f}   grids differ by {gc:.2%}{extra}"
              f"   -> {'converged' if gc <= 0.02 else 'NOT converged'}")

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
    fig, (a, b, e, h) = plt.subplots(1, 4, figsize=(22, 4.6))
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
    for v in loc:
        e.annotate(f"{v[0]}-{v[0]+1}", (v[1], v[2]), textcoords="offset points", xytext=(4, -9), fontsize=7)
    g = np.geomspace(Iv.min(), Iv.max(), 20)
    e.loglog(g, np.sqrt(g) * np.median(av / np.sqrt(Iv)), "--", color="0.5", lw=0.9, label="∝ √I (guide)")
    e.set_xlabel("median KKT invariant I in the window"); e.set_ylabel("local exponent α")
    e.set_title("Local scaling exponent grows with I", fontsize=10); e.legend(fontsize=8)
    for v in loc:
        h.semilogx(v[1], v[3], "o", color="#b7791f", ms=5, mfc="#b7791f" if v[4] else "none")
        h.annotate(f"{v[0]}-{v[0]+1}", (v[1], v[3]), textcoords="offset points", xytext=(4, -9), fontsize=7)
    h.axhline(1, color="0.6", lw=0.8, ls="--")
    h.set_xlabel("median KKT invariant I in the window"); h.set_ylabel(f"box-counting D0 ({BOX_EPS[0]:g}-{BOX_EPS[1]:g} Hz)")
    h.set_title(f"Local dimension of the {length(J_MAX)}-cell band set (open: not converged)", fontsize=10)
    fig.tight_layout(); fig.savefig("fibonacci_trace_map.png", dpi=140)
    print("saved fibonacci_trace_map.png")


if __name__ == "__main__":
    sys.exit(main())
