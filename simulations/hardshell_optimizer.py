"""
🌸 HARD-SHELL FLOWER OF LIFE OPTIMIZER 🌸
==========================================

"Axiom of Physical Choice" Implementation

This optimizer:
✓ Starts from sacred Flower of Life geometry
✓ Allows AI to "tune" positions locally
✓ HARD constraint: zero overlaps allowed
✓ Evaluates toroidal field symmetry
✓ Finds local optimum near FoL

Philosophy:
The Flower of Life represents nature's "Choice" from infinite possibilities.
Instead of asking AI to rediscover this from scratch, we let it optimize
within the sacred geometric framework.

This is like tuning a violin (FoL) rather than building one from scratch (random AI).

Authors: Sportysport & Claude (Anthropic)
License: MIT
"""

import numpy as np
import torch
import torch.optim as optim
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import json
import time
from datetime import datetime

print("=" * 80)
print("🌸 HARD-SHELL FLOWER OF LIFE OPTIMIZER")
print("=" * 80)
print()
print("Philosophy: Tune sacred geometry, don't reinvent it!")
print()

# Check GPU
if torch.cuda.is_available():
    device = torch.device('cuda')
    gpu_name = torch.cuda.get_device_name(0)
    print(f"✓ GPU: {gpu_name}")
    print(f"✓ CUDA: {torch.version.cuda}")
else:
    device = torch.device('cpu')
    gpu_name = "CPU"
    print("⚠️  Using CPU")
print()

# Constants
SPEED_OF_SOUND = 343.0
AIR_DENSITY = 1.225
PHI = (1 + np.sqrt(5)) / 2  # Golden ratio

# HARD-SHELL CONSTRAINTS
TRANSDUCER_DIAMETER = 0.010  # 10mm physical diameter
MIN_SPACING = 0.012  # 12mm center-to-center (10mm + 2mm clearance)
MAX_PERTURBATION = 0.005  # 5mm maximum deviation from FoL
MAX_SPREAD = 0.080  # 80mm from center

