"""
Quick Manual Visualization
===========================
For when optimization crashes before visualization
"""

import json
import numpy as np
import matplotlib.pyplot as plt

# The AI found these positions (from your last run):
# Best well depth: 93845.93 µJ (996% improvement!)

# Since we don't have the JSON, let's visualize FoL for comparison
# and explain what happened

wavelength = 343.0 / 40000.0

# FoL geometry
r1 = 2.5 * wavelength
fol_positions = [[0, 0]]
for i in range(6):
    theta = i * np.pi / 3
    fol_positions.append([r1 * np.cos(theta), r1 * np.sin(theta)])

fol_positions = np.array(fol_positions) * 1000  # Convert to mm

# Create figure
fig, ax = plt.subplots(1, 1, figsize=(10, 10))

# Plot FoL
ax.scatter(fol_positions[:, 0], fol_positions[:, 1],
          s=500, c='#00ff88', marker='o', 
          edgecolors='white', linewidths=3,
          label='Flower of Life (8,566 µJ)', alpha=0.8, zorder=10)

# Add labels
for i, pos in enumerate(fol_positions):
    ax.annotate(f'{i+1}', (pos[0], pos[1]), 
               fontsize=14, fontweight='bold',
               ha='center', va='center')

ax.set_xlabel('X Position (mm)', fontsize=14, fontweight='bold')
ax.set_ylabel('Y Position (mm)', fontsize=14, fontweight='bold')
ax.set_title('Flower of Life Baseline\n(AI found 996% better!)', 
            fontsize=16, fontweight='bold')
ax.set_aspect('equal')
ax.grid(alpha=0.3)
ax.legend(fontsize=12)
ax.set_xlim(-30, 30)
ax.set_ylim(-30, 30)

# Add text box with results
textstr = f'''AI OPTIMIZATION RESULTS:
━━━━━━━━━━━━━━━━━━━━━━━
FoL Baseline: 8,566 µJ
AI Best: 93,846 µJ
Improvement: +996% (11× better!)

Time: 1.9 minutes on RTX 5090
Generations: 693
Population: 150

🔥 AI DISCOVERED GEOMETRY
   ALMOST 11× STRONGER!
'''

props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', fontfamily='monospace', bbox=props)

plt.tight_layout()
plt.savefig('fol_baseline_with_ai_results.png', dpi=300, bbox_inches='tight')
print("✓ Saved: fol_baseline_with_ai_results.png")
print()
print("=" * 70)
print("📊 AI FOUND 996% IMPROVEMENT!")
print("=" * 70)
print()
print("To see the ACTUAL AI pattern, run:")
print("  python neural_optimizer.py")
print("  Choose option 1 (Evolutionary only)")
print()
print("This will create ai_discovered_geometry.png showing")
print("the exact emitter positions AI discovered!")
print("=" * 70)

plt.show()
