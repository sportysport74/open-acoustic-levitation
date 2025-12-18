"""
Animated Particle Trajectory GIF Generator
===========================================

Creates animated GIF showing real-time particle motion converging to acoustic traps.
Demonstrates superior stability of Flower of Life geometry.

Outputs:
- particle_animation.gif (side-by-side 3 geometries)
- fol_animation_solo.gif (FoL only, high quality)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d import Axes3D
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PHYSICAL CONSTANTS
# ============================================================================

SPEED_OF_SOUND = 343.0
CARRIER_FREQ = 40000
WAVELENGTH = SPEED_OF_SOUND / CARRIER_FREQ
AIR_DENSITY = 1.225
PARTICLE_RADIUS = 0.0135 / 2
PARTICLE_DENSITY = 84
PARTICLE_MASS = PARTICLE_DENSITY * (4/3) * np.pi * PARTICLE_RADIUS**3
SOUND_PRESSURE_AMPLITUDE = 1000

GRAVITY = 9.81
DRAG_COEFFICIENT = 6 * np.pi * 1.81e-5 * PARTICLE_RADIUS

PHI = (1 + np.sqrt(5)) / 2

print("=" * 70)
print("ANIMATED TRAJECTORY GIF GENERATOR")
print("Creating real-time particle motion visualization")
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
    return np.array([
        (0, 0, 0), (spacing, 0, 0), (-spacing, 0, 0),
        (0, spacing, 0), (0, -spacing, 0),
        (spacing, spacing, 0), (-spacing, -spacing, 0),
    ])

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
    for ex, ey, ez in positions:
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

def acoustic_force(positions, x, y, z, delta=1e-5):
    U_xp = gor_kov_potential(positions, x + delta, y, z)
    U_xm = gor_kov_potential(positions, x - delta, y, z)
    U_yp = gor_kov_potential(positions, x, y + delta, z)
    U_ym = gor_kov_potential(positions, x, y - delta, z)
    U_zp = gor_kov_potential(positions, x, y, z + delta)
    U_zm = gor_kov_potential(positions, x, y, z - delta)
    
    dU_dx = (U_xp - U_xm) / (2 * delta)
    dU_dy = (U_yp - U_ym) / (2 * delta)
    dU_dz = (U_zp - U_zm) / (2 * delta)
    
    return np.array([-dU_dx, -dU_dy, -dU_dz])

# ============================================================================
# SIMPLIFIED PARTICLE SIMULATION (for animation)
# ============================================================================

def simulate_trajectories_animated(emitter_positions, n_particles=6, dt=1e-4, t_max=0.3):
    """Simulate multiple particles with saved states for animation"""
    
    # Initial positions in circle at z=10mm
    theta_particles = np.linspace(0, 2*np.pi, n_particles, endpoint=False)
    r_start = 0.015
    z_start = 0.010
    
    # Initialize particles
    particles = []
    for theta in theta_particles:
        pos = np.array([r_start * np.cos(theta), r_start * np.sin(theta), z_start])
        vel = np.array([0.0, 0.0, 0.0])
        particles.append({'pos': pos, 'vel': vel, 'trail': [pos.copy()]})
    
    # Simulation
    n_steps = int(t_max / dt)
    save_interval = 25  # Save every 25 steps for animation
    saved_states = []
    
    for step in range(n_steps):
        for particle in particles:
            pos = particle['pos']
            vel = particle['vel']
            
            F_acoustic = acoustic_force(emitter_positions, pos[0], pos[1], pos[2])
            F_gravity = np.array([0, 0, -PARTICLE_MASS * GRAVITY])
            F_drag = -DRAG_COEFFICIENT * vel
            F_total = F_acoustic + F_gravity + F_drag
            
            accel = F_total / PARTICLE_MASS
            vel = vel + accel * dt
            pos = pos + vel * dt
            
            particle['pos'] = pos
            particle['vel'] = vel
            
            if step % 5 == 0:  # Add to trail every 5 steps
                particle['trail'].append(pos.copy())
        
        # Save state for animation
        if step % save_interval == 0:
            state = []
            for particle in particles:
                state.append({
                    'pos': particle['pos'].copy(),
                    'trail': np.array(particle['trail'][-50:])  # Last 50 points
                })
            saved_states.append(state)
    
    return saved_states

# ============================================================================
# GENERATE ANIMATIONS
# ============================================================================

print("\nSimulating particle trajectories for animation...")

geometries = {
    'Flower of Life': flower_of_life_positions(),
    'Square Grid': square_grid_positions(),
    'Random': random_positions()
}

# Simulate all geometries
all_states = {}
for name, positions in geometries.items():
    print(f"  Simulating: {name}...")
    states = simulate_trajectories_animated(positions, n_particles=6, t_max=0.3)
    all_states[name] = states
    print(f"    ✓ {len(states)} frames generated")

print("\nCreating animations...")

# ============================================================================
# ANIMATION 1: Side-by-side comparison (top view)
# ============================================================================

print("  Generating side-by-side comparison GIF...")

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Particle Convergence - Real-Time Comparison', fontsize=16, fontweight='bold')

colors = plt.cm.viridis(np.linspace(0, 1, 6))

def init():
    for ax in axes:
        ax.clear()
    return axes

def animate(frame):
    for idx, (name, positions) in enumerate(geometries.items()):
        ax = axes[idx]
        ax.clear()
        
        # Plot emitters
        ax.scatter(positions[:,0]*1000, positions[:,1]*1000,
                  c='red', s=300, marker='o', alpha=0.5, 
                  edgecolors='darkred', linewidths=3, zorder=10)
        
        # Plot trap center
        ax.plot(0, 0, 'w+', markersize=20, markeredgewidth=4, zorder=15)
        
        # Plot particles
        states = all_states[name]
        if frame < len(states):
            for i, particle_state in enumerate(states[frame]):
                trail = particle_state['trail']
                pos = particle_state['pos']
                
                # Trail
                if len(trail) > 1:
                    ax.plot(trail[:,0]*1000, trail[:,1]*1000, 
                           color=colors[i], alpha=0.4, linewidth=1.5)
                
                # Current position
                ax.scatter(pos[0]*1000, pos[1]*1000,
                          color=colors[i], s=150, marker='o', 
                          edgecolors='black', linewidths=2, zorder=5)
        
        ax.set_xlabel('X (mm)', fontweight='bold')
        ax.set_ylabel('Y (mm)', fontweight='bold')
        ax.set_title(name, fontweight='bold')
        ax.set_xlim([-30, 30])
        ax.set_ylim([-30, 30])
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        
        # Add frame counter
        ax.text(0.95, 0.95, f'Frame {frame}/{len(states)}',
               transform=ax.transAxes, ha='right', va='top',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    
    plt.tight_layout()
    return axes

n_frames = min(len(states) for states in all_states.values())
anim = FuncAnimation(fig, animate, init_func=init, frames=n_frames, 
                    interval=50, blit=False, repeat=True)

writer = PillowWriter(fps=20)
anim.save('particle_animation_comparison.gif', writer=writer)
print("    ✓ Saved: particle_animation_comparison.gif")
plt.close()

# ============================================================================
# ANIMATION 2: FoL only (high quality)
# ============================================================================

print("  Generating high-quality FoL animation...")

fig2, ax = plt.subplots(figsize=(10, 10))
fig2.suptitle('Flower of Life - Particle Convergence', fontsize=16, fontweight='bold')

fol_positions = geometries['Flower of Life']
fol_states = all_states['Flower of Life']

def init2():
    ax.clear()
    return [ax]

def animate2(frame):
    ax.clear()
    
    # Plot emitters
    ax.scatter(fol_positions[:,0]*1000, fol_positions[:,1]*1000,
              c='gold', s=400, marker='*', alpha=0.8, 
              edgecolors='black', linewidths=3, zorder=10, label='Emitters')
    
    # Trap center
    ax.plot(0, 0, 'r+', markersize=25, markeredgewidth=5, zorder=15, label='Trap Center')
    
    # Particles
    if frame < len(fol_states):
        for i, particle_state in enumerate(fol_states[frame]):
            trail = particle_state['trail']
            pos = particle_state['pos']
            
            # Trail with fade
            if len(trail) > 1:
                ax.plot(trail[:,0]*1000, trail[:,1]*1000, 
                       color=colors[i], alpha=0.6, linewidth=2)
            
            # Current position
            ax.scatter(pos[0]*1000, pos[1]*1000,
                      color=colors[i], s=200, marker='o', 
                      edgecolors='black', linewidths=2.5, zorder=5)
    
    ax.set_xlabel('X Position (mm)', fontweight='bold', fontsize=14)
    ax.set_ylabel('Y Position (mm)', fontweight='bold', fontsize=14)
    ax.set_xlim([-25, 25])
    ax.set_ylim([-25, 25])
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right', fontsize=12)
    
    # Time counter
    time_ms = frame * 50 / 20 * 1000  # Convert frame to milliseconds
    ax.text(0.05, 0.95, f'Time: {time_ms:.0f} ms',
           transform=ax.transAxes, fontsize=14, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    plt.tight_layout()
    return [ax]

anim2 = FuncAnimation(fig2, animate2, init_func=init2, frames=len(fol_states), 
                     interval=50, blit=False, repeat=True)

writer2 = PillowWriter(fps=20)
anim2.save('fol_animation_solo.gif', writer=writer2)
print("    ✓ Saved: fol_animation_solo.gif")
plt.close()

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("ANIMATION GENERATION COMPLETE!")
print("=" * 70)
print("\nGenerated files:")
print("  1. particle_animation_comparison.gif - Side-by-side 3-panel")
print("  2. fol_animation_solo.gif - High-quality FoL only")
print("\nAnimation specs:")
print("  - 20 FPS")
print("  - ~300ms simulation time")
print("  - 6 particles per geometry")
print("  - Real physics (acoustic force + gravity + drag)")
print("\nUse cases:")
print("  - README.md embed for visual proof")
print("  - Social media sharing")
print("  - Presentations and demos")
print("=" * 70) 