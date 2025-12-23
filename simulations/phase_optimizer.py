"""
🎵 PHASE-ONLY FLOWER OF LIFE OPTIMIZER 🎵
==========================================

Can AI beat Flower of Life by optimizing PHASES only?

This optimizer:
✓ Locks positions to perfect Flower of Life
✓ Optimizes only phase angles (0-2π per emitter)
✓ Tests if clever phase tuning can improve trap strength
✓ Compares against symmetric phases (all in-phase)

Why this matters:
- Positions are hard to change (physical mounting)
- Phases are easy to control (driver boards)
- If AI can't improve with free phases → FoL is truly optimal

Expected result: AI will find symmetric phases similar to all-in-phase,
proving geometry + symmetric phases = optimal solution.

Authors: Sportysport & Claude (Anthropic)
License: MIT
"""

import numpy as np
import torch
import torch.optim as optim
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
import json
import time
from datetime import datetime

print("=" * 80)
print("🎵 PHASE-ONLY FLOWER OF LIFE OPTIMIZER")
print("=" * 80)
print()
print("Positions locked to FoL. Can AI find better phases?")
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

class PhaseOnlyOptimizer:
    """Optimize phases while positions stay fixed to FoL"""
    
    def __init__(self, n_emitters=19, frequency=40000.0, device='cuda'):
        self.device = device
        self.n_emitters = n_emitters
        self.frequency = frequency
        self.wavelength = 343.0 / frequency
        
        # Get FIXED FoL positions (these NEVER change)
        self.fol_positions = self._get_perfect_fol()
        
        self.history = []
        
    def _get_perfect_fol(self):
        """Get mathematically perfect Flower of Life (FIXED)"""
        r1 = 2.5 * self.wavelength
        r2 = 5.0 * self.wavelength
        
        positions = [[0, 0]]
        
        # Ring 1: 6 emitters
        for i in range(6):
            theta = i * np.pi / 3
            positions.append([r1 * np.cos(theta), r1 * np.sin(theta)])
        
        # Ring 2: 12 emitters
        for i in range(12):
            theta = i * np.pi / 6
            positions.append([r2 * np.cos(theta), r2 * np.sin(theta)])
        
        return torch.tensor(positions[:self.n_emitters], 
                          dtype=torch.float32, device=self.device)
    
    def calculate_field_quality(self, phases):
        """
        Calculate field metrics with given phases
        Positions are LOCKED to FoL!
        """
        # Evaluation grid
        grid_size = 80
        extent = 0.06
        
        x = torch.linspace(-extent, extent, grid_size, device=self.device)
        y = torch.linspace(-extent, extent, grid_size, device=self.device)
        X, Y = torch.meshgrid(x, y, indexing='ij')
        Z = torch.full_like(X, 0.005)
        
        grid_points = torch.stack([X.ravel(), Y.ravel(), Z.ravel()], dim=1)
        
        # Add z=0 to fixed positions
        emitters_3d = torch.cat([self.fol_positions, 
                                torch.zeros(self.n_emitters, 1, device=self.device)], 
                               dim=1)
        
        # Calculate potential with these phases
        U = self._calculate_potential(grid_points, emitters_3d, phases)
        U_grid = U.reshape(X.shape)
        
        # Well depth
        well_depth = (U.max() - U.min()).item()
        
        # Toroidal symmetry
        r_grid = torch.sqrt(X**2 + Y**2)
        
        radii = [0.01, 0.02, 0.03, 0.04]
        symmetry_score = 0
        
        for r in radii:
            mask = (r_grid > r - 0.002) & (r_grid < r + 0.002)
            if mask.sum() > 0:
                ring_values = U_grid[mask]
                ring_std = ring_values.std().item()
                symmetry_score += 1.0 / (ring_std + 1e-6)
        
        symmetry_score /= len(radii)
        
        # Count trap points (local minima)
        U_np = U_grid.cpu().numpy()
        
        # Simple trap detection: points significantly below mean
        threshold = U_np.min() + 0.2 * (U_np.max() - U_np.min())
        trap_mask = U_np < threshold
        
        # Rough count (connected regions would be better, but this is fast)
        n_traps = trap_mask.sum()
        
        return {
            'well_depth': well_depth,
            'symmetry': symmetry_score,
            'n_traps': n_traps,
            'total_score': well_depth * 1e6 + symmetry_score * 1000
        }
    
    def _calculate_potential(self, points, emitters, phases):
        """Calculate Gor'kov potential with phases"""
        k = 2 * np.pi / self.wavelength
        
        pts = points.unsqueeze(1)
        ems = emitters.unsqueeze(0)
        
        r = torch.sqrt(torch.sum((pts - ems)**2, dim=2))
        r = torch.clamp(r, min=1e-6)
        
        # Expand phases for broadcasting
        phases_expanded = phases.unsqueeze(0)
        
        pressure_amp = 1000.0
        p_real = (pressure_amp / r) * torch.cos(k * r + phases_expanded)
        p_imag = (pressure_amp / r) * torch.sin(k * r + phases_expanded)
        
        p_total_real = p_real.sum(dim=1)
        p_total_imag = p_imag.sum(dim=1)
        p_mag_sq = p_total_real**2 + p_total_imag**2
        
        particle_radius = 0.0015
        V0 = (4/3) * np.pi * particle_radius**3
        particle_density = 84.0
        f1 = 1 - (AIR_DENSITY / particle_density)
        
        U = -V0 * (f1 / (2 * AIR_DENSITY * SPEED_OF_SOUND**2)) * p_mag_sq
        
        return U
    
    def optimize_phases(self, iterations=500, learning_rate=0.01):
        """
        Optimize phases while positions stay LOCKED to FoL
        """
        print("🎵 PHASE-ONLY OPTIMIZATION")
        print()
        print(f"📏 CONSTRAINTS:")
        print(f"   Positions: LOCKED to perfect Flower of Life")
        print(f"   Phases: FREE (0-2π per emitter)")
        print(f"   Emitters: {self.n_emitters}")
        print()
        
        # Baseline: All phases = 0 (symmetric, all in-phase)
        symmetric_phases = torch.zeros(self.n_emitters, device=self.device)
        symmetric_metrics = self.calculate_field_quality(symmetric_phases)
        
        print(f"📊 BASELINE (All In-Phase):")
        print(f"   Well depth: {symmetric_metrics['well_depth']*1e6:.2f} µJ")
        print(f"   Symmetry score: {symmetric_metrics['symmetry']:.2f}")
        print(f"   Trap points: {symmetric_metrics['n_traps']}")
        print(f"   Total score: {symmetric_metrics['total_score']:.2f}")
        print()
        
        # Start from random phases
        phases = torch.rand(self.n_emitters, device=self.device) * 2 * np.pi
        phases.requires_grad = True
        
        optimizer = optim.Adam([phases], lr=learning_rate)
        
        best_score = symmetric_metrics['total_score']
        best_phases = symmetric_phases.clone()
        iterations_since_improvement = 0
        
        start_time = time.time()
        
        print("Starting phase optimization...")
        print()
        
        for i in range(iterations):
            optimizer.zero_grad()
            
            # Normalize phases to [0, 2π]
            with torch.no_grad():
                phases.data = torch.fmod(phases.data, 2 * np.pi)
                phases.data = torch.where(phases.data < 0, 
                                         phases.data + 2 * np.pi, 
                                         phases.data)
            
            # Calculate field (positions locked!)
            grid_size = 80
            extent = 0.06
            
            x = torch.linspace(-extent, extent, grid_size, device=self.device)
            y = torch.linspace(-extent, extent, grid_size, device=self.device)
            X, Y = torch.meshgrid(x, y, indexing='ij')
            Z = torch.full_like(X, 0.005)
            
            grid_points = torch.stack([X.ravel(), Y.ravel(), Z.ravel()], dim=1)
            emitters_3d = torch.cat([self.fol_positions, 
                                    torch.zeros(self.n_emitters, 1, device=self.device)], 
                                   dim=1)
            
            U = self._calculate_potential(grid_points, emitters_3d, phases)
            
            # Well depth (kept as tensor)
            well_depth_tensor = U.max() - U.min()
            
            # Maximize well depth
            loss = -well_depth_tensor
            
            # Backprop
            loss.backward()
            optimizer.step()
            
            # Calculate full metrics for display
            with torch.no_grad():
                metrics = self.calculate_field_quality(phases)
            
            # Update best
            current_score = metrics['total_score']
            
            if current_score > best_score:
                best_score = current_score
                best_phases = phases.clone().detach()
                iterations_since_improvement = 0
                
                improvement = ((best_score - symmetric_metrics['total_score']) / 
                             symmetric_metrics['total_score']) * 100
                
                print(f"✨ Iter {i}: NEW BEST! Score: {best_score:.2f} "
                      f"({improvement:+.2f}% vs symmetric)")
                print(f"   Well: {metrics['well_depth']*1e6:.2f}µJ | "
                      f"Sym: {metrics['symmetry']:.2f} | "
                      f"Traps: {metrics['n_traps']}")
            else:
                iterations_since_improvement += 1
            
            # Progress
            if i % 100 == 0 and i > 0:
                print(f"Iter {i}/{iterations} | Best: {best_score:.2f} | "
                      f"Since improve: {iterations_since_improvement}")
            
            # History
            self.history.append({
                'iteration': i,
                'score': current_score,
                'well_depth': metrics['well_depth'],
                'best_score': best_score
            })
            
            # Early stopping
            if iterations_since_improvement > 150:
                print(f"\n⏹️  Early stopping at iteration {i}")
                break
        
        total_time = time.time() - start_time
        
        # Final evaluation
        final_metrics = self.calculate_field_quality(best_phases)
        
        print()
        print("=" * 80)
        print("🏆 PHASE OPTIMIZATION COMPLETE!")
        print("=" * 80)
        print(f"Total time: {total_time:.1f} seconds")
        print()
        print(f"SYMMETRIC (All In-Phase):")
        print(f"  Score: {symmetric_metrics['total_score']:.2f}")
        print(f"  Well depth: {symmetric_metrics['well_depth']*1e6:.2f} µJ")
        print()
        print(f"OPTIMIZED (AI-Tuned Phases):")
        print(f"  Score: {final_metrics['total_score']:.2f}")
        print(f"  Well depth: {final_metrics['well_depth']*1e6:.2f} µJ")
        print()
        
        improvement = ((final_metrics['total_score'] - symmetric_metrics['total_score']) / 
                      symmetric_metrics['total_score']) * 100
        
        print(f"Improvement: {improvement:+.2f}%")
        print()
        
        if improvement > 5:
            print("🎉 AI found significant phase improvements!")
        elif improvement > 0:
            print("🎵 AI found minor phase tuning (~symmetric still best)")
        else:
            print("🌸 Symmetric phases remain optimal!")
        
        return best_phases, final_metrics, symmetric_metrics
    
    def visualize_results(self, optimized_phases, opt_metrics, sym_metrics, 
                         filename='phase_optimization_results.png'):
        """Visualize phase optimization results"""
        
        symmetric_phases = torch.zeros(self.n_emitters, device=self.device)
        
        fig = plt.figure(figsize=(20, 10))
        gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
        
        # Plot 1: FoL positions with phase arrows (symmetric)
        ax1 = fig.add_subplot(gs[0, 0])
        self._plot_phases(ax1, symmetric_phases, "Symmetric Phases (All In-Phase)")
        
        # Plot 2: FoL positions with phase arrows (optimized)
        ax2 = fig.add_subplot(gs[0, 1])
        self._plot_phases(ax2, optimized_phases, "AI-Optimized Phases")
        
        # Plot 3: Phase comparison plot
        ax3 = fig.add_subplot(gs[0, 2])
        self._plot_phase_comparison(ax3, symmetric_phases, optimized_phases)
        
        # Plot 4: Field comparison (symmetric)
        ax4 = fig.add_subplot(gs[1, 0])
        self._plot_field(ax4, symmetric_phases, "Symmetric Field")
        
        # Plot 5: Field comparison (optimized)
        ax5 = fig.add_subplot(gs[1, 1])
        self._plot_field(ax5, optimized_phases, "Optimized Field")
        
        # Plot 6: Optimization history
        ax6 = fig.add_subplot(gs[1, 2])
        self._plot_history(ax6, sym_metrics)
        
        plt.suptitle('Phase-Only Optimization: Can AI Beat Symmetric Phases?', 
                    fontsize=18, fontweight='bold', y=0.98)
        
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✓ Saved visualization: {filename}")
        
        return fig
    
    def _plot_phases(self, ax, phases, title):
        """Plot emitters with phase arrows"""
        pos = self.fol_positions.cpu().numpy()
        phases_np = phases.cpu().numpy()
        
        # Draw emitters
        ax.scatter(pos[:, 0]*1000, pos[:, 1]*1000,
                  s=400, c='lightblue', edgecolors='black', linewidths=2,
                  zorder=5)
        
        # Draw phase arrows
        for i in range(self.n_emitters):
            # Arrow pointing in phase direction
            angle = phases_np[i]
            length = 8  # mm
            dx = length * np.cos(angle)
            dy = length * np.sin(angle)
            
            arrow = FancyArrowPatch(
                (pos[i, 0]*1000, pos[i, 1]*1000),
                (pos[i, 0]*1000 + dx, pos[i, 1]*1000 + dy),
                arrowstyle='->', mutation_scale=20, linewidth=2,
                color='red', zorder=10
            )
            ax.add_patch(arrow)
            
            # Label with phase value
            ax.text(pos[i, 0]*1000, pos[i, 1]*1000 - 12,
                   f'{angle:.2f}', ha='center', fontsize=8,
                   bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
        
        ax.set_xlabel('X (mm)', fontweight='bold')
        ax.set_ylabel('Y (mm)', fontweight='bold')
        ax.set_title(title, fontweight='bold')
        ax.set_aspect('equal')
        ax.grid(alpha=0.3)
        ax.set_xlim(-60, 60)
        ax.set_ylim(-60, 60)
    
    def _plot_phase_comparison(self, ax, sym_phases, opt_phases):
        """Plot phase values comparison"""
        sym_np = sym_phases.cpu().numpy()
        opt_np = opt_phases.cpu().numpy()
        
        x = np.arange(self.n_emitters)
        width = 0.35
        
        ax.bar(x - width/2, sym_np, width, label='Symmetric', alpha=0.8)
        ax.bar(x + width/2, opt_np, width, label='Optimized', alpha=0.8)
        
        ax.set_xlabel('Emitter Index', fontweight='bold')
        ax.set_ylabel('Phase (radians)', fontweight='bold')
        ax.set_title('Phase Values Comparison', fontweight='bold')
        ax.legend()
        ax.grid(alpha=0.3, axis='y')
        ax.set_ylim(0, 2*np.pi)
        ax.axhline(y=np.pi, color='r', linestyle='--', alpha=0.3)
    
    def _plot_field(self, ax, phases, title):
        """Plot acoustic field"""
        grid_size = 100
        extent = 0.05
        
        x = np.linspace(-extent, extent, grid_size)
        y = np.linspace(-extent, extent, grid_size)
        X, Y = np.meshgrid(x, y)
        
        grid_points = np.stack([X.ravel(), Y.ravel(), np.full(grid_size**2, 0.005)], axis=1)
        grid_tensor = torch.tensor(grid_points, dtype=torch.float32, device=self.device)
        
        emitters_3d = torch.cat([self.fol_positions,
                                torch.zeros(self.n_emitters, 1, device=self.device)],
                               dim=1)
        
        U = self._calculate_potential(grid_tensor, emitters_3d, phases)
        U_grid = U.cpu().numpy().reshape(X.shape) * 1e6
        
        im = ax.contourf(X*1000, Y*1000, U_grid, levels=50, cmap='RdYlBu_r')
        plt.colorbar(im, ax=ax, label='Potential (µJ)')
        
        pos = self.fol_positions.cpu().numpy()
        ax.scatter(pos[:, 0]*1000, pos[:, 1]*1000,
                  c='black', s=50, edgecolors='white', linewidths=1, zorder=10)
        
        ax.set_xlabel('X (mm)', fontweight='bold')
        ax.set_ylabel('Y (mm)', fontweight='bold')
        ax.set_title(title, fontweight='bold')
        ax.set_aspect('equal')
    
    def _plot_history(self, ax, sym_metrics):
        """Plot optimization history"""
        if not self.history:
            return
        
        iterations = [h['iteration'] for h in self.history]
        scores = [h['score'] for h in self.history]
        best_scores = [h['best_score'] for h in self.history]
        
        ax.plot(iterations, scores, alpha=0.3, label='Current')
        ax.plot(iterations, best_scores, linewidth=2, label='Best')
        ax.axhline(y=sym_metrics['total_score'], color='r', linestyle='--',
                  linewidth=2, label='Symmetric Baseline')
        
        ax.set_xlabel('Iteration', fontweight='bold')
        ax.set_ylabel('Score', fontweight='bold')
        ax.set_title('Optimization Progress', fontweight='bold')
        ax.legend()
        ax.grid(alpha=0.3)
    
    def save_results(self, phases, metrics, sym_metrics, filename='phase_optimization_results.json'):
        """Save results"""
        # Convert numpy types to Python types for JSON
        def convert_to_python(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {k: convert_to_python(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_to_python(item) for item in obj]
            elif isinstance(obj, torch.Tensor):
                return obj.cpu().tolist()
            return obj
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'gpu': gpu_name,
            'n_emitters': self.n_emitters,
            'frequency': self.frequency,
            'symmetric_phases': {
                'phases': torch.zeros(self.n_emitters).tolist(),
                'metrics': convert_to_python(sym_metrics)
            },
            'optimized_phases': {
                'phases': phases.cpu().tolist(),
                'metrics': convert_to_python(metrics)
            },
            'improvement_percent': ((metrics['total_score'] - sym_metrics['total_score']) / 
                                   sym_metrics['total_score']) * 100,
            'history': convert_to_python(self.history)
        }
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"✓ Saved results: {filename}")

def main():
    """Run phase-only optimization"""
    print("=" * 80)
    print("TESTING: Can AI beat FoL with optimized phases?")
    print("=" * 80)
    print()
    
    optimizer = PhaseOnlyOptimizer(n_emitters=19, device=device)
    
    phases, opt_metrics, sym_metrics = optimizer.optimize_phases(
        iterations=500,
        learning_rate=0.01
    )
    
    print()
    print("📊 Creating visualizations...")
    optimizer.visualize_results(phases, opt_metrics, sym_metrics)
    
    print()
    print("💾 Saving results...")
    optimizer.save_results(phases, opt_metrics, sym_metrics)
    
    print()
    print("=" * 80)
    print("✅ PHASE OPTIMIZATION COMPLETE!")
    print("=" * 80)
    print()
    print("Files created:")
    print("  • phase_optimization_results.png - Visual comparison")
    print("  • phase_optimization_results.json - Full data")
    print()
    print("🎥 Ready for Part 4 video!")
    print()

if __name__ == '__main__':
    main()
