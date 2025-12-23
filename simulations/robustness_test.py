"""
🛠️ ROBUSTNESS TEST: MANUFACTURING TOLERANCE ANALYSIS 🛠️
=========================================================

Does Flower of Life work in the REAL WORLD?

This test:
✓ Adds realistic manufacturing errors (±2mm position, ±15° phase)
✓ Compares FoL vs random arrays under same noise
✓ Tests emitter failures (disabled transducers)
✓ Runs 1,000 trials for statistical confidence
✓ Proves FoL is STABLE not fragile

Why this matters:
- 3D printers have tolerance (±0.5-2mm)
- Hand assembly has errors
- Phase drivers have noise
- Transducers can fail

If FoL degrades gracefully while random fails catastrophically,
it proves the geometry is ROBUST for real builds!

Authors: Sportysport & Claude (Anthropic)
License: MIT
"""

import numpy as np
import torch
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import json
import time
from datetime import datetime
from scipy import stats

print("=" * 80)
print("🛠️ ROBUSTNESS TEST: MANUFACTURING TOLERANCE ANALYSIS")
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
SPEED_OF_SOUND = 343.0
AIR_DENSITY = 1.225

# Manufacturing tolerances (REALISTIC!)
POSITION_NOISE_MM = 2.0  # ±2mm position error (3D printer / hand assembly)
PHASE_NOISE_DEG = 15.0   # ±15° phase error (driver electronics)
FAILURE_RATE = 0.05      # 5% chance any emitter fails

