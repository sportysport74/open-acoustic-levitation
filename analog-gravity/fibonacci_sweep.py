#!/usr/bin/env python3
"""
Is the Fibonacci tube's gap structure a quasicrystal effect? Generation sweep + control.

For N = 13, 21, 34, 55, 89, 144 rings (successive Fibonacci numbers; same average
spacing d, gap ratio L/S = phi), track every transmission gap's centre and width
at -10/-20/-30 dB, using the transfer-matrix model of fibonacci_tube.py, LOSSLESS
so that only the structure creates gaps (with damping, longer tubes would grow
"gaps" just from accumulated loss).

Quasicrystal prediction, generation to generation:
  * existing gaps persist at stable positions
  * new gaps open between them
  * total passband width shrinks

CONTROL: the same numbers of L and S gaps in random order (N_SHUFFLE shuffles per
generation, fixed seed). If random layouts show the same pattern, it does not come
from the Fibonacci order.

Gaps follow fibonacci_tube.py's rules: a gap is a band below the threshold; pass-
peaks narrower than 0.2 kHz don't split a gap; bands touching the 0.5-25 kHz sweep
edge are not counted. A gap at generation n "persists" if its centre lies inside a
gap at generation n+1; a gap at n+1 is "new" if it overlaps no gap of generation n.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fibonacci_tube import transfer, layouts, gaps_list, THRESHOLDS

GENS = (13, 21, 34, 55, 89, 144)
FREQS = np.linspace(500, 25000, 49001)           # 0.5 Hz grid
N_SHUFFLE, SEED = 10, 2026


def tdb(gaps):
    with np.errstate(divide="ignore"):           # exact zeros at the lossless stub resonance
        return 20 * np.log10(np.abs(transfer(FREQS, gaps, alpha=(0.0, 0.0))[0]))


def analyse(T, thr):
    """Counted gaps (lo, hi) in kHz and total passband width (kHz above thr)."""
    gaps = [(lo, hi) for lo, hi, edge in gaps_list(T, thr, freqs=FREQS) if not edge]
    passband = np.count_nonzero(T >= thr) * (FREQS[1] - FREQS[0]) / 1e3
    return gaps, passband


def persistence(prev, cur):
    """(persisted, of, new): gaps of prev whose centre lies inside a gap of cur,
    and gaps of cur that overlap no gap of prev."""
    kept = sum(any(lo <= 0.5 * (a + b) <= hi for lo, hi in cur) for a, b in prev)
    new = sum(not any(lo <= b and hi >= a for a, b in prev) for lo, hi in cur)
    return kept, len(prev), new


def main():
    rng = np.random.default_rng(SEED)
    fib = {N: layouts(N)[1] for N in GENS}
    rnd = {N: [list(rng.permutation(fib[N])) for _ in range(N_SHUFFLE)] for N in GENS}
    Tf = {N: tdb(fib[N]) for N in GENS}
    Tr = {N: [tdb(g) for g in rnd[N]] for N in GENS}
    res = {}
    for thr in THRESHOLDS:
        print(f"\n=== threshold {thr} dB ===")
        print("  rings | Fibonacci: gaps  passband  persisted  new | random (mean of "
              f"{N_SHUFFLE}): gaps  passband  persisted  new")
        fg = [analyse(Tf[N], thr) for N in GENS]
        rg = [[analyse(T, thr) for T in Tr[N]] for N in GENS]
        res[thr] = (fg, rg)
        for i, N in enumerate(GENS):
            gaps, pb = fg[i]
            if i:
                k, of, new = persistence(fg[i - 1][0], gaps)
                fper = f"{k:3d}/{of:<3d} {new:4d}"
                rk = [persistence(rg[i - 1][j][0], rg[i][j][0]) for j in range(N_SHUFFLE)]
                rper = (f"{sum(x[0] for x in rk)/max(1, sum(x[1] for x in rk)):6.0%}   "
                        f"{np.mean([x[2] for x in rk]):4.1f}")
            else:
                fper, rper = "   -       -", "     -      -"
            rcount = np.mean([len(g) for g, _ in rg[i]]); rsd = np.std([len(g) for g, _ in rg[i]])
            rpb = np.mean([p for _, p in rg[i]])
            print(f"  {N:5d} |           {len(gaps):3d}  {pb:6.2f} kHz  {fper} |"
                  f"            {rcount:4.1f}+-{rsd:3.1f}  {rpb:6.2f} kHz  {rper}")
        print("  Fibonacci gaps, centre (width) in kHz:")
        for i, N in enumerate(GENS):
            print(f"    {N:3d}: " + ", ".join(f"{0.5*(lo+hi):.2f} ({hi-lo:.2f})" for lo, hi in fg[i][0]))
    plot(res)


def plot(res):
    fig, ax = plt.subplots(len(THRESHOLDS), 2, figsize=(13, 9), sharex=True, sharey=True)
    for r, thr in enumerate(THRESHOLDS):
        fg, rg = res[thr]
        for i, N in enumerate(GENS):
            for lo, hi in fg[i][0]:
                ax[r, 0].plot([lo, hi], [i, i], color="#b7791f", lw=6, solid_capstyle="butt")
            for j in range(N_SHUFFLE):
                y = i - 0.35 + 0.7 * j / (N_SHUFFLE - 1)
                for lo, hi in rg[i][j][0]:
                    ax[r, 1].plot([lo, hi], [y, y], color="#4a5568", lw=1.6, solid_capstyle="butt")
        for cidx, title in ((0, "Fibonacci order"), (1, f"same L/S counts, random order ({N_SHUFFLE} shuffles)")):
            a_ = ax[r, cidx]
            a_.set_yticks(range(len(GENS))); a_.set_yticklabels([str(n) for n in GENS])
            a_.set_ylim(-0.7, len(GENS) - 0.3); a_.grid(axis="x", color="0.92")
            a_.set_title(f"{title}: gaps below {thr} dB", fontsize=10)
        ax[r, 0].set_ylabel("rings (generation)")
    for a_ in ax[-1]:
        a_.set_xlabel("frequency (kHz)")
    fig.suptitle("Gap positions vs generation, lossless transfer matrices (0.5–25 kHz)")
    fig.tight_layout(); fig.savefig("fibonacci_sweep.png", dpi=140)
    print("\nsaved fibonacci_sweep.png")


if __name__ == "__main__":
    main()
