#!/usr/bin/env python3
"""
Golden-ratio acoustic quasicrystal: periodic vs Fibonacci-spaced resonator rings.

1-D transfer-matrix model of a duct (5 kHz design: 26.5 mm ID, 6 quarter-wave
stubs per ring). Rings are placed either
  * periodically (every d), or
  * as a Fibonacci quasicrystal: gaps L and S with L/S = phi, ordered by the
    substitution L -> LS, S -> L (same average spacing d).
Plots sound transmission vs frequency for both.
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

c, rho = 343.0, 1.204
phi = (1 + 5 ** 0.5) / 2
a = 13.25e-3; S = np.pi * a ** 2; Z = rho * c / S
r_s, l_s, n_s = 3.97e-3, 5.65e-3, 6
S_b = n_s * np.pi * r_s ** 2
d = 8.57e-3
loss = 3e-3  # small damping so resonances stay finite


def wavenumbers(freqs, alpha=None):
    """Complex duct and stub wavenumbers. alpha=None: the small proportional damping
    above. alpha=(duct, stub) in Np/m: frequency-independent attenuation instead
    (the loss model of tube_shock.py); alpha=(0, 0) is lossless."""
    f = np.asarray(freqs, dtype=float)
    if alpha is None:
        k = 2 * np.pi * f / c * (1 - 1j * loss)
        return k, k
    return 2 * np.pi * f / c - 1j * alpha[0], 2 * np.pi * f / c - 1j * alpha[1]


def stub_admittance(ks):
    return 1j * S_b / (rho * c) * np.tan(ks * (l_s + 0.85 * r_s))


def transfer(freqs, gaps, alpha=None):
    """Complex pressure transmission and reflection coefficients (T, R) through a
    ring after each gap, anechoic both ends; vectorized over frequency."""
    k, ks = wavenumbers(freqs, alpha)
    Y = stub_admittance(ks)
    A, B, C, D = (np.ones_like(k), np.zeros_like(k), np.zeros_like(k), np.ones_like(k))
    log2s = np.zeros(k.shape)        # M is carried as 2**log2s * [[A, B], [C, D]]
    for g in gaps:
        cs, sn = np.cos(k * g), np.sin(k * g)
        # M <- M @ [[cs, iZ sn], [i sn / Z, cs]] @ [[1, 0], [Y, 1]]
        a2, b2 = A * cs + B * (1j * sn / Z), A * (1j * Z * sn) + B * cs
        c2, d2 = C * cs + D * (1j * sn / Z), C * (1j * Z * sn) + D * cs
        A, B, C, D = a2 + b2 * Y, b2, c2 + d2 * Y, d2
        # lossless runs near a stub resonance overflow after a few dozen rings; rescale by
        # exact powers of two (results that never get this large are bit-for-bit unchanged)
        big = np.maximum.reduce([np.abs(A), np.abs(B), np.abs(C), np.abs(D)]) > 2.0 ** 256
        if big.any():
            A[big], B[big], C[big], D[big] = (x[big] * 2.0 ** -256 for x in (A, B, C, D))
            log2s[big] += 256
    den = A + B / Z + C * Z + D
    return 2 / den * np.exp2(-log2s), (A + B / Z - C * Z - D) / den


def T_dB(freqs, gaps, alpha=None):
    """Transmission (dB) through a ring after each gap, anechoic both ends."""
    return 20 * np.log10(np.abs(transfer(freqs, gaps, alpha)[0]))


def fibonacci(n):
    seq = "L"
    while len(seq) < n:
        seq = "".join("LS" if ch == "L" else "L" for ch in seq)
    return seq[:n]


def layouts(N):
    """Periodic and Fibonacci gap lists for N rings, same total length."""
    seq = fibonacci(N)
    nL = seq.count("L"); nS = N - nL
    Sg = d * N / (nL * phi + nS)          # keep total length equal
    return [d] * N, [phi * Sg if ch == "L" else Sg for ch in seq], Sg


freqs = np.linspace(500, 25000, 4000)
MERGE_KHZ = 0.2   # pass-peaks narrower than this don't split a gap
THRESHOLDS = (-10, -20, -30)


def gaps_list(T, thr=-20, merge_khz=MERGE_KHZ, freqs=freqs):
    """Blocked bands (T < thr) in kHz, as (lo, hi, touches_sweep_edge).
    Bands separated by a pass-peak narrower than merge_khz are merged."""
    blocked = T < thr; bands = []; i = 0
    while i < len(T):
        if blocked[i]:
            j = i
            while j < len(T) and blocked[j]:
                j += 1
            lo, hi = freqs[i] / 1e3, freqs[j - 1] / 1e3
            edge = i == 0 or j == len(T)
            if bands and lo - bands[-1][1] < merge_khz:
                plo, _, pedge = bands.pop()
                lo, edge = plo, edge or pedge
            bands.append((lo, hi, edge)); i = j
        else:
            i += 1
    return bands


def fmt_dB(x):
    return "< -100 dB" if x < -100 else f"{x:6.1f} dB"


def check(name, ok, detail):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return ok


def bloch_rhs(f):
    """cos(q d) of the infinite periodic lattice (lossless):
    cos(k d) + (i Z Y / 2) sin(k d). |RHS| > 1 means a band gap."""
    k, ks = wavenumbers(f, (0.0, 0.0))
    return (np.cos(k * d) + 0.5j * Z * stub_admittance(ks) * np.sin(k * d)).real


def intervals(mask, f):
    """[lo, hi] (kHz) of runs where mask is True."""
    edges = np.flatnonzero(np.diff(np.concatenate(([0], mask.astype(int), [0]))))
    return [(f[i] / 1e3, f[j - 1] / 1e3) for i, j in zip(edges[::2], edges[1::2])]


def validate(N=55):
    print(f"\nCHECKS ({N} rings)")
    results = []
    per_gaps, fib_gaps, _ = layouts(N)
    # E1: a lossless two-port conserves energy
    for name, gaps in (("periodic", per_gaps), ("fibonacci", fib_gaps)):
        T, R = transfer(freqs, gaps, alpha=(0.0, 0.0))
        err = np.max(np.abs(np.abs(T) ** 2 + np.abs(R) ** 2 - 1))
        results.append(check(f"lossless {name}: |R|^2 + |T|^2 = 1", err < 1e-9, f"max deviation {err:.1e}"))
    # B1: periodic gaps vs the Bloch condition of the infinite lattice
    fb = np.linspace(500, 25000, 245001)                       # 0.1 Hz grid
    rhs = bloch_rhs(fb)
    bloch = intervals(np.abs(rhs) > 1, fb)
    depth = [N * 8.686 * np.arccosh(np.abs(rhs[(fb >= lo * 1e3) & (fb <= hi * 1e3)]).max()) for lo, hi in bloch]
    Tl = T_dB(fb, per_gaps, alpha=(0.0, 0.0))
    finite = [(lo, hi) for lo, hi, ed in gaps_list(Tl, freqs=fb) if not ed]
    for (lo, hi), dep in zip(bloch, depth):
        if dep < 20:
            print(f"    Bloch gap {lo:.3f}-{hi:.3f} kHz: max attenuation {dep:.1f} dB in {N} cells, "
                  f"too shallow to reach -20 dB (finite tube min {Tl[(fb >= lo*1e3) & (fb <= hi*1e3)].min():.1f} dB)")
            continue
        match = [(x, y) for x, y in finite if x <= hi and y >= lo]
        err = max(abs(match[0][0] - lo), abs(match[0][1] - hi)) if len(match) == 1 else float("inf")
        results.append(check(f"Bloch gap {lo:.3f}-{hi:.3f} kHz", err < 0.15,
                             f"finite lossless tube blocks " + (f"{match[0][0]:.3f}-{match[0][1]:.3f} kHz, "
                             f"edges within {err*1e3:.0f} Hz" if len(match) == 1 else f"{len(match)} matching bands")))
    stray = [(x, y) for x, y in finite if not any(x <= hi and y >= lo for lo, hi in bloch)]
    results.append(check("no blocked band outside a Bloch gap", not stray,
                         ", ".join(f"{x:.2f}-{y:.2f}" for x, y in stray) or "none"))
    print("\nSUMMARY:", "ALL TESTS PASS" if all(results) else "SOME TESTS FAILED")
    return all(results)


def main(N=55):  # a Fibonacci number of rings
    per_gaps, fib_gaps, Sg = layouts(N)
    Tp, Tf = T_dB(freqs, per_gaps), T_dB(freqs, fib_gaps)

    fig, ax = plt.subplots(2, 1, figsize=(11, 6.5), sharex=True)
    for a_, T, lab, col in ((ax[0], Tp, f"Periodic: {N} rings every {d*1e3:.2f} mm", "#2b6cb0"),
                            (ax[1], Tf, f"Fibonacci quasicrystal: gaps {phi*Sg*1e3:.2f} / {Sg*1e3:.2f} mm (ratio φ)", "#b7791f")):
        a_.plot(freqs / 1e3, T, color=col, lw=1)
        a_.set_ylim(-80, 3); a_.set_ylabel("transmission (dB)"); a_.set_title(lab, fontsize=10)
        for h, nm in ((5, "f"), (10, "2f"), (15, "3f")):
            a_.axvline(h, color="gray", ls="--", lw=0.7); a_.text(h + 0.15, -75, nm, fontsize=8)
    ax[1].set_xlabel("frequency (kHz)")
    fig.suptitle(f"Same tube, same {N} resonator rings, same length ({sum(per_gaps)*100:.1f} cm) — only the spacing differs")
    fig.tight_layout()
    fig.savefig("fibonacci_tube.png", dpi=140)

    print(f"blocked = transmission below threshold; gaps split by pass-peaks < {MERGE_KHZ} kHz wide are merged;\n"
          f"bands touching the {freqs[0]/1e3:g}-{freqs[-1]/1e3:g} kHz sweep edge are listed but not counted")
    for name, T in (("periodic", Tp), ("fibonacci", Tf)):
        b = gaps_list(T)
        inner = [(x, y) for x, y, e in b if not e]
        edge = [(x, y) for x, y, e in b if e]
        print(f"{name:9s}: {len(inner)} gaps (< -20 dB): " +
              (", ".join(f"{x:.1f}-{y:.1f}" for x, y in inner) or "none") + " kHz" +
              ("   [edge, not counted: " + ", ".join(f"{x:.1f}-{y:.1f}" for x, y in edge) + " kHz]" if edge else ""))
        for h in (5, 10, 15):
            print(f"           at {h} kHz: {fmt_dB(np.interp(h*1e3, freqs, T))}")
    print("gap count vs threshold: " + "".join(f"{t:>8d} dB" for t in THRESHOLDS))
    for name, T in (("periodic", Tp), ("fibonacci", Tf)):
        print(f"  {name:21s}" + "".join(f"{sum(not e for *_, e in gaps_list(T, t)):11d}" for t in THRESHOLDS))
    print("saved fibonacci_tube.png")
    return 0 if validate(N) else 1


if __name__ == "__main__":
    sys.exit(main())
