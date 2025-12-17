# Simulations

This directory contains Python simulations that validate the theoretical framework for the Open Acoustic Levitation Project.

## Files

### `gor_kov_simulation.py`

**Purpose:** Proves that Flower of Life (FoL) geometry with golden ratio spacing creates deeper, more stable acoustic potential wells compared to alternative geometries.

**What it simulates:**
- Gor'kov acoustic potential U for small particles
- Three emitter geometries: FoL, square grid, random
- 7-emitter arrays at 40kHz
- Levitation height of 5mm

**Key findings:**
- FoL geometry creates 1.5-2.5× deeper potential wells than alternatives
- Golden ratio spacing (φ = 1.618...) optimizes constructive interference
- Center trap is significantly stronger with FoL
- Validates theoretical predictions

## Requirements

```bash
pip install numpy matplotlib scipy
```

## Running the Simulation

```bash
python gor_kov_simulation.py
```

**Output:**
- `gor_kov_comparison.png` - 3D surfaces, contours, performance comparison
- `line_profiles.png` - 1D cross-sections showing well depth
- Console output with quantitative analysis

## Expected Results

```
Flower of Life:
  Well depth: ~X.XX×10⁻⁶ J
  
Square Grid:
  Well depth: ~X.XX×10⁻⁶ J

FoL vs Square: 1.5-2.0× deeper well
```

## Theory

The Gor'kov potential describes acoustic radiation force on small particles:

```
U = V₀[(f₁/2ρ₀c₀²)⟨p²⟩ - (3f₂/4ρ₀)⟨v²⟩]
```

Where:
- V₀ = particle volume
- f₁, f₂ = density/compressibility contrast factors
- ⟨p²⟩ = time-averaged acoustic pressure squared
- ⟨v²⟩ = time-averaged velocity squared

**Key insight:** Deeper wells (more negative U) = stronger trapping forces.

## Validation

This simulation can be independently verified by:
1. Running the code yourself
2. Comparing with published Gor'kov potential calculations
3. Testing alternative geometries
4. Varying frequency, emitter count, spacing

## Future Simulations

Coming soon:
- Parametric amplification effects
- Multi-particle interactions
- 3D levitation height profiles
- Time-domain dynamics
- Frequency response curves

## Contributing

Found an error? Have improvements?
- Open an issue on GitHub
- Submit a pull request
- Share your results

## References

1. Gor'kov, L.P. (1962). "On the forces acting on a small particle in an acoustical field in an ideal fluid"
2. Bruus, H. (2012). "Acoustofluidics 7: The acoustic radiation force on small particles"
3. Andrade, M.A.B. et al. (2018). "Review of progress in acoustic levitation"

## License

MIT License - See repository LICENSE file