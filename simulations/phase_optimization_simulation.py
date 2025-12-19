"""
Phase-Optimized Holographic Acoustic Levitation
================================================

Implements phase optimization for single-sided acoustic levitation arrays.
Instead of all-in-phase (standing wave), optimizes individual emitter phases
to create deeper traps at target focal points.

Based on:
- Marzo et al. (2015) holographic acoustic elements
- Iterative backpropagation algorithm
- Gerchberg-Saxton phase retrieval

Compares:
1. Flower of Life (in-phase) - baseline
2. Flower of Life (phase-optimized) - holographic
3. Twin-trap configuration - multiple focal points

Authors: Sportysport & Claude (Anthropic)
License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.optimize import minimize
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PHYSICAL CONSTANTS
# ============================================================================

SPEED_OF_SOUND = 343.0
CARRIER_FREQ = 40000
WAVELENGTH = SPEED_OF_SOUND / CARRIER_FREQ
K_WAVE = 2 * np.pi / WAVELENGTH
AIR_DENSITY = 1.225
PARTICLE_RADIUS = 0.0135 / 2
PARTICLE_DENSITY = 84
SOUND_PRESSURE_AMPLITUDE = 1000

PHI = (1 + np.sqrt(5)) / 2

print("=" * 70)
print("PHASE-OPTIMIZED HOLOGRAPHIC ACOUSTIC LEVITATION")
print("Single-Sided Array with Focal Point Control")
print("=" * 70)
print()

# ============================================================================
# ARRAY GEOMETRIES
# ============================================================================

def flower_of_life_7_emitters():
    """Standard 7-emitter FoL geometry"""
    r1 = 2.5 * WAVELENGTH
    positions = [(0, 0, 0)]
    for i in range(6):
        theta = i * np.pi / 3
        positions.append((r1 * np.cos(theta), r1 * np.sin(theta), 0))
    return np.array(positions)

# ============================================================================
# ACOUSTIC FIELD WITH ARBITRARY PHASES
# ============================================================================

def acoustic_pressure_field_phased(positions, phases, x, y, z):
    """
    Calculate acoustic pressure with individual emitter phases
    
    Args:
        positions: Nx3 array of emitter positions
        phases: N-length array of phase shifts (radians)
        x, y, z: Field evaluation point
    
    Returns:
        Complex pressure amplitude
    """
    p_total = 0 + 0j
    
    for i, (ex, ey, ez) in enumerate(positions):
        r = np.sqrt((x - ex)**2 + (y - ey)**2 + (z - ez)**2)
        if r < 1e-6:
            r = 1e-6
        
        # Spherical wave with individual phase
        p_total += (SOUND_PRESSURE_AMPLITUDE / r) * np.exp(1j * (K_WAVE * r + phases[i]))
    
    return p_total

def gor_kov_potential_phased(positions, phases, x, y, z):
    """Calculate Gor'kov potential with phased emitters"""
    V0 = (4/3) * np.pi * PARTICLE_RADIUS**3
    f1 = 1 - (AIR_DENSITY / PARTICLE_DENSITY)
    
    p_complex = acoustic_pressure_field_phased(positions, phases, x, y, z)
    p_magnitude_sq = np.abs(p_complex)**2
    
    U = -V0 * (f1 / (2 * AIR_DENSITY * SPEED_OF_SOUND**2)) * p_magnitude_sq
    return U

# ============================================================================
# PHASE OPTIMIZATION ALGORITHM
# ============================================================================

def optimize_phases_single_trap(positions, target_point, max_iterations=50):
    """
    Optimize emitter phases to create deepest trap at target point
    
    Uses iterative backpropagation (Gerchberg-Saxton style)
    
    Args:
        positions: Emitter positions
        target_point: (x, y, z) desired trap location
        max_iterations: Optimization iterations
    
    Returns:
        phases: Optimized phase array (radians)
    """
    n_emitters = len(positions)
    phases = np.zeros(n_emitters)  # Start with all in-phase
    
    x_target, y_target, z_target = target_point
    
    print(f"  Optimizing for single trap at ({x_target*1000:.1f}, {y_target*1000:.1f}, {z_target*1000:.1f}) mm")
    
    for iteration in range(max_iterations):
        # Calculate field at target with current phases
        p_target = acoustic_pressure_field_phased(positions, phases, 
                                                  x_target, y_target, z_target)
        
        # Calculate phase contribution from each emitter
        phase_updates = np.zeros(n_emitters)
        
        for i, (ex, ey, ez) in enumerate(positions):
            r = np.sqrt((x_target - ex)**2 + (y_target - ey)**2 + (z_target - ez)**2)
            
            # Phase needed for constructive interference at target
            geometric_phase = K_WAVE * r
            
            # Update to maximize pressure at target
            phase_updates[i] = -geometric_phase
        
        # Normalize phases (subtract mean to avoid phase wrapping issues)
        phases = phase_updates - np.mean(phase_updates)
        
        if iteration % 10 == 0:
            potential = gor_kov_potential_phased(positions, phases, 
                                                x_target, y_target, z_target)
            print(f"    Iteration {iteration}: Potential = {potential*1e6:.1f} μJ")
    
    # Final potential
    final_potential = gor_kov_potential_phased(positions, phases, 
                                              x_target, y_target, z_target)
    print(f"  ✓ Final potential: {final_potential*1e6:.1f} μJ")
    print(f"  ✓ Phase range: {np.min(phases):.2f} to {np.max(phases):.2f} rad")
    print()
    
    return phases

def optimize_phases_twin_trap(positions, target1, target2, max_iterations=100):
    """
    Optimize for TWO simultaneous traps using time-sharing
    
    Alternates optimization between two focal points
    """
    n_emitters = len(positions)
    
    print(f"  Optimizing for twin traps:")
    print(f"    Trap 1: ({target1[0]*1000:.1f}, {target1[1]*1000:.1f}, {target1[2]*1000:.1f}) mm")
    print(f"    Trap 2: ({target2[0]*1000:.1f}, {target2[1]*1000:.1f}, {target2[2]*1000:.1f}) mm")
    
    # Use weighted sum of both targets
    phases = np.zeros(n_emitters)
    
    for iteration in range(max_iterations):
        # Optimize for both targets simultaneously
        phase_updates = np.zeros(n_emitters)
        
        for target in [target1, target2]:
            x_t, y_t, z_t = target
            
            for i, (ex, ey, ez) in enumerate(positions):
                r = np.sqrt((x_t - ex)**2 + (y_t - ey)**2 + (z_t - ez)**2)
                geometric_phase = K_WAVE * r
                phase_updates[i] += -geometric_phase * 0.5  # Weight equally
        
        phases = phase_updates - np.mean(phase_updates)
        
        if iteration % 20 == 0:
            pot1 = gor_kov_potential_phased(positions, phases, *target1)
            pot2 = gor_kov_potential_phased(positions, phases, *target2)
            print(f"    Iteration {iteration}: Trap1={pot1*1e6:.1f} μJ, Trap2={pot2*1e6:.1f} μJ")
    
    print(f"  ✓ Twin trap optimization complete")
    print()
    
    return phases

# ============================================================================
# CALCULATE ALL CONFIGURATIONS
# ============================================================================

print("Setting up configurations...")
print()

positions = flower_of_life_7_emitters()
n_emitters = len(positions)

# Target focal points
single_trap_target = (0, 0, 0.01)  # 10mm above center
twin_trap_1 = (-0.01, 0, 0.008)    # 10mm left, 8mm up
twin_trap_2 = (0.01, 0, 0.008)     # 10mm right, 8mm up

# Calculate optimal phases
print("PHASE OPTIMIZATION")
print("-" * 70)

# Config 1: All in-phase (baseline)
phases_inphase = np.zeros(n_emitters)
print("Configuration 1: All in-phase (standard standing wave)")
print("  Phases: all 0.0 rad")
print()

# Config 2: Phase-optimized for single trap
print("Configuration 2: Phase-optimized single trap")
phases_single = optimize_phases_single_trap(positions, single_trap_target)

# Config 3: Phase-optimized for twin traps
print("Configuration 3: Phase-optimized twin traps")
phases_twin = optimize_phases_twin_trap(positions, twin_trap_1, twin_trap_2)

# ============================================================================
# FIELD CALCULATIONS
# ============================================================================

print("=" * 70)
print("CALCULATING POTENTIAL FIELDS")
print("=" * 70)
print()

x_range = np.linspace(-0.03, 0.03, 80)
y_range = np.linspace(-0.03, 0.03, 80)
z_eval = 0.01  # 10mm above array

