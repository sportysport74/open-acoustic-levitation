import json
import numpy as np
import matplotlib.pyplot as plt
import os

def load_ai_results(filename):
    if not os.path.exists(filename):
        print(f"❌ Error: {filename} not found!")
        return None
    with open(filename, 'r') as f:
        return json.load(f)

# 1. Load the data
results = load_ai_results('constrained_optimization_results.json')

# 2. Setup Baseline Flower of Life (FoL)
wavelength = 343.0 / 40000.0
r1 = 2.5 * wavelength
fol_positions = [[0, 0]]
for i in range(6):
    theta = i * np.pi / 3
    fol_positions.append([r1 * np.cos(theta), r1 * np.sin(theta)])
fol_positions = np.array(fol_positions) * 1000  # Convert to mm

# 3. Create Visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# --- Plot 1: Flower of Life ---
ax1.scatter(fol_positions[:, 0], fol_positions[:, 1],
            s=800, c='#00ff88', marker='o', edgecolors='black', 
            linewidths=2, alpha=0.7, label='FoL Baseline')
ax1.set_title(f"Standard Flower of Life\nDepth: 8,566 µJ", fontsize=14, fontweight='bold')

# --- Plot 2: AI Constrained Discovery ---
if results:
    # Try different possible keys for positions
    if 'best_positions_mm' in results:
        ai_pos = np.array(results['best_positions_mm'])
    elif 'best_positions' in results:
        ai_pos = np.array(results['best_positions'])
        # If the values are very small (e.g. 0.01), they are in meters, convert to mm
        if np.max(np.abs(ai_pos)) < 1.0:
            ai_pos = ai_pos * 1000
    else:
        print("❌ Could not find position data in JSON. Keys found:", results.keys())
        ai_pos = None

    if ai_pos is not None:
        depth = results.get('best_depth_uj', results.get('best_fitness', 0))
        improvement = results.get('improvement_percent', 0)
        
        ax2.scatter(ai_pos[:, 0], ai_pos[:, 1],
                    s=800, c='#ff3366', marker='h', edgecolors='black', 
                    linewidths=2, alpha=0.8, label='AI Optimized')
        
        # Draw a 5mm "collision circle" (2.5mm radius)
        for pos in ai_pos:
            circle = plt.Circle((pos[0], pos[1]), 2.5, color='red', fill=False, linestyle='--', alpha=0.3)
            ax2.add_patch(circle)
            
        ax2.set_title(f"AI CONSTRAINED GEOMETRY\nDepth: {depth:.1f} µJ (+{improvement:.1f}%)", 
                      fontsize=14, fontweight='bold', color='#ff3366')
else:
    ax2.text(0.5, 0.5, "Data not found.", ha='center', va='center')

# Formatting
for ax in [ax1, ax2]:
    ax.set_aspect('equal')
    ax.set_xlim(-40, 40)
    ax.set_ylim(-40, 40)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper right')

plt.tight_layout()
plt.savefig('ai_vs_fol_comparison.png', dpi=300)
print("✅ Comparison saved to: ai_vs_fol_comparison.png")
plt.show()