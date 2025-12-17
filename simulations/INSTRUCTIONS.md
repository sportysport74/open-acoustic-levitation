# Running the Simulations - Quick Start Guide

## Prerequisites

**Python 3.7 or higher required.**

Check your version:
```bash
python --version
```

## Installation

### Option 1: Using pip (Recommended)

```bash
# Install required packages
pip install numpy matplotlib scipy

# Or use requirements file
pip install -r requirements.txt
```

### Option 2: Using conda

```bash
conda install numpy matplotlib scipy
```

### Option 3: Virtual Environment (Best Practice)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install packages
pip install numpy matplotlib scipy
```

## Running the Simulation

### Step 1: Navigate to simulations directory

```bash
cd simulations
```

### Step 2: Run the script

```bash
python gor_kov_simulation.py
```

### Step 3: View results

Output files will be created in the same directory:
- `gor_kov_comparison.png` - Main comparison visualization
- `line_profiles.png` - Detailed cross-sections

Console will show quantitative analysis.

## Expected Output

```
======================================================================
ACOUSTIC LEVITATION SIMULATION
Comparing Emitter Geometries
======================================================================

Physical Parameters:
  Frequency: 40.0 kHz
  Wavelength: 8.575 mm
  Golden Ratio φ: 1.618034
  Particle: Ping pong ball (13.5 mm radius)

Setting up simulation grid...
Calculating Gor'kov potentials...
  - Flower of Life geometry...
  - Square grid geometry...
  - Random geometry...
  - Done!

======================================================================
RESULTS ANALYSIS
======================================================================

Flower of Life:
  Minimum potential: -X.XXe-06 J
  Maximum potential: X.XXe-06 J
  Well depth: X.XXe-06 J
  Center trap: -X.XXe-06 J
  Relative performance: XX.X%

Square Grid:
  [Similar output]

Random:
  [Similar output]

======================================================================
COMPARISON
======================================================================
FoL vs Square: 1.XX× deeper well
FoL vs Random: 2.XX× deeper well

✓ Flower of Life geometry is OPTIMAL
======================================================================

Generating visualizations...
✓ Saved: gor_kov_comparison.png
✓ Saved: line_profiles.png

Simulation complete!
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'numpy'"

**Solution:** Install numpy
```bash
pip install numpy
```

### "Python is not recognized..."

**Solution:** Python not in PATH
- Windows: Reinstall Python, check "Add to PATH"
- Mac: Install via Homebrew: `brew install python`
- Linux: `sudo apt install python3 python3-pip`

### Plots not showing

The script automatically saves to files. If you want interactive plots:

Edit `gor_kov_simulation.py`, add at end:
```python
plt.show()  # Add before script ends
```

### Simulation runs slow

This is normal - calculating 100×100 grid for 3 geometries takes 30-60 seconds.

For faster results, reduce grid resolution in the script:
```python
# Change line ~140 from:
x_range = np.linspace(-0.04, 0.04, 100)
# To:
x_range = np.linspace(-0.04, 0.04, 50)
```

## Customization

### Change frequency

Edit line ~21:
```python
CARRIER_FREQ = 30000  # Try 30 kHz instead of 40 kHz
```

### Change emitter count

Modify geometry functions starting at line ~42.
Example for 19-emitter FoL:
```python
def flower_of_life_positions():
    # Add two more rings...
```

### Change particle

Edit lines ~24-26:
```python
PARTICLE_RADIUS = 0.01  # 10mm radius
PARTICLE_DENSITY = 500  # Styrofoam
```

### Export data

Add to end of script:
```python
np.save('potential_fol.npy', U_fol)
np.save('potential_square.npy', U_square)
```

## Next Steps

After validating FoL superiority:
1. Try different frequencies (20-60 kHz range)
2. Test different emitter counts (7, 19, 37...)
3. Vary golden ratio spacing (×0.8 to ×1.2 of φ)
4. Compare with your physical build results!

## Questions?

- Open issue on GitHub
- Check documentation in `docs/`
- Ask in community Discord

## Contributing

Want to improve the simulation?
- Add parametric modulation effects
- Include reflector plate model
- Time-domain dynamics
- Multi-particle simulation

Submit pull requests!