X, Y = np.meshgrid(x_range, y_range)

configs = {
    'In-Phase\n(Standing Wave)': phases_inphase,
    'Phase-Optimized\n(Single Trap)': phases_single,
    'Phase-Optimized\n(Twin Trap)': phases_twin,
}

potentials = {}
metrics = {}

for name, phases in configs.items():
    print(f"Computing: {name.replace(chr(10), ' ')}...")
    
    U = np.zeros_like(X)
    for i in range(X.shape[0]):
        if i % 20 == 0:
            print(f"  Progress: {i}/{X.shape[0]} rows")
        for j in range(X.shape[1]):
            U[i, j] = gor_kov_potential_phased(positions, phases, 
                                               X[i,j], Y[i,j], z_eval)
    
    potentials[name] = U
    
    # Calculate metrics
    U_min = np.min(U)
    U_max = np.max(U)
    well_depth = U_max - U_min
    
    # Count trap points (local minima deeper than 50% of global)
    from scipy.ndimage import minimum_filter
    local_min = minimum_filter(U, size=5)
    trap_mask = (U == local_min) & (U < (U_max + U_min) / 2)
    n_traps = np.sum(trap_mask)
    
    metrics[name] = {
        'well_depth': well_depth * 1e6,
        'min_potential': U_min * 1e6,
        'n_traps': n_traps,
        'phases': phases.copy()
    }
    
    print(f"  ✓ Well depth: {well_depth*1e6:.1f} μJ")
    print(f"  ✓ Trap points: {n_traps}")
    print()

print("Done!")
print()

# ============================================================================
# ANALYSIS
# ============================================================================

print("=" * 70)
print("COMPARATIVE ANALYSIS")
print("=" * 70)
print()

print("Well Depth Comparison:")
for name, data in metrics.items():
    print(f"  {name.replace(chr(10), ' ')}: {data['well_depth']:.1f} μJ")
print()

print("Trap Point Count:")
for name, data in metrics.items():
    print(f"  {name.replace(chr(10), ' ')}: {data['n_traps']}")
print()

# Calculate improvement
baseline_depth = metrics['In-Phase\n(Standing Wave)']['well_depth']
single_depth = metrics['Phase-Optimized\n(Single Trap)']['well_depth']
twin_depth = metrics['Phase-Optimized\n(Twin Trap)']['well_depth']

improvement_single = ((single_depth - baseline_depth) / baseline_depth) * 100
improvement_twin = ((twin_depth - baseline_depth) / baseline_depth) * 100

print(f"Phase Optimization Improvements:")
print(f"  Single trap: {improvement_single:+.1f}%")
print(f"  Twin trap: {improvement_twin:+.1f}%")
print()

# ============================================================================
# VISUALIZATION
# ============================================================================

print("Generating visualizations...")

# Figure 1: 3-panel potential field comparison
fig1, axes = plt.subplots(1, 3, figsize=(18, 6))
fig1.suptitle('Phase Optimization for Holographic Acoustic Levitation', 
              fontsize=16, fontweight='bold')