class HardShellOptimizer:
    """Optimize FoL with hard physical constraints"""
    
    def __init__(self, n_emitters=19, frequency=40000.0, device='cuda'):
        self.device = device
        self.n_emitters = n_emitters
        self.frequency = frequency
        self.wavelength = 343.0 / frequency
        
        # Get perfect FoL as reference
        self.fol_reference = self._get_perfect_fol()
        
        self.history = []
        
    def _get_perfect_fol(self):
        """Get mathematically perfect Flower of Life"""
        r1 = 2.5 * self.wavelength  # ~21mm for 40kHz
        r2 = 5.0 * self.wavelength  # ~43mm
        
        positions = [[0, 0]]
        
        # Ring 1: 6 emitters (60° spacing)
        for i in range(6):
            theta = i * np.pi / 3
            positions.append([r1 * np.cos(theta), r1 * np.sin(theta)])
        
        # Ring 2: 12 emitters (30° spacing)
        for i in range(12):
            theta = i * np.pi / 6
            positions.append([r2 * np.cos(theta), r2 * np.sin(theta)])
        
        return torch.tensor(positions[:self.n_emitters], 
                          dtype=torch.float32, device=self.device)
    
    def check_hard_shell_collision(self, positions):
        """
        HARD-SHELL: Check if any transducers physically overlap
        
        Returns:
            collision (bool): True if ANY collision detected
            min_distance (float): Minimum distance found
        """
        min_dist = float('inf')
        collision = False
        
        for i in range(self.n_emitters):
            for j in range(i + 1, self.n_emitters):
                dist = torch.sqrt(torch.sum((positions[i] - positions[j])**2))
                min_dist = min(min_dist, dist.item())
                
                if dist < MIN_SPACING:
                    collision = True
        
        return collision, min_dist
    
    def check_perturbation_limit(self, positions):
        """Check if positions deviated too far from FoL reference"""
        deviations = torch.sqrt(torch.sum((positions - self.fol_reference)**2, dim=1))
        max_deviation = deviations.max().item()
        
        exceeded = max_deviation > MAX_PERTURBATION
        
        return exceeded, max_deviation
    
    def calculate_field_quality(self, positions):
        """
        Calculate field quality metrics:
        - Well depth (trap strength)
        - Toroidal symmetry (how circular the field is)
        - Field uniformity (how stable the trap is)
        """
        # Evaluation grid (fine for quality measurement)
        grid_size = 80
        extent = 0.06
        
        x = torch.linspace(-extent, extent, grid_size, device=self.device)
        y = torch.linspace(-extent, extent, grid_size, device=self.device)
        X, Y = torch.meshgrid(x, y, indexing='ij')
        
        # Evaluate at z=5mm (typical levitation height)
        Z = torch.full_like(X, 0.005)
        
        grid_points = torch.stack([X.ravel(), Y.ravel(), Z.ravel()], dim=1)
        
        # Add z=0 to emitters
        emitters_3d = torch.cat([positions, 
                                torch.zeros(self.n_emitters, 1, device=self.device)], 
                               dim=1)
        
        # Calculate potential
        U = self._calculate_potential(grid_points, emitters_3d)
        U_grid = U.reshape(X.shape)
        
        # Metrics
        well_depth = (U.max() - U.min()).item()
        
        # Toroidal symmetry: measure radial uniformity
        r_grid = torch.sqrt(X**2 + Y**2)
        
        # Sample at different radii
        radii = [0.01, 0.02, 0.03, 0.04]  # 10mm, 20mm, 30mm, 40mm
        symmetry_score = 0
        
        for r in radii:
            mask = (r_grid > r - 0.002) & (r_grid < r + 0.002)
            if mask.sum() > 0:
                ring_values = U_grid[mask]
                ring_std = ring_values.std().item()
                symmetry_score += 1.0 / (ring_std + 1e-6)  # Lower std = higher score
        
        symmetry_score /= len(radii)
        
        # Uniformity: how flat is the bottom of the well
        trap_region = U < (U.min() + 0.1 * (U.max() - U.min()))
        if trap_region.sum() > 0:
            uniformity = 1.0 / (U[trap_region].std().item() + 1e-6)
        else:
            uniformity = 0
        
        return {
            'well_depth': well_depth,
            'symmetry': symmetry_score,
            'uniformity': uniformity,
            'total_score': well_depth * 1e6 + symmetry_score * 1000 + uniformity * 100
        }
    
    def _calculate_potential(self, points, emitters):
        """Calculate Gor'kov potential"""
        k = 2 * np.pi / self.wavelength
        
        pts = points.unsqueeze(1)
        ems = emitters.unsqueeze(0)
        
        r = torch.sqrt(torch.sum((pts - ems)**2, dim=2))
        r = torch.clamp(r, min=1e-6)
        
        pressure_amp = 1000.0
        p_real = (pressure_amp / r) * torch.cos(k * r)
        p_imag = (pressure_amp / r) * torch.sin(k * r)
        
        p_total_real = p_real.sum(dim=1)
        p_total_imag = p_imag.sum(dim=1)
        p_mag_sq = p_total_real**2 + p_total_imag**2
        
        particle_radius = 0.0015
        V0 = (4/3) * np.pi * particle_radius**3
        particle_density = 84.0
        f1 = 1 - (AIR_DENSITY / particle_density)
        
        U = -V0 * (f1 / (2 * AIR_DENSITY * SPEED_OF_SOUND**2)) * p_mag_sq
        
        return U
    
    def optimize_from_fol(self, iterations=500, learning_rate=0.0003):
        """
        Optimize starting from FoL with hard-shell constraints
        
        Strategy:
        - Start at perfect FoL
        - Use gradient descent to find better positions
        - Project back onto valid space after each step
        - Never allow collisions
        """
        print("🌸 HARD-SHELL OPTIMIZATION FROM FLOWER OF LIFE")
        print()
        print(f"📏 HARD CONSTRAINTS:")
        print(f"   Transducer diameter: {TRANSDUCER_DIAMETER*1000:.1f}mm")
        print(f"   Min spacing: {MIN_SPACING*1000:.1f}mm")
        print(f"   Max perturbation: {MAX_PERTURBATION*1000:.1f}mm from FoL")
        print()
        
        # Start from perfect FoL
        positions = self.fol_reference.clone()
        positions.requires_grad = True
        
        # Evaluate baseline
        fol_metrics = self.calculate_field_quality(self.fol_reference)
        fol_collision, fol_min_dist = self.check_hard_shell_collision(self.fol_reference)
        
        print(f"📊 BASELINE (Perfect FoL):")
        print(f"   Well depth: {fol_metrics['well_depth']*1e6:.2f} µJ")
        print(f"   Symmetry score: {fol_metrics['symmetry']:.2f}")
        print(f"   Uniformity: {fol_metrics['uniformity']:.2f}")
        print(f"   Total score: {fol_metrics['total_score']:.2f}")
        print(f"   Min spacing: {fol_min_dist*1000:.2f}mm")
        print(f"   Collisions: {'✗ YES' if fol_collision else '✓ NONE'}")
        print()
        
        optimizer = optim.Adam([positions], lr=learning_rate)
        
        best_score = fol_metrics['total_score']
        best_positions = self.fol_reference.clone()
        iterations_since_improvement = 0
        
        start_time = time.time()
        
        print("Starting optimization...")
        print()
        
        for i in range(iterations):
            optimizer.zero_grad()
            
            # Calculate potential field (keep as tensor for gradients!)
            grid_size = 80
            extent = 0.06
            
            x = torch.linspace(-extent, extent, grid_size, device=self.device)
            y = torch.linspace(-extent, extent, grid_size, device=self.device)
            X, Y = torch.meshgrid(x, y, indexing='ij')
            Z = torch.full_like(X, 0.005)
            
            grid_points = torch.stack([X.ravel(), Y.ravel(), Z.ravel()], dim=1)
            emitters_3d = torch.cat([positions, 
                                    torch.zeros(self.n_emitters, 1, device=self.device)], 
                                   dim=1)
            
            U = self._calculate_potential(grid_points, emitters_3d)
            
            # Well depth (kept as tensor!)
            well_depth_tensor = U.max() - U.min()
            
            # Maximize well depth (negative for minimization)
            loss = -well_depth_tensor
            
            # Backprop
            loss.backward()
            optimizer.step()
            
            # Calculate full metrics for display (can be float)
            with torch.no_grad():
                metrics = self.calculate_field_quality(positions)
            
            # PROJECT BACK ONTO VALID SPACE (hard-shell enforcement)
            with torch.no_grad():
                # Clip to max perturbation from FoL
                deviations = positions - self.fol_reference
                deviation_mags = torch.sqrt(torch.sum(deviations**2, dim=1, keepdim=True))
                scale = torch.clamp(deviation_mags / MAX_PERTURBATION, max=1.0)
                positions.data = self.fol_reference + deviations * scale
                
                # Push apart if too close (hard-shell repair)
                for _ in range(5):  # Multiple passes
                    moved = False
                    for j in range(self.n_emitters):
                        for k in range(j + 1, self.n_emitters):
                            dist = torch.sqrt(torch.sum((positions[j] - positions[k])**2))
                            
                            if dist < MIN_SPACING:
                                # Push apart along connecting line
                                direction = (positions[j] - positions[k]) / (dist + 1e-6)
                                push = (MIN_SPACING - dist) / 2
                                positions[j] += direction * push
                                positions[k] -= direction * push
                                moved = True
                    
                    if not moved:
                        break
            
            # Check validity
            collision, min_dist = self.check_hard_shell_collision(positions)
            exceeded, max_dev = self.check_perturbation_limit(positions)
            
            # Update best if valid and better
            if not collision and not exceeded:
                current_score = metrics['total_score']
                
                if current_score > best_score:
                    best_score = current_score
                    best_positions = positions.clone().detach()
                    iterations_since_improvement = 0
                    
                    improvement = ((best_score - fol_metrics['total_score']) / 
                                 fol_metrics['total_score']) * 100
                    
                    print(f"✨ Iter {i}: NEW BEST! Score: {best_score:.2f} "
                          f"({improvement:+.2f}% vs FoL)")
                    print(f"   Well: {metrics['well_depth']*1e6:.2f}µJ | "
                          f"Sym: {metrics['symmetry']:.2f} | "
                          f"Uni: {metrics['uniformity']:.2f}")
                    print(f"   Min spacing: {min_dist*1000:.2f}mm | "
                          f"Max dev: {max_dev*1000:.2f}mm")
                else:
                    iterations_since_improvement += 1
            else:
                iterations_since_improvement += 1
            
            # Progress
            if i % 100 == 0 and i > 0:
                print(f"Iter {i}/{iterations} | Best: {best_score:.2f} | "
                      f"Collision: {'YES' if collision else 'NO'} | "
                      f"Since improve: {iterations_since_improvement}")
            
            # History
            self.history.append({
                'iteration': i,
                'score': metrics['total_score'],
                'well_depth': metrics['well_depth'],
                'valid': not collision and not exceeded,
                'best_score': best_score
            })
            
            # Early stopping
            if iterations_since_improvement > 150:
                print(f"\n⏹️  Early stopping at iteration {i}")
                break
        
        total_time = time.time() - start_time
        
        # Final evaluation
        final_metrics = self.calculate_field_quality(best_positions)
        final_collision, final_min_dist = self.check_hard_shell_collision(best_positions)
        
        print()
        print("=" * 80)
        print("🏆 OPTIMIZATION COMPLETE!")
        print("=" * 80)
        print(f"Total time: {total_time:.1f} seconds")
        print()
        print(f"PERFECT FOL:")
        print(f"  Score: {fol_metrics['total_score']:.2f}")
        print(f"  Well depth: {fol_metrics['well_depth']*1e6:.2f} µJ")
        print()
        print(f"OPTIMIZED (AI-Tuned FoL):")
        print(f"  Score: {final_metrics['total_score']:.2f}")
        print(f"  Well depth: {final_metrics['well_depth']*1e6:.2f} µJ")
        print(f"  Min spacing: {final_min_dist*1000:.2f}mm ✓")
        print(f"  Collisions: {'✗ INVALID' if final_collision else '✓ NONE'}")
        print()
        
        improvement = ((final_metrics['total_score'] - fol_metrics['total_score']) / 
                      fol_metrics['total_score']) * 100
        
        print(f"Improvement: {improvement:+.2f}%")
        print()
        
        if improvement > 1:
            print("🎉 AI found improvements by tuning sacred geometry!")
        elif improvement > -1:
            print("🌸 FoL is essentially optimal - AI confirms ancient wisdom!")
        else:
            print("🌸 Perfect FoL remains superior!")
        
        return best_positions, final_metrics
    
    def visualize_results(self, optimized_positions, filename='hardshell_optimization.png'):
        """Visualize FoL vs optimized"""
        fig, axes = plt.subplots(1, 3, figsize=(24, 8))
        
        fol_pos = self.fol_reference.cpu().numpy()
        opt_pos = optimized_positions.cpu().numpy()
        
        # Plot 1: Perfect FoL with hard-shell circles
        ax = axes[0]
        
        for pos in fol_pos:
            circle = Circle((pos[0]*1000, pos[1]*1000), TRANSDUCER_DIAMETER*1000/2,
                          fill=True, facecolor='lightgreen', alpha=0.3,
                          edgecolor='green', linewidth=2)
            ax.add_patch(circle)
        
        ax.scatter(fol_pos[:, 0]*1000, fol_pos[:, 1]*1000,
                  c='#00ff88', s=400, marker='o', edgecolors='white', linewidths=3,
                  label='Perfect FoL', zorder=10)
        
        # Draw rings
        r1 = 2.5 * self.wavelength * 1000
        r2 = 5.0 * self.wavelength * 1000
        circle1 = Circle((0, 0), r1, fill=False, edgecolor='cyan', 
                        linewidth=2, linestyle='--', alpha=0.5)
        circle2 = Circle((0, 0), r2, fill=False, edgecolor='cyan',
                        linewidth=2, linestyle='--', alpha=0.5)
        ax.add_patch(circle1)
        ax.add_patch(circle2)
        
        ax.set_xlabel('X (mm)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Y (mm)', fontsize=14, fontweight='bold')
        ax.set_title('Perfect Flower of Life\n(Sacred Geometry Baseline)', 
                    fontsize=16, fontweight='bold')
        ax.set_aspect('equal')
        ax.grid(alpha=0.3)
        ax.legend(fontsize=12)
        ax.set_xlim(-80, 80)
        ax.set_ylim(-80, 80)
        
        # Plot 2: AI-Optimized with deviations shown
        ax = axes[1]
        
        for pos in opt_pos:
            circle = Circle((pos[0]*1000, pos[1]*1000), TRANSDUCER_DIAMETER*1000/2,
                          fill=True, facecolor='lightblue', alpha=0.3,
                          edgecolor='blue', linewidth=2)
            ax.add_patch(circle)
        
        # Show deviation vectors
        for i in range(self.n_emitters):
            ax.arrow(fol_pos[i, 0]*1000, fol_pos[i, 1]*1000,
                    (opt_pos[i, 0] - fol_pos[i, 0])*1000,
                    (opt_pos[i, 1] - fol_pos[i, 1])*1000,
                    head_width=2, head_length=1, fc='red', ec='red',
                    alpha=0.6, linewidth=1.5)
        
        ax.scatter(opt_pos[:, 0]*1000, opt_pos[:, 1]*1000,
                  c='#ff00ff', s=400, marker='D', edgecolors='white', linewidths=3,
                  label='AI-Tuned', zorder=10)
        
        ax.set_xlabel('X (mm)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Y (mm)', fontsize=14, fontweight='bold')
        ax.set_title('AI-Tuned Geometry\n(Optimized from FoL)', 
                    fontsize=16, fontweight='bold')
        ax.set_aspect('equal')
        ax.grid(alpha=0.3)
        ax.legend(fontsize=12)
        ax.set_xlim(-80, 80)
        ax.set_ylim(-80, 80)
        
        # Plot 3: Overlay comparison
        ax = axes[2]
        
        ax.scatter(fol_pos[:, 0]*1000, fol_pos[:, 1]*1000,
                  c='#00ff88', s=400, marker='o', edgecolors='white', linewidths=2,
                  label='Perfect FoL', alpha=0.5, zorder=5)
        
        ax.scatter(opt_pos[:, 0]*1000, opt_pos[:, 1]*1000,
                  c='#ff00ff', s=400, marker='D', edgecolors='white', linewidths=3,
                  label='AI-Tuned', alpha=0.8, zorder=10)
        
        # Connect corresponding points
        for i in range(self.n_emitters):
            ax.plot([fol_pos[i, 0]*1000, opt_pos[i, 0]*1000],
                   [fol_pos[i, 1]*1000, opt_pos[i, 1]*1000],
                   'r--', alpha=0.3, linewidth=1)
        
        ax.set_xlabel('X (mm)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Y (mm)', fontsize=14, fontweight='bold')
        ax.set_title('Direct Comparison\n(Red lines show AI adjustments)', 
                    fontsize=16, fontweight='bold')
        ax.set_aspect('equal')
        ax.grid(alpha=0.3)
        ax.legend(fontsize=12)
        ax.set_xlim(-80, 80)
        ax.set_ylim(-80, 80)
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✓ Saved visualization: {filename}")
        
        return fig
    
    def save_results(self, positions, metrics, filename='hardshell_results.json'):
        """Save results"""
        collision, min_dist = self.check_hard_shell_collision(positions)
        exceeded, max_dev = self.check_perturbation_limit(positions)
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'gpu': gpu_name,
            'n_emitters': self.n_emitters,
            'frequency': self.frequency,
            'constraints': {
                'transducer_diameter_mm': TRANSDUCER_DIAMETER * 1000,
                'min_spacing_mm': MIN_SPACING * 1000,
                'max_perturbation_mm': MAX_PERTURBATION * 1000
            },
            'perfect_fol': {
                'positions': self.fol_reference.cpu().numpy().tolist()
            },
            'optimized': {
                'positions': positions.cpu().numpy().tolist(),
                'metrics': metrics,
                'min_distance_mm': min_dist * 1000,
                'max_deviation_mm': max_dev * 1000,
                'valid': not collision and not exceeded
            },
            'history': self.history
        }
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"✓ Saved results: {filename}")

def main():
    """Run hard-shell optimization"""
    print("=" * 80)
    print("AXIOM OF PHYSICAL CHOICE - IMPLEMENTATION")
    print("=" * 80)
    print()
    print("We start from nature's choice (Flower of Life)")
    print("and let AI tune it within physical reality.")
    print()
    
    optimizer = HardShellOptimizer(n_emitters=19, device=device)
    
    positions, metrics = optimizer.optimize_from_fol(
        iterations=500,
        learning_rate=0.0003
    )
    
    print()
    print("📊 Creating visualizations...")
    optimizer.visualize_results(positions)
    
    print()
    print("💾 Saving results...")
    optimizer.save_results(positions, metrics)
    
    print()
    print("=" * 80)
    print("✅ HARD-SHELL OPTIMIZATION COMPLETE!")
    print("=" * 80)
    print()
    print("Files created:")
    print("  • hardshell_optimization.png - Visual comparison")
    print("  • hardshell_results.json - Full data")
    print()
    print("🎥 Ready for the ultimate video!")
    print()

if __name__ == '__main__':
    main()
