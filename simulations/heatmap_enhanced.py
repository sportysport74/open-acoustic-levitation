"""
Enhanced Heatmap Visualization with Force Vectors and Quantified Annotations
=============================================================================

Adds to the basic heatmap visualization:
- Force vector overlays (quiver plots)
- Quantified well depth annotations
- Force magnitude comparison panel
- Min/max potential text overlays

Run this AFTER gor_kov_simulation.py or copy the geometry/potential code
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PHYSICAL CONSTANTS (copy from main simulation)
# ============================================================================

SPEED_OF_SOUND = 343.0
CARRIER_FREQ = 40000
WAVELENGTH = SPEED_OF_SOUND / CARRIER_FREQ
AIR_DENSITY = 1.225
PARTICLE_RADIUS = 0.0135 / 2
PARTICLE_DENSITY = 84
SOUND_PRESSURE_AMPLITUDE = 1000

PHI = (1 + np.sqrt(5)) / 2

print("=" * 70)
print("ENHANCED HEATMAP VISUALIZATION")
print("Adding force vectors and quantified annotations")
print("=" * 70)

# ============================================================================
# GEOMETRY DEFINITIONS
# ============================================================================

def flower_of_life_positions(r1_wavelengths=2.5):
    r1 = r1_wavelengths * WAVELENGTH
    positions = [
        (0, 0, 0),
        (r1, 0, 0),
        (r1 * np.cos(np.pi/3), r1 * np.sin(np.pi/3), 0),
        (r1 * np.cos(2*np.pi/3), r1 * np.sin(2*np.pi/3), 0),
        (r1 * np.cos(np.pi), r1 * np.sin(np.pi), 0),
        (r1 * np.cos(4*np.pi/3), r1 * np.sin(4*np.pi/3), 0),
        (r1 * np.cos(5*np.pi/3), r1 * np.sin(5*np.pi/3), 0),
    ]
    return np.array(positions)

def square_grid_positions():
    spacing = 2.5 * WAVELENGTH
    positions = [
        (0, 0, 0),
        (spacing, 0, 0),
        (-spacing, 0, 0),
        (0, spacing, 0),
        (0, -spacing, 0),
        (spacing, spacing, 0),
        (-spacing, -spacing, 0),
    ]
    return np.array(positions)

def random_positions(seed=42):
    np.random.seed(seed)
    r_max = 3 * WAVELENGTH
    positions = [(0, 0, 0)]
    for _ in range(6):
        r = np.random.uniform(WAVELENGTH, r_max)
        theta = np.random.uniform(0, 2*np.pi)
        positions.append((r * np.cos(theta), r * np.sin(theta), 0))
    return np.array(positions)

# ============================================================================
# FIELD CALCULATIONS
# ============================================================================

def acoustic_pressure_field(positions, x, y, z):
    k = 2 * np.pi / WAVELENGTH
    p_total = 0
    for i, (ex, ey, ez) in enumerate(positions):
        r = np.sqrt((x - ex)**2 + (y - ey)**2 + (z - ez)**2)
        if r < 1e-6:
            r = 1e-6
        p_total += (SOUND_PRESSURE_AMPLITUDE / r) * np.exp(1j * k * r)
    return p_total

def gor_kov_potential(positions, x, y, z):
    V0 = (4/3) * np.pi * PARTICLE_RADIUS**3
    f1 = 1 - (AIR_DENSITY / PARTICLE_DENSITY)
    
    p_complex = acoustic_pressure_field(positions, x, y, z)
    p_magnitude_sq = np.abs(p_complex)**2
    
    U = -V0 * (f1 / (2 * AIR_DENSITY * SPEED_OF_SOUND**2)) * p_magnitude_sq
    return U

# ============================================================================
# CALCULATE FIELDS
# ============================================================================

print("\nCalculating potential fields...")

x_range = np.linspace(-0.04, 0.04, 100)
y_range = np.linspace(-0.04, 0.04, 100)
z_levitation = 0.005

X, Y = np.meshgrid(x_range, y_range)
Z = np.zeros_like(X) + z_levitation

# Calculate potentials
geometries = {
    'Flower of Life': flower_of_life_positions(),
    'Square Grid': square_grid_positions(),
    'Random': random_positions()
}

potentials = {}
for name, positions in geometries.items():
    print(f"  Calculating: {name}...")
    U = np.zeros_like(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            U[i, j] = gor_kov_potential(positions, X[i,j], Y[i,j], Z[i,j])
    potentials[name] = U

print("  Done!\n")

# ============================================================================
# ENHANCED VISUALIZATION: HEATMAPS WITH FORCE VECTORS
# ============================================================================

print("Generating enhanced heatmap with force vectors...")

fig = plt.figure(figsize=(24, 8))
fig.suptitle('Enhanced Acoustic Potential Analysis - Heatmaps with Force Vectors', 
             fontsize=18, fontweight='bold')

# Calculate force vectors for quiver plot (subsample grid for clarity)
step = 5  # Plot every 5th vector
X_quiver = X[::step, ::step]
Y_quiver = Y[::step, ::step]

for idx, (geom_name, U) in enumerate(potentials.items()):
    ax = fig.add_subplot(1, 3, idx+1)
    
    # Heatmap
    im = ax.imshow(U*1e6, extent=[-40, 40, -40, 40], origin='lower', 
                   cmap='RdYlBu_r', aspect='equal', interpolation='bilinear')
    
    # Calculate force vectors (gradient)
    U_grad_y, U_grad_x = np.gradient(U*1e6)
    
    # Subsample for quiver
    U_grad_x_sub = U_grad_x[::step, ::step]
    U_grad_y_sub = U_grad_y[::step, ::step]
    
    # Force = -gradient (particles move toward lower potential)
    Fx = -U_grad_x_sub
    Fy = -U_grad_y_sub
    
    # Normalize for visualization
    force_mag = np.sqrt(Fx**2 + Fy**2)
    force_mag_safe = np.where(force_mag > 0, force_mag, 1)  # Avoid div by zero
    Fx_norm = Fx / force_mag_safe
    Fy_norm = Fy / force_mag_safe
    
    # Quiver plot (force vectors)
    quiver = ax.quiver(X_quiver*1000, Y_quiver*1000, Fx_norm, Fy_norm,
                      force_mag, cmap='plasma', alpha=0.6, 
                      scale=30, width=0.003, headwidth=4, headlength=5)
    
    # Emitter positions
    emitter_pos = geometries[geom_name]
    ax.scatter(emitter_pos[:,0]*1000, emitter_pos[:,1]*1000,
              c='black', s=250, marker='o', edgecolors='white', linewidths=3, 
              label='Emitters', zorder=10)
    
    # Trap center
    ax.plot(0, 0, 'w+', markersize=20, markeredgewidth=4, zorder=15)
    
    # Get min/max values for annotations
    U_min = np.min(U*1e6)
    U_max = np.max(U*1e6)
    well_depth = U_max - U_min
    
    # Find min position
    min_idx = np.unravel_index(np.argmin(U), U.shape)
    min_x = X[min_idx] * 1000
    min_y = Y[min_idx] * 1000
    
    # Add text annotations
    ax.text(0.05, 0.95, f'Min U: {U_min:.2f} μJ\nMax U: {U_max:.2f} μJ\nWell Depth: {well_depth:.2f} μJ',
           transform=ax.transAxes, fontsize=11, fontweight='bold',
           verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Mark minimum location
    ax.scatter(min_x, min_y, c='lime', s=300, marker='X', 
              edgecolors='black', linewidths=2, zorder=12, label='Min Potential')
    
    ax.set_xlabel('X Position (mm)', fontweight='bold', fontsize=12)
    ax.set_ylabel('Y Position (mm)', fontweight='bold', fontsize=12)
    ax.set_title(f'{geom_name}\n(Arrows = Force Direction)', fontweight='bold', fontsize=14)
    ax.grid(True, alpha=0.2, linestyle='--')
    
    # Colorbar for potential
    cbar = plt.colorbar(im, ax=ax, label='Potential U (μJ)', fraction=0.046, pad=0.04)
    
    ax.legend(loc='lower right', fontsize=9)

plt.tight_layout()
plt.savefig('heatmap_enhanced_with_forces.png', dpi=300, bbox_inches='tight')
print("✓ Saved: heatmap_enhanced_with_forces.png")

# ============================================================================
# FORCE MAGNITUDE COMPARISON PANEL
# ============================================================================

print("Generating force magnitude comparison...")

fig2 = plt.figure(figsize=(24, 8))
fig2.suptitle('Force Field Magnitude Comparison - |∇U|', 
              fontsize=18, fontweight='bold')

for idx, (geom_name, U) in enumerate(potentials.items()):
    ax = fig2.add_subplot(1, 3, idx+1)
    
    # Calculate gradient magnitude
    U_grad_y, U_grad_x = np.gradient(U*1e6)
    force_magnitude = np.sqrt(U_grad_x**2 + U_grad_y**2)
    
    # Heatmap of force magnitude
    im = ax.imshow(force_magnitude, extent=[-40, 40, -40, 40], origin='lower',
                  cmap='hot', aspect='equal', interpolation='bilinear')
    
    # Emitter positions
    emitter_pos = geometries[geom_name]
    ax.scatter(emitter_pos[:,0]*1000, emitter_pos[:,1]*1000,
              c='cyan', s=250, marker='o', edgecolors='white', linewidths=3, 
              label='Emitters', zorder=10)
    
    # Trap center
    ax.plot(0, 0, 'w+', markersize=20, markeredgewidth=4, zorder=15)
    
    # Stats
    force_max = np.max(force_magnitude)
    force_mean = np.mean(force_magnitude)
    
    # Find max force location (edge of trap)
    max_idx = np.unravel_index(np.argmax(force_magnitude), force_magnitude.shape)
    max_x = X[max_idx] * 1000
    max_y = Y[max_idx] * 1000
    
    ax.text(0.05, 0.95, f'Max |∇U|: {force_max:.2f} μJ/mm\nMean |∇U|: {force_mean:.2f} μJ/mm',
           transform=ax.transAxes, fontsize=11, fontweight='bold',
           verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Mark maximum force location
    ax.scatter(max_x, max_y, c='lime', s=300, marker='X', 
              edgecolors='black', linewidths=2, zorder=12, label='Max Force')
    
    ax.set_xlabel('X Position (mm)', fontweight='bold', fontsize=12)
    ax.set_ylabel('Y Position (mm)', fontweight='bold', fontsize=12)
    ax.set_title(f'{geom_name}\nForce Strength', fontweight='bold', fontsize=14)
    ax.grid(True, alpha=0.2, linestyle='--')
    
    cbar = plt.colorbar(im, ax=ax, label='|∇U| (μJ/mm)', fraction=0.046, pad=0.04)
    
    ax.legend(loc='lower right', fontsize=9)

plt.tight_layout()
plt.savefig('force_magnitude_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: force_magnitude_comparison.png")

# ============================================================================
# COMBINED 4-PANEL ANALYSIS (FoL ONLY)
# ============================================================================

print("Generating 4-panel FoL detailed analysis...")

fig3 = plt.figure(figsize=(20, 16))
fig3.suptitle('Flower of Life - Comprehensive 4-Panel Analysis', 
              fontsize=18, fontweight='bold')

U_fol = potentials['Flower of Life']
fol_positions = geometries['Flower of Life']

# Panel 1: Potential field with force vectors
ax1 = fig3.add_subplot(2, 2, 1)
im1 = ax1.imshow(U_fol*1e6, extent=[-40, 40, -40, 40], origin='lower',
                cmap='RdYlBu_r', aspect='equal', interpolation='bilinear')

U_grad_y, U_grad_x = np.gradient(U_fol*1e6)
U_grad_x_sub = U_grad_x[::step, ::step]
U_grad_y_sub = U_grad_y[::step, ::step]
Fx = -U_grad_x_sub
Fy = -U_grad_y_sub
force_mag = np.sqrt(Fx**2 + Fy**2)
force_mag_safe = np.where(force_mag > 0, force_mag, 1)
Fx_norm = Fx / force_mag_safe
Fy_norm = Fy / force_mag_safe

ax1.quiver(X_quiver*1000, Y_quiver*1000, Fx_norm, Fy_norm,
          force_mag, cmap='plasma', alpha=0.6, scale=30, width=0.003)
ax1.scatter(fol_positions[:,0]*1000, fol_positions[:,1]*1000,
           c='black', s=250, marker='o', edgecolors='white', linewidths=3, zorder=10)
ax1.plot(0, 0, 'w+', markersize=20, markeredgewidth=4, zorder=15)

U_min = np.min(U_fol*1e6)
well_depth = np.max(U_fol*1e6) - U_min
ax1.text(0.05, 0.95, f'Well Depth: {well_depth:.2f} μJ\nMin U: {U_min:.2f} μJ',
        transform=ax1.transAxes, fontsize=12, fontweight='bold',
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

ax1.set_title('Potential Field + Force Vectors', fontweight='bold', fontsize=14)
ax1.set_xlabel('X (mm)', fontweight='bold')
ax1.set_ylabel('Y (mm)', fontweight='bold')
plt.colorbar(im1, ax=ax1, label='U (μJ)', fraction=0.046)

# Panel 2: Force magnitude
ax2 = fig3.add_subplot(2, 2, 2)
force_magnitude = np.sqrt(U_grad_x**2 + U_grad_y**2)
im2 = ax2.imshow(force_magnitude, extent=[-40, 40, -40, 40], origin='lower',
                cmap='hot', aspect='equal', interpolation='bilinear')
ax2.scatter(fol_positions[:,0]*1000, fol_positions[:,1]*1000,
           c='cyan', s=250, marker='o', edgecolors='white', linewidths=3, zorder=10)
ax2.plot(0, 0, 'w+', markersize=20, markeredgewidth=4, zorder=15)

force_max = np.max(force_magnitude)
ax2.text(0.05, 0.95, f'Max Force: {force_max:.2f} μJ/mm',
        transform=ax2.transAxes, fontsize=12, fontweight='bold',
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

ax2.set_title('Force Field Strength |∇U|', fontweight='bold', fontsize=14)
ax2.set_xlabel('X (mm)', fontweight='bold')
ax2.set_ylabel('Y (mm)', fontweight='bold')
plt.colorbar(im2, ax=ax2, label='|∇U| (μJ/mm)', fraction=0.046)

# Panel 3: Equipotential contours with annotations
ax3 = fig3.add_subplot(2, 2, 3)
levels = np.linspace(np.min(U_fol*1e6), np.max(U_fol*1e6), 20)
contourf = ax3.contourf(X*1000, Y*1000, U_fol*1e6, levels=levels, cmap='viridis')
contour = ax3.contour(X*1000, Y*1000, U_fol*1e6, levels=levels, colors='white', 
                     linewidths=0.5, alpha=0.5)
ax3.clabel(contour, inline=True, fontsize=8, fmt='%0.1f')

ax3.scatter(fol_positions[:,0]*1000, fol_positions[:,1]*1000,
           c='red', s=250, marker='o', edgecolors='white', linewidths=3, zorder=10)
ax3.plot(0, 0, 'w+', markersize=20, markeredgewidth=4, zorder=15)

ax3.set_title('Equipotential Contours', fontweight='bold', fontsize=14)
ax3.set_xlabel('X (mm)', fontweight='bold')
ax3.set_ylabel('Y (mm)', fontweight='bold')
ax3.set_aspect('equal')
plt.colorbar(contourf, ax=ax3, label='U (μJ)', fraction=0.046)

# Panel 4: Quantified comparison bar chart
ax4 = fig3.add_subplot(2, 2, 4)

metrics = {}
for name, U in potentials.items():
    U_grad_y, U_grad_x = np.gradient(U*1e6)
    metrics[name] = {
        'well_depth': np.max(U*1e6) - np.min(U*1e6),
        'max_force': np.max(np.sqrt(U_grad_x**2 + U_grad_y**2)),
        'mean_force': np.mean(np.sqrt(U_grad_x**2 + U_grad_y**2))
    }

x_pos = np.arange(len(metrics))
width = 0.25

well_depths = [metrics[name]['well_depth'] for name in metrics.keys()]
max_forces = [metrics[name]['max_force'] for name in metrics.keys()]
mean_forces = [metrics[name]['mean_force'] for name in metrics.keys()]

bars1 = ax4.bar(x_pos - width, well_depths, width, label='Well Depth (μJ)', 
               color='#2ecc71', alpha=0.8, edgecolor='black', linewidth=1.5)
bars2 = ax4.bar(x_pos, max_forces, width, label='Max Force (μJ/mm)', 
               color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)
bars3 = ax4.bar(x_pos + width, mean_forces, width, label='Mean Force (μJ/mm)', 
               color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.5)

# Add value labels
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

ax4.set_ylabel('Value', fontweight='bold', fontsize=12)
ax4.set_title('Quantified Performance Metrics', fontweight='bold', fontsize=14)
ax4.set_xticks(x_pos)
ax4.set_xticklabels([name.replace(' ', '\n') for name in metrics.keys()], fontsize=10)
ax4.legend(fontsize=10, loc='upper left')
ax4.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('fol_4panel_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: fol_4panel_analysis.png")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("ENHANCED VISUALIZATION COMPLETE!")
print("=" * 70)
print("\nGenerated files:")
print("  1. heatmap_enhanced_with_forces.png - Force vector overlays")
print("  2. force_magnitude_comparison.png - |∇U| comparison")
print("  3. fol_4panel_analysis.png - Comprehensive FoL analysis")
print("\nKey additions:")
print("  ✓ Force vectors (quiver plots) showing trap dynamics")
print("  ✓ Quantified annotations (min U, well depth, max force)")
print("  ✓ Force magnitude heatmaps")
print("  ✓ 4-panel comprehensive analysis")
print("=" * 70)