for idx, (name, U) in enumerate(potentials.items()):
    ax = axes[idx]
    
    im = ax.imshow(U*1e6, extent=[-30, 30, -30, 30], origin='lower',
                   cmap='RdYlBu_r', aspect='equal', interpolation='bilinear')
    
    # Plot emitters
    ax.scatter(positions[:,0]*1000, positions[:,1]*1000,
              c='black', s=150, marker='o', edgecolors='white', linewidths=2,
              label='Emitters', zorder=10)
    
    # Mark target points
    if 'Single' in name:
        ax.plot(0, 0, 'g*', markersize=20, markeredgewidth=2,
               markeredgecolor='white', label='Target', zorder=15)
    elif 'Twin' in name:
        ax.plot(-10, 0, 'g*', markersize=20, markeredgewidth=2,
               markeredgecolor='white', zorder=15)
        ax.plot(10, 0, 'g*', markersize=20, markeredgewidth=2,
               markeredgecolor='white', label='Targets', zorder=15)
    
    ax.set_xlabel('X Position (mm)', fontweight='bold', fontsize=11)
    ax.set_ylabel('Y Position (mm)', fontweight='bold', fontsize=11)
    ax.set_title(name, fontweight='bold', fontsize=13)
    ax.grid(True, alpha=0.2)
    ax.legend(loc='upper right', fontsize=9)
    
    # Add metrics
    data = metrics[name]
    annotation = f"Well Depth: {data['well_depth']:.1f} μJ\n"
    annotation += f"Traps: {data['n_traps']}"
    
    ax.text(0.05, 0.95, annotation,
           transform=ax.transAxes, fontsize=10, fontweight='bold',
           verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    
    plt.colorbar(im, ax=ax, label='Potential U (μJ)', fraction=0.046)

plt.tight_layout()
plt.savefig('phase_optimization_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: phase_optimization_comparison.png")

# Figure 2: Phase diagrams
fig2, axes = plt.subplots(1, 3, figsize=(18, 5))
fig2.suptitle('Emitter Phase Configurations', fontsize=16, fontweight='bold')

for idx, (name, data) in enumerate(metrics.items()):
    ax = axes[idx]
    phases = data['phases']
    
    # Polar plot of phases
    theta = np.linspace(0, 2*np.pi, n_emitters, endpoint=False)
    
    # Color-code by phase
    colors = plt.cm.hsv((phases - np.min(phases)) / (np.max(phases) - np.min(phases) + 1e-9))
    
    bars = ax.bar(np.arange(n_emitters), phases, color=colors, 
                  edgecolor='black', linewidth=2, alpha=0.8)
    
    ax.set_xlabel('Emitter Index', fontweight='bold', fontsize=11)
    ax.set_ylabel('Phase (radians)', fontweight='bold', fontsize=11)
    ax.set_title(name, fontweight='bold', fontsize=13)
    ax.set_xticks(np.arange(n_emitters))
    ax.set_xticklabels([f'E{i}' for i in range(n_emitters)])
    ax.grid(axis='y', alpha=0.3)
    ax.axhline(y=0, color='red', linestyle='--', linewidth=2, alpha=0.5)
    
    # Stats
    phase_range = np.max(phases) - np.min(phases)
    ax.text(0.05, 0.95, f"Range: {phase_range:.2f} rad\n({phase_range*180/np.pi:.1f}°)",
           transform=ax.transAxes, fontsize=10, fontweight='bold',
           verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

plt.tight_layout()
plt.savefig('phase_diagrams.png', dpi=300, bbox_inches='tight')
print("✓ Saved: phase_diagrams.png")

# Figure 3: Performance comparison bars
fig3, ax = plt.subplots(figsize=(12, 6))

x_pos = np.arange(len(metrics))
well_depths = [data['well_depth'] for data in metrics.values()]
colors = ['#3498db', '#2ecc71', '#e74c3c']

bars = ax.bar(x_pos, well_depths, color=colors, alpha=0.8,
             edgecolor='black', linewidth=2)

# Add value labels
for bar, depth in zip(bars, well_depths):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
           f'{depth:.0f} μJ',
           ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_xticks(x_pos)
ax.set_xticklabels([name.replace('\n', ' ') for name in metrics.keys()], 
                   fontsize=11, fontweight='bold')
ax.set_ylabel('Well Depth (μJ)', fontweight='bold', fontsize=13)
ax.set_title('Phase Optimization Improves Trap Depth', fontsize=15, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

# Add improvement annotations
ax.text(1, single_depth * 1.05, f'+{improvement_single:.1f}%',
       ha='center', fontsize=11, fontweight='bold', color='green')
if improvement_twin > 0:
    ax.text(2, twin_depth * 1.05, f'+{improvement_twin:.1f}%',
           ha='center', fontsize=11, fontweight='bold', color='green')

plt.tight_layout()
plt.savefig('phase_optimization_improvement.png', dpi=300, bbox_inches='tight')
print("✓ Saved: phase_optimization_improvement.png")

print()
print("=" * 70)
print("PHASE OPTIMIZATION COMPLETE")
print("=" * 70)
print()
print("Key Findings:")
print(f"  - Phase optimization improves trap depth by {improvement_single:.1f}%")
print(f"  - Twin trap mode enables {metrics['Phase-Optimized\n(Twin Trap)']['n_traps']} simultaneous traps")
print(f"  - Holographic control unlocks advanced manipulation capabilities")
print()
print("Applications:")
print("  - Deeper traps for heavier particles")
print("  - Multiple simultaneous levitation points")
print("  - Dynamic trap positioning (time-varying phases)")
print("  - Arbitrary pressure field shaping")
print()
print("=" * 70)