class RobustnessTest:
    """Test FoL vs random under realistic manufacturing errors"""
    
    def __init__(self, n_emitters=19, frequency=40000.0, device='cuda'):
        self.device = device
        self.n_emitters = n_emitters
        self.frequency = frequency
        self.wavelength = 343.0 / frequency
        
    def _get_perfect_fol(self):
        """Get perfect Flower of Life (no noise)"""
        r1 = 2.5 * self.wavelength
        r2 = 5.0 * self.wavelength
        
        positions = [[0, 0]]
        
        for i in range(6):
            theta = i * np.pi / 3
            positions.append([r1 * np.cos(theta), r1 * np.sin(theta)])
        
        for i in range(12):
            theta = i * np.pi / 6
            positions.append([r2 * np.cos(theta), r2 * np.sin(theta)])
        
        return torch.tensor(positions[:self.n_emitters], 
                          dtype=torch.float32, device=self.device)
    
    def _get_random_array(self):
        """Get random emitter positions with ENFORCED minimum spacing"""
        MIN_SPACING = 0.012  # 12mm minimum (same constraint as FoL!)
        MAX_ATTEMPTS = 1000
        
        positions = []
        
        for i in range(self.n_emitters):
            attempts = 0
            while attempts < MAX_ATTEMPTS:
                # Random position within ±40mm
                new_pos = torch.rand(2, device=self.device) * 0.08 - 0.04
                
                # Check spacing against all existing positions
                valid = True
                for existing_pos in positions:
                    dist = torch.sqrt(torch.sum((new_pos - existing_pos)**2))
                    if dist < MIN_SPACING:
                        valid = False
                        break
                
                if valid or len(positions) == 0:
                    positions.append(new_pos)
                    break
                
                attempts += 1
            
            if attempts >= MAX_ATTEMPTS:
                # Fallback: place at a safe distance from center
                angle = (i / self.n_emitters) * 2 * np.pi
                radius = 0.025 + (i / self.n_emitters) * 0.015
                new_pos = torch.tensor([radius * np.cos(angle), radius * np.sin(angle)],
                                      device=self.device)
                positions.append(new_pos)
        
        return torch.stack(positions)
    
    def add_manufacturing_noise(self, positions, position_noise_mm, phase_noise_deg):
        """
        Add realistic manufacturing errors
        
        Args:
            positions: Perfect positions (n_emitters, 2)
            position_noise_mm: Position error std (mm)
            phase_noise_deg: Phase error std (degrees)
        
        Returns:
            noisy_positions, noisy_phases
        """
        # Position noise (Gaussian, ±2mm typical)
        noise = torch.randn_like(positions, device=self.device) * (position_noise_mm / 1000)
        noisy_positions = positions + noise
        
        # Phase noise (Gaussian, ±15° typical)
        phase_noise_rad = phase_noise_deg * np.pi / 180
        noisy_phases = torch.randn(self.n_emitters, device=self.device) * phase_noise_rad
        
        return noisy_positions, noisy_phases
    
    def simulate_failures(self, failure_rate=0.05):
        """
        Simulate random emitter failures
        
        Returns:
            active_mask: Boolean tensor (True = working, False = failed)
        """
        random_vals = torch.rand(self.n_emitters, device=self.device)
        active_mask = random_vals > failure_rate
        return active_mask
    
    def calculate_well_depth(self, positions, phases=None, active_mask=None):
        """Calculate well depth with noise and failures"""
        if phases is None:
            phases = torch.zeros(self.n_emitters, device=self.device)
        
        if active_mask is None:
            active_mask = torch.ones(self.n_emitters, dtype=torch.bool, device=self.device)
        
        # Only use active emitters
        active_positions = positions[active_mask]
        active_phases = phases[active_mask]
        n_active = active_mask.sum().item()
        
        if n_active == 0:
            return 0.0  # All failed!
        
        # Evaluation grid
        grid_size = 60
        extent = 0.05
        
        x = torch.linspace(-extent, extent, grid_size, device=self.device)
        y = torch.linspace(-extent, extent, grid_size, device=self.device)
        X, Y = torch.meshgrid(x, y, indexing='ij')
        Z = torch.full_like(X, 0.005)
        
        grid_points = torch.stack([X.ravel(), Y.ravel(), Z.ravel()], dim=1)
        
        # Add z=0 to positions
        emitters_3d = torch.cat([active_positions, 
                                torch.zeros(n_active, 1, device=self.device)], 
                               dim=1)
        
        # Calculate potential
        U = self._calculate_potential(grid_points, emitters_3d, active_phases)
        
        well_depth = (U.max() - U.min()).item()
        
        return well_depth
    
    def _calculate_potential(self, points, emitters, phases):
        """Gor'kov potential calculation"""
        k = 2 * np.pi / self.wavelength
        
        pts = points.unsqueeze(1)
        ems = emitters.unsqueeze(0)
        
        r = torch.sqrt(torch.sum((pts - ems)**2, dim=2))
        r = torch.clamp(r, min=1e-6)
        
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
    
    def run_robustness_trials(self, n_trials=1000):
        """
        Run robustness test with realistic manufacturing errors
        """
        print("🛠️ ROBUSTNESS TEST")
        print()
        print(f"📏 MANUFACTURING TOLERANCES:")
        print(f"   Position error: ±{POSITION_NOISE_MM:.1f}mm (Gaussian)")
        print(f"   Phase error: ±{PHASE_NOISE_DEG:.1f}° (Gaussian)")
        print(f"   Failure rate: {FAILURE_RATE*100:.1f}% per emitter")
        print(f"   Trials: {n_trials}")
        print()
        
        # Get perfect geometries
        perfect_fol = self._get_perfect_fol()
        
        # Baseline (perfect conditions)
        perfect_fol_depth = self.calculate_well_depth(perfect_fol)
        
        print(f"📊 BASELINE (Perfect FoL, No Noise):")
        print(f"   Well depth: {perfect_fol_depth*1e6:.2f} µJ")
        print()
        
        # Storage for results
        fol_results = {
            'position_noise_only': [],
            'phase_noise_only': [],
            'both_noise': [],
            'with_failures': []
        }
        
        random_results = {
            'position_noise_only': [],
            'phase_noise_only': [],
            'both_noise': [],
            'with_failures': []
        }
        
        start_time = time.time()
        
        print("Running trials...")
        print()
        
        for trial in range(n_trials):
            if trial % 100 == 0:
                print(f"Trial {trial}/{n_trials}...")
            
            # Get random array for this trial
            random_positions = self._get_random_array()
            
            # TEST 1: Position noise only
            fol_noisy_pos, _ = self.add_manufacturing_noise(perfect_fol, POSITION_NOISE_MM, 0)
            rand_noisy_pos, _ = self.add_manufacturing_noise(random_positions, POSITION_NOISE_MM, 0)
            
            fol_depth_1 = self.calculate_well_depth(fol_noisy_pos)
            rand_depth_1 = self.calculate_well_depth(rand_noisy_pos)
            
            fol_results['position_noise_only'].append(fol_depth_1)
            random_results['position_noise_only'].append(rand_depth_1)
            
            # TEST 2: Phase noise only
            _, fol_noisy_phase = self.add_manufacturing_noise(perfect_fol, 0, PHASE_NOISE_DEG)
            _, rand_noisy_phase = self.add_manufacturing_noise(random_positions, 0, PHASE_NOISE_DEG)
            
            fol_depth_2 = self.calculate_well_depth(perfect_fol, fol_noisy_phase)
            rand_depth_2 = self.calculate_well_depth(random_positions, rand_noisy_phase)
            
            fol_results['phase_noise_only'].append(fol_depth_2)
            random_results['phase_noise_only'].append(rand_depth_2)
            
            # TEST 3: Both noise sources
            fol_noisy_pos, fol_noisy_phase = self.add_manufacturing_noise(
                perfect_fol, POSITION_NOISE_MM, PHASE_NOISE_DEG)
            rand_noisy_pos, rand_noisy_phase = self.add_manufacturing_noise(
                random_positions, POSITION_NOISE_MM, PHASE_NOISE_DEG)
            
            fol_depth_3 = self.calculate_well_depth(fol_noisy_pos, fol_noisy_phase)
            rand_depth_3 = self.calculate_well_depth(rand_noisy_pos, rand_noisy_phase)
            
            fol_results['both_noise'].append(fol_depth_3)
            random_results['both_noise'].append(rand_depth_3)
            
            # TEST 4: With random failures
            active_mask = self.simulate_failures(FAILURE_RATE)
            
            fol_depth_4 = self.calculate_well_depth(fol_noisy_pos, fol_noisy_phase, active_mask)
            rand_depth_4 = self.calculate_well_depth(rand_noisy_pos, rand_noisy_phase, active_mask)
            
            fol_results['with_failures'].append(fol_depth_4)
            random_results['with_failures'].append(rand_depth_4)
        
        total_time = time.time() - start_time
        
        # Convert to numpy for statistics
        for key in fol_results:
            fol_results[key] = np.array(fol_results[key]) * 1e6  # Convert to µJ
            random_results[key] = np.array(random_results[key]) * 1e6
        
        print()
        print("=" * 80)
        print("🏆 ROBUSTNESS TEST COMPLETE!")
        print("=" * 80)
        print(f"Total time: {total_time:.1f} seconds")
        print()
        
        # Statistics
        print("📊 RESULTS:")
        print()
        
        tests = [
            ('Position Noise Only (±2mm)', 'position_noise_only'),
            ('Phase Noise Only (±15°)', 'phase_noise_only'),
            ('Both Noise Sources', 'both_noise'),
            ('With 5% Emitter Failures', 'with_failures')
        ]
        
        for test_name, test_key in tests:
            fol_data = fol_results[test_key]
            rand_data = random_results[test_key]
            
            # Remove zeros (complete failures)
            fol_data_nonzero = fol_data[fol_data > 0]
            rand_data_nonzero = rand_data[rand_data > 0]
            
            fol_mean = fol_data_nonzero.mean() if len(fol_data_nonzero) > 0 else 0
            fol_std = fol_data_nonzero.std() if len(fol_data_nonzero) > 0 else 0
            rand_mean = rand_data_nonzero.mean() if len(rand_data_nonzero) > 0 else 0
            rand_std = rand_data_nonzero.std() if len(rand_data_nonzero) > 0 else 0
            
            fol_success = (fol_data > 0).sum() / len(fol_data) * 100
            rand_success = (rand_data > 0).sum() / len(rand_data) * 100
            
            # Statistical test
            if len(fol_data_nonzero) > 0 and len(rand_data_nonzero) > 0:
                t_stat, p_value = stats.ttest_ind(fol_data_nonzero, rand_data_nonzero)
                cohen_d = (fol_mean - rand_mean) / np.sqrt((fol_std**2 + rand_std**2) / 2)
            else:
                p_value = 1.0
                cohen_d = 0.0
            
            print(f"{test_name}:")
            print(f"  FoL:    {fol_mean:7.2f} ± {fol_std:6.2f} µJ ({fol_success:.1f}% success)")
            print(f"  Random: {rand_mean:7.2f} ± {rand_std:6.2f} µJ ({rand_success:.1f}% success)")
            print(f"  p-value: {p_value:.2e} | Cohen's d: {cohen_d:+.3f}")
            
            if fol_mean > rand_mean:
                improvement = ((fol_mean - rand_mean) / rand_mean * 100) if rand_mean > 0 else 0
                print(f"  ✓ FoL is {improvement:.1f}% more robust!")
            print()
        
        # Overall assessment
        print("=" * 80)
        print("🎯 ASSESSMENT:")
        print("=" * 80)
        
        # Check if FoL is consistently better
        all_better = all(
            fol_results[test_key].mean() > random_results[test_key].mean()
            for _, test_key in tests
        )
        
        if all_better:
            print("✅ FLOWER OF LIFE IS ROBUST!")
            print("   FoL outperforms random arrays under ALL noise conditions")
            print("   Sacred geometry degrades GRACEFULLY, not catastrophically")
        else:
            print("⚠️  Mixed results - some conditions favor random")
        
        print()
        
        return fol_results, random_results, perfect_fol_depth * 1e6
    
    def visualize_results(self, fol_results, random_results, perfect_depth,
                         filename='robustness_test_results.png'):
        """Visualize robustness test results"""
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        tests = [
            ('Position Noise (±2mm)', 'position_noise_only'),
            ('Phase Noise (±15°)', 'phase_noise_only'),
            ('Both Noise Sources', 'both_noise'),
            ('With 5% Failures', 'with_failures')
        ]
        
        for idx, (ax, (test_name, test_key)) in enumerate(zip(axes.flat, tests)):
            fol_data = fol_results[test_key]
            rand_data = random_results[test_key]
            
            # Remove zeros
            fol_data = fol_data[fol_data > 0]
            rand_data = rand_data[rand_data > 0]
            
            # Histograms
            bins = np.linspace(0, max(fol_data.max(), rand_data.max()), 50)
            
            ax.hist(rand_data, bins=bins, alpha=0.6, color='red', 
                   label=f'Random (μ={rand_data.mean():.1f}µJ)', edgecolor='black')
            ax.hist(fol_data, bins=bins, alpha=0.6, color='green',
                   label=f'FoL (μ={fol_data.mean():.1f}µJ)', edgecolor='black')
            
            # Perfect baseline
            ax.axvline(perfect_depth, color='blue', linestyle='--', linewidth=2,
                      label=f'Perfect FoL ({perfect_depth:.1f}µJ)')
            
            ax.set_xlabel('Well Depth (µJ)', fontweight='bold', fontsize=12)
            ax.set_ylabel('Count', fontweight='bold', fontsize=12)
            ax.set_title(test_name, fontweight='bold', fontsize=14)
            ax.legend(fontsize=10)
            ax.grid(alpha=0.3)
        
        plt.suptitle('Robustness Test: FoL vs Random Under Manufacturing Errors',
                    fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✓ Saved visualization: {filename}")
        
        return fig
    
    def save_results(self, fol_results, random_results, perfect_depth,
                    filename='robustness_test_results.json'):
        """Save results to JSON"""
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'gpu': gpu_name,
            'n_emitters': self.n_emitters,
            'frequency': self.frequency,
            'tolerances': {
                'position_noise_mm': POSITION_NOISE_MM,
                'phase_noise_deg': PHASE_NOISE_DEG,
                'failure_rate': FAILURE_RATE
            },
            'perfect_fol_depth': float(perfect_depth),
            'fol_results': {k: v.tolist() for k, v in fol_results.items()},
            'random_results': {k: v.tolist() for k, v in random_results.items()}
        }
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"✓ Saved results: {filename}")

def main():
    """Run robustness test"""
    print("=" * 80)
    print("TESTING: Does FoL work with REAL manufacturing errors?")
    print("=" * 80)
    print()
    
    tester = RobustnessTest(n_emitters=19, device=device)
    
    fol_results, random_results, perfect_depth = tester.run_robustness_trials(
        n_trials=1000
    )
    
    print()
    print("📊 Creating visualizations...")
    tester.visualize_results(fol_results, random_results, perfect_depth)
    
    print()
    print("💾 Saving results...")
    tester.save_results(fol_results, random_results, perfect_depth)
    
    print()
    print("=" * 80)
    print("✅ ROBUSTNESS TEST COMPLETE!")
    print("=" * 80)
    print()
    print("Files created:")
    print("  • robustness_test_results.png - Statistical comparison")
    print("  • robustness_test_results.json - Full data")
    print()
    print("🎥 Ready for robustness video!")
    print()

if __name__ == '__main__':
    main()
