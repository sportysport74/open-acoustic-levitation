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


def T_dB(freqs, gaps):
    out = []
    for f in freqs:
        k = 2 * np.pi * f / c * (1 - 1j * loss)
        Y = 1j * S_b / (rho * c) * np.tan(k * (l_s + 0.85 * r_s))
        shunt = np.array([[1, 0], [Y, 1]])
        M = np.eye(2, dtype=complex)
        for g in gaps:
            seg = np.array([[np.cos(k * g), 1j * Z * np.sin(k * g)],
                            [1j * np.sin(k * g) / Z, np.cos(k * g)]])
            M = M @ seg @ shunt
        A, B, C, D = M.ravel()
        out.append(20 * np.log10(abs(2 / (A + B / Z + C * Z + D))))
    return np.array(out)


def fibonacci(n):
    seq = "L"
    while len(seq) < n:
        seq = "".join("LS" if ch == "L" else "L" for ch in seq)
    return seq[:n]


N = 55  # a Fibonacci number of rings
seq = fibonacci(N)
nL = seq.count("L"); nS = N - nL
Sg = d * N / (nL * phi + nS)          # keep total length equal
fib_gaps = [phi * Sg if ch == "L" else Sg for ch in seq]
per_gaps = [d] * N

freqs = np.linspace(500, 25000, 4000)
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


MERGE_KHZ = 0.2   # pass-peaks narrower than this don't split a gap
THRESHOLDS = (-10, -20, -30)


def gaps_list(T, thr=-20, merge_khz=MERGE_KHZ):
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
