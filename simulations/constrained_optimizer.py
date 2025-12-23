"""
🧠 CONSTRAINED NEURAL NETWORK GEOMETRY OPTIMIZER 🧠
====================================================

NOW WITH PHYSICAL CONSTRAINTS!

This prevents AI from "cheating" by clustering emitters.

Constraints:
✓ Minimum spacing: 5mm between any two emitters
✓ Maximum spread: 60mm from center
✓ Physical realizability enforced!

Perfect for finding REAL optimal geometries!

Authors: Sportysport & Claude (Anthropic)
License: MIT
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import json
import time
from datetime import datetime

print("=" * 80)
print("🧠 CONSTRAINED NEURAL NETWORK GEOMETRY OPTIMIZER")
print("=" * 80)
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
SPEED_OF_SOUND = torch.tensor(343.0, device=device)
AIR_DENSITY = torch.tensor(1.225, device=device)

# CONSTRAINTS
MIN_SPACING = 0.005  # 5mm minimum between emitters
MAX_SPREAD = 0.060   # 60mm maximum from center
CONSTRAINT_PENALTY = 1e6  # Heavy penalty for violations

class ConstrainedOptimizer:
    """Geometry optimizer with physical constraints"""
    
    def __init__(self, n_emitters=7, frequency=40000.0, device='cuda'):
        self.device = device
        self.n_emitters = n_emitters
        self.frequency = frequency
        self.wavelength = 343.0 / frequency
        
        self.best_geometries = []
        self.history = []
        
        # Constraint violation tracking
        self.constraint_violations = []
        
    def check_constraints(self, positions):
        """
        Check if geometry satisfies physical constraints
        
        Returns:
            valid (bool): True if all constraints satisfied
            penalty (float): Penalty value for violations
        """
        batch_size = positions.shape[0] if len(positions.shape) == 3 else 1
        
        if len(positions.shape) == 2:
            positions = positions.unsqueeze(0)
        
        total_penalty = torch.zeros(batch_size, device=self.device)
        
        for b in range(batch_size):
            pos = positions[b]  # (n_emitters, 2)
            
            # Constraint 1: Minimum spacing between emitters
            for i in range(self.n_emitters):
                for j in range(i + 1, self.n_emitters):
                    dist = torch.sqrt(torch.sum((pos[i] - pos[j])**2))
                    
                    if dist < MIN_SPACING:
                        violation = MIN_SPACING - dist
                        total_penalty[b] += CONSTRAINT_PENALTY * violation
            
            # Constraint 2: Maximum spread from center
            distances_from_center = torch.sqrt(torch.sum(pos**2, dim=1))
            max_dist = distances_from_center.max()
            
            if max_dist > MAX_SPREAD:
                violation = max_dist - MAX_SPREAD
                total_penalty[b] += CONSTRAINT_PENALTY * violation
        
        valid = (total_penalty == 0).all()
        
        if batch_size == 1:
            return valid.item(), total_penalty[0].item()
        return valid, total_penalty
    
    def calculate_well_depth_batch(self, positions_batch):
        """Calculate well depth with constraint penalties"""
        batch_size = positions_batch.shape[0]
        
        # Evaluation grid
        grid_size = 50
        extent = 0.04
        x = torch.linspace(-extent, extent, grid_size, device=self.device)
        y = torch.linspace(-extent, extent, grid_size, device=self.device)
        X, Y = torch.meshgrid(x, y, indexing='ij')
        
        grid_points = torch.stack([X.ravel(), Y.ravel()], dim=1)
        n_points = grid_points.shape[0]
        
        well_depths = []
        
        for b in range(batch_size):
            emitters = positions_batch[b]
            
            # Add z=0
            emitters_3d = torch.cat([emitters, torch.zeros(self.n_emitters, 1, device=self.device)], dim=1)
            
            # Grid with z=5mm
            z = torch.full((n_points, 1), 0.005, device=self.device)
            points_3d = torch.cat([grid_points, z], dim=1)
            
            # Calculate potential
            U = self._calculate_potential(points_3d, emitters_3d)
            
            # Well depth
            well_depth = (U.max() - U.min()).item()
            well_depths.append(well_depth)
        
        well_depths = torch.tensor(well_depths, device=self.device)
        
        # Apply constraint penalties
        _, penalties = self.check_constraints(positions_batch)
        
        # Subtract penalty from well depth (lower is worse)
        constrained_depths = well_depths - penalties
        
        return constrained_depths
    
    def _calculate_potential(self, points, emitters):
        """Calculate Gor'kov potential"""
        k = 2 * torch.pi / self.wavelength
        
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
        V0 = (4/3) * torch.pi * particle_radius**3
        particle_density = 84.0
        f1 = 1 - (AIR_DENSITY / particle_density)
        
        U = -V0 * (f1 / (2 * AIR_DENSITY * SPEED_OF_SOUND**2)) * p_mag_sq
        
        return U
    
    def run_constrained_evolutionary(self, generations=1000, population_size=150):
        """
        Evolutionary optimization with physical constraints
        """
        print(f"🧬 CONSTRAINED EVOLUTIONARY OPTIMIZATION")
        print(f"   Generations: {generations}")
        print(f"   Population: {population_size}")
        print(f"   Emitters: {self.n_emitters}")
        print()
        print(f"📏 CONSTRAINTS:")
        print(f"   Min spacing: {MIN_SPACING*1000:.1f}mm between emitters")
        print(f"   Max spread: {MAX_SPREAD*1000:.1f}mm from center")
        print()
        
        # Initialize population with valid geometries
        population = self._initialize_valid_population(population_size)
        
        # Baseline: Flower of Life
        fol_positions = self._get_fol_geometry()
        fol_depth = self.calculate_well_depth_batch(fol_positions.unsqueeze(0))[0].item()
        fol_valid, _ = self.check_constraints(fol_positions)
        
        print(f"📊 Baseline (Flower of Life):")
        print(f"   Well depth: {fol_depth*1e6:.2f} µJ")
        print(f"   Constraints: {'✓ VALID' if fol_valid else '✗ INVALID'}")
        print()
        
        best_ever = fol_depth
        best_ever_positions = fol_positions.clone()
        generations_since_improvement = 0
        
        start_time = time.time()
        
        for gen in range(generations):
            # Evaluate fitness
            fitness = self.calculate_well_depth_batch(population)
            
            # Find best VALID geometry
            valid_mask = []
            for i in range(population_size):
                valid, _ = self.check_constraints(population[i])
                valid_mask.append(valid)
            
            valid_mask = torch.tensor(valid_mask, device=self.device)
            
            if valid_mask.any():
                valid_fitness = fitness.clone()
                valid_fitness[~valid_mask] = -1e10  # Mask invalid
                
                best_idx = valid_fitness.argmax()
                best_depth = fitness[best_idx].item()
                best_is_valid = valid_mask[best_idx].item()
                
                if best_is_valid and best_depth > best_ever:
                    best_ever = best_depth
                    best_ever_positions = population[best_idx].clone()
                    generations_since_improvement = 0
                    
                    improvement = ((best_ever - fol_depth) / fol_depth) * 100
                    print(f"🔥 Gen {gen}: NEW BEST! {best_ever*1e6:.2f} µJ ({improvement:+.1f}% vs FoL) ✓ VALID")
                    
                    self.best_geometries.append({
                        'generation': gen,
                        'well_depth': best_ever,
                        'positions': best_ever_positions.cpu().numpy().tolist(),
                        'improvement_vs_fol': improvement,
                        'valid': True
                    })
                else:
                    generations_since_improvement += 1
            else:
                generations_since_improvement += 1
            
            # Progress
            if gen % 50 == 0:
                elapsed = time.time() - start_time
                eta = (elapsed / (gen + 1)) * (generations - gen - 1)
                valid_count = valid_mask.sum().item()
                print(f"Gen {gen}/{generations} | Best: {best_ever*1e6:.2f} µJ | "
                      f"Valid: {valid_count}/{population_size} | ETA: {eta/60:.1f}min")
            
            # History
            self.history.append({
                'generation': gen,
                'best_fitness': best_depth if valid_mask.any() else 0,
                'mean_fitness': fitness[valid_mask].mean().item() if valid_mask.any() else 0,
                'best_ever': best_ever,
                'valid_count': valid_mask.sum().item()
            })
            
            # Selection (top 20% of VALID geometries)
            n_elite = population_size // 5
            
            if valid_mask.sum() >= n_elite:
                valid_fitness_for_selection = fitness.clone()
                valid_fitness_for_selection[~valid_mask] = -1e10
                elite_indices = valid_fitness_for_selection.topk(n_elite).indices
            else:
                # Not enough valid - take what we have
                elite_indices = torch.where(valid_mask)[0]
                if len(elite_indices) == 0:
                    # No valid geometries! Re-initialize
                    population = self._initialize_valid_population(population_size)
                    continue
            
            elite = population[elite_indices]
            
            # Reproduction
            new_population = []
            new_population.append(elite)
            
            while len(torch.cat(new_population, dim=0)) < population_size:
                # Crossover
                parent1_idx = torch.randint(0, len(elite), (1,)).item()
                parent2_idx = torch.randint(0, len(elite), (1,)).item()
                parent1 = elite[parent1_idx]
                parent2 = elite[parent2_idx]
                
                alpha = torch.rand(1, device=self.device)
                child = alpha * parent1 + (1 - alpha) * parent2
                
                # Mutation
                if torch.rand(1) < 0.1:
                    mutation_mask = torch.rand(self.n_emitters, device=self.device) < 0.3
                    mutation = torch.randn(self.n_emitters, 2, device=self.device) * 0.003
                    child = child + mutation * mutation_mask.unsqueeze(1)
                
                # Repair if needed (push apart if too close)
                child = self._repair_geometry(child)
                
                new_population.append(child.unsqueeze(0))
            
            population = torch.cat(new_population, dim=0)[:population_size]
            
            # Early stopping
            if generations_since_improvement > 200:
                print(f"\n⏹️  Early stopping at generation {gen}")
                break
        
        total_time = time.time() - start_time
        
        print()
        print("=" * 80)
        print("🏆 CONSTRAINED OPTIMIZATION COMPLETE!")
        print("=" * 80)
        print(f"Total time: {total_time/60:.1f} minutes")
        print(f"Best well depth: {best_ever*1e6:.2f} µJ")
        print(f"FoL baseline: {fol_depth*1e6:.2f} µJ")
        improvement = ((best_ever - fol_depth) / fol_depth) * 100
        print(f"Improvement: {improvement:+.2f}%")
        print()
        
        valid, _ = self.check_constraints(best_ever_positions)
        print(f"Final geometry: {'✓ VALID' if valid else '✗ INVALID'}")
        print()
        
        if improvement > 0:
            print("🎉 AI DISCOVERED BETTER GEOMETRY (WITH REAL CONSTRAINTS)!")
        else:
            print("🌸 Flower of Life remains optimal!")
        
        return best_ever_positions, best_ever
    
    def _initialize_valid_population(self, population_size):
        """Initialize population with geometries that satisfy constraints"""
        population = []
        
        for _ in range(population_size):
            attempts = 0
            while attempts < 100:
                # Random positions
                pos = torch.rand(self.n_emitters, 2, device=self.device) * 0.06 - 0.03
                
                # Check constraints
                valid, _ = self.check_constraints(pos)
                
                if valid:
                    population.append(pos.unsqueeze(0))
                    break
                
                attempts += 1
            
            if attempts >= 100:
                # Fallback: use FoL with small perturbation
                fol = self._get_fol_geometry()
                noise = torch.randn_like(fol) * 0.002
                population.append((fol + noise).unsqueeze(0))
        
        return torch.cat(population, dim=0)
    
    def _repair_geometry(self, positions):
        """Repair geometry to satisfy constraints (push emitters apart)"""
        pos = positions.clone()
        
        # Fix spacing violations
        for iteration in range(10):
            fixed = True
            for i in range(self.n_emitters):
                for j in range(i + 1, self.n_emitters):
                    dist = torch.sqrt(torch.sum((pos[i] - pos[j])**2))
                    
                    if dist < MIN_SPACING:
                        # Push apart
                        direction = (pos[i] - pos[j]) / (dist + 1e-6)
                        push = (MIN_SPACING - dist) / 2
                        pos[i] = pos[i] + direction * push
                        pos[j] = pos[j] - direction * push
                        fixed = False
            
            if fixed:
                break
        
        # Fix max spread
        distances = torch.sqrt(torch.sum(pos**2, dim=1))
        if distances.max() > MAX_SPREAD:
            scale = MAX_SPREAD / distances.max()
            pos = pos * scale
        
        return pos
    
    def _get_fol_geometry(self):
        """Get Flower of Life baseline"""
        r1 = 2.5 * self.wavelength
        positions = [[0, 0]]
        for i in range(6):
            theta = i * np.pi / 3
            positions.append([r1 * np.cos(theta), r1 * np.sin(theta)])
        return torch.tensor(positions[:self.n_emitters], dtype=torch.float32, device=self.device)
    
    def visualize_results(self, positions, filename='constrained_ai_geometry.png'):
        """Visualize with constraint circles"""
        fig, axes = plt.subplots(1, 2, figsize=(18, 8))
        
        # Calculate fields
        grid_size = 100
        extent = 0.05
        x = np.linspace(-extent, extent, grid_size)
        y = np.linspace(-extent, extent, grid_size)
        X, Y = np.meshgrid(x, y)
        
        positions_np = positions.cpu().numpy()
        fol_positions = self._get_fol_geometry().cpu().numpy()
        
        # Plot 1: AI Geometry
        ax = axes[0]
        
        emitters_3d = np.zeros((len(positions_np), 3))
        emitters_3d[:, :2] = positions_np
        
        grid_points = np.stack([X.ravel(), Y.ravel(), np.full(grid_size**2, 0.005)], axis=1)
        grid_tensor = torch.tensor(grid_points, dtype=torch.float32, device=self.device)
        emitters_tensor = torch.tensor(emitters_3d, dtype=torch.float32, device=self.device)
        
        U = self._calculate_potential(grid_tensor, emitters_tensor)
        U_grid = U.cpu().numpy().reshape(X.shape) * 1e6
        
        im = ax.contourf(X * 1000, Y * 1000, U_grid, levels=50, cmap='plasma')
        
        # Draw constraint circles
        for pos in positions_np:
            circle = Circle((pos[0]*1000, pos[1]*1000), MIN_SPACING*1000/2, 
                          fill=False, edgecolor='cyan', linewidth=2, linestyle='--', alpha=0.5)
            ax.add_patch(circle)
        
        ax.scatter(positions_np[:, 0] * 1000, positions_np[:, 1] * 1000,
                  c='white', s=300, marker='D', edgecolors='black', linewidths=3, zorder=10,
                  label='AI-Discovered (Constrained)')
        
        ax.set_xlabel('X (mm)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Y (mm)', fontsize=14, fontweight='bold')
        ax.set_title('AI-Discovered Geometry\n(With Physical Constraints)', fontsize=16, fontweight='bold')
        ax.set_aspect('equal')
        plt.colorbar(im, ax=ax, label='Potential (µJ)')
        ax.legend(fontsize=10)
        
        # Plot 2: Comparison
        ax = axes[1]
        
        ax.scatter(fol_positions[:, 0] * 1000, fol_positions[:, 1] * 1000,
                  c='#00ff88', s=400, marker='o', edgecolors='white', linewidths=3,
                  label='Flower of Life', alpha=0.7, zorder=5)
        
        ax.scatter(positions_np[:, 0] * 1000, positions_np[:, 1] * 1000,
                  c='#ff00ff', s=400, marker='D', edgecolors='white', linewidths=3,
                  label='AI-Discovered (Constrained)', alpha=0.9, zorder=10)
        
        # Draw constraint zones
        for pos in positions_np:
            circle = Circle((pos[0]*1000, pos[1]*1000), MIN_SPACING*1000/2,
                          fill=True, facecolor='cyan', alpha=0.1, edgecolor='cyan', linewidth=1)
            ax.add_patch(circle)
        
        ax.set_xlabel('X (mm)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Y (mm)', fontsize=14, fontweight='bold')
        ax.set_title('Comparison: FoL vs Constrained AI', fontsize=16, fontweight='bold')
        ax.set_aspect('equal')
        ax.legend(fontsize=12, loc='upper right')
        ax.grid(alpha=0.3)
        ax.set_xlim(-60, 60)
        ax.set_ylim(-60, 60)
        
        # Add constraint info
        textstr = f'''CONSTRAINTS ENFORCED:
Min spacing: {MIN_SPACING*1000:.1f}mm
Max spread: {MAX_SPREAD*1000:.1f}mm

All emitters satisfy
physical realizability!'''
        
        props = dict(boxstyle='round', facecolor='lightblue', alpha=0.8)
        ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=props)
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✓ Saved visualization: {filename}")
        
        return fig
    
    def save_results(self, positions, well_depth, filename='constrained_optimization_results.json'):
        """Save results"""
        valid, penalty = self.check_constraints(positions)
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'gpu': gpu_name,
            'n_emitters': self.n_emitters,
            'frequency': self.frequency,
            'constraints': {
                'min_spacing_mm': MIN_SPACING * 1000,
                'max_spread_mm': MAX_SPREAD * 1000
            },
            'best_well_depth': well_depth,
            'best_positions': positions.cpu().numpy().tolist(),
            'valid': valid,
            'constraint_penalty': penalty,
            'history': self.history,
            'best_geometries': self.best_geometries
        }
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"✓ Saved results: {filename}")

def main():
    """Run constrained optimization"""
    print("🚀 CONSTRAINED GEOMETRY OPTIMIZATION")
    print()
    print("This will find the REAL optimal geometry with physical constraints!")
    print()
    
    optimizer = ConstrainedOptimizer(n_emitters=7, device=device)
    
    print("Running evolutionary optimization with constraints...")
    print()
    
    positions, depth = optimizer.run_constrained_evolutionary(
        generations=1500,
        population_size=200
    )
    
    # Visualize
    print()
    print("📊 Creating visualizations...")
    optimizer.visualize_results(positions)
    
    # Save
    print()
    print("💾 Saving results...")
    optimizer.save_results(positions, depth)
    
    print()
    print("=" * 80)
    print("✅ CONSTRAINED OPTIMIZATION COMPLETE!")
    print("=" * 80)
    print()
    print("Files created:")
    print("  • constrained_ai_geometry.png - Visual comparison")
    print("  • constrained_optimization_results.json - Full data")
    print()
    print("🎥 Ready for Part 3 video!")
    print()

if __name__ == '__main__':
    main()
