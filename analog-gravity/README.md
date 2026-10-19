# Analog Gravity & Nonlinear Acoustics Lab

Sound in moving air obeys the same wave equation as a field in curved spacetime
(Unruh, 1981). This folder simulates that "acoustic metric," adds the effects a
real medium has (dispersion, shock steepening, viscosity), and turns the results
into bench experiments.

**Rule for everything here: every simulation checks itself against a known
answer before its results are trusted.** Run any script and it prints PASS/FAIL.

Runs on CPU; uses CUDA automatically if PyTorch sees a GPU.

> Performance note: at these grid sizes (N ≤ 4096, float64) the GPU is no faster
> than the CPU. ~87% of GPU time is 4096-point FP64 cuFFT (~38 µs each): one small
> FFT can't fill the GPU, and consumer GPUs run FP64 at 1/64 rate. Removing
> GPU→CPU syncs from the time loops didn't change run times (`sonic_horizon.py`
> ~100 s either way, RTX 5090).

```bash
pip install torch numpy matplotlib
python sonic_horizon.py            # phase 1: ideal acoustic metric
python sonic_horizon_physical.py   # phase 2: dispersion, shocks, viscosity
python kdv_test.py                 # shock vs dispersion
python resonator_tube_design.py    # bench-build feasibility numbers
python fibonacci_tube.py           # golden-ratio quasicrystal tube
```

---

## 1. Sonic horizon on the Unruh metric — `sonic_horizon.py`

Solves (1/√−g) ∂μ(√−g g^μν ∂ν ψ) = 0 on
ds² = (ρ/c)[−(c² − v²)dt² − 2v dt dx + dx²], with a flow that crosses the speed
of sound twice (a black-hole and a white-hole horizon). Pseudo-spectral + RK4.

| Test | Result |
|---|---|
| Still air: packet speed = c | 1.0000 |
| Moving air: speeds = v ± c | 0.5000 / −1.5000 |
| Conserved energy | drift ~10⁻¹⁴ |
| Packet position & wavenumber vs ray theory | agree within 0.4% |
| Packet never crosses the white-hole horizon | ✓, blueshifted 20× |

![](results/sonic_horizon_result.png)

## 2. Real-medium effects — `sonic_horizon_physical.py`

| Effect | Test | Result |
|---|---|---|
| Dispersion ω² = c²k² + ξ²k⁴ | phase speed vs formula | match to 5 decimals |
| Viscosity | decay rate νk²/2 | match within 0.03% |
| Nonlinear steepening | shock time vs Burgers t_s = 1/(βεkc) | 0.3790 vs 0.3789 |

**Bug found and fixed:** the originally proposed nonlinear term (`v_eff = v + β ψ_x`)
steepened shocks exactly 2× too fast, because v_eff appears in two advection
terms. The correct coefficient is β/2. The Burgers test caught it.

**Horizon result:** in the ideal metric the wave piles up at the white hole (1%
gets through). With dispersion, the squeezed wave turns into fast short ripples
that escape — essentially 100% through by t = 0.9. Exact escape wavenumber
(solve v_g = 1.4c): k* = 1,817; measured ≈ 1,800.

![](results/sonic_horizon_dispersion.png)

## 3. Shock vs dispersion — `kdv_test.py`

At 160 dB in air (acoustic Mach ≈ 0.014) a 40 kHz wave shocks after ~9.5
wavelengths ≈ **8 cm** — the practical ceiling on acoustic levitation. With
strong model dispersion (ξ = 10⁻³) the shock never forms (gradient plateaus at
1.4×), but no soliton train appears at that setting either (1 pulse per original
wavelength in both runs, counting only peaks with prominence > 0.3 u₀ so
grid-scale wiggles on the shock front aren't mistaken for pulses).
Real air's dispersion length (~70 nm) is far too small to help at 40 kHz.

![](results/shock_vs_dispersion.png)

## 4. Bench build feasibility — `resonator_tube_design.py`

A tube lined with side resonators tuned so the 2nd harmonic falls in their band
gap should stop a shock from forming (Sugimoto-style). The calculator sizes it
at 40, 10, 5 and 2 kHz and checks the shock actually forms in the plain tube
(Gol'dberg number).

- **5 kHz:** 26.5 mm ID (1" Sch 40 PVC), shock in 1.15 m at 155 dB, 6 quarter-wave
  stubs per ring, rings every 8.6 mm. Straightforward.
- **40 kHz:** the hard version. Levers to make it work: wider tube with a plane
  source, pressurized gas (lower viscous loss), horn-coupled hex array for
  ~160 dB, resin-printed or corrugated (Bragg) wall, schlieren imaging to see
  the shocks directly.

## 5. Golden-ratio quasicrystal — `fibonacci_tube.py`

Same 55 rings, same length; only the spacing changes. Periodic spacing gives
one clean band gap (8.1–11.2 kHz at −20 dB). Fibonacci spacing (gap ratio φ,
substitution L→LS, S→L) widens the main gap to 7.3–12.0 kHz and adds side gaps,
but how many depends on where you draw the line. Counting gaps (blocked bands
split only by pass-peaks wider than 0.2 kHz, ignoring bands that touch the
0.5–25 kHz sweep edge):

| Threshold | Periodic | Fibonacci |
|---|---|---|
| −10 dB | 2 | 4 |
| −20 dB | 1 | 3 (7.3–12.0, 13.6–14.5, 23.2–23.5 kHz) |
| −30 dB | 1 | 4 (main gap splits into 7.3–7.8, 8.1–11.3, 11.5–12.0; plus 13.6–14.4) |

The robust features at every threshold are the widened main gap and the
13.6–14.5 kHz side gap; the rest come and go with the threshold. Whether this
55-ring tube shows the self-similar, Cantor-like gap structure of a true
quasicrystal needs a finer analysis (more rings, gap widths vs. generation).
Open question: does it suppress shock formation differently from the periodic tube?

![](results/fibonacci_tube.png)

---

## References
- W. G. Unruh, "Experimental black-hole evaporation?", PRL 46, 1351 (1981)
- M. Visser, "Acoustic black holes", CQG 15, 1767 (1998)
- S. Weinfurtner et al., "Measurement of stimulated Hawking emission in an analogue system", PRL 106, 021302 (2011)
- N. Sugimoto, "Propagation of nonlinear acoustic waves in a tunnel with an array of Helmholtz resonators", JFM 244, 55 (1992)
- M. F. Hamilton & D. T. Blackstock (eds.), *Nonlinear Acoustics*

*Built Oct 18, 2026 — Sportysport74 & Claude (Anthropic). Same license as the rest of this repo.*
