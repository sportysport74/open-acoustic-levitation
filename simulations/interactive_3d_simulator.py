"""
Real-Time Interactive 3D Acoustic Levitation Simulator
=======================================================

GPU-accelerated live visualization of acoustic fields.

Controls:
- Left-click drag: Rotate view
- Right-click drag: Pan view
- Scroll: Zoom
- Press 'a': Add random emitter
- Press 'd': Remove last emitter  
- Press 'p': Drop particle
- Press 'r': Reset
- Press 's': Save configuration
- Sliders: Adjust frequency, power, particle size

Hardware: Optimized for RTX 5090 + Ryzen 9 5900X

Authors: Sportysport & Claude (Anthropic)
License: MIT
"""

import sys
import numpy as np
import torch
import pyvista as pv
from pyvista.plotting import Plotter
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QSlider, QLabel, QPushButton, QFrame)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.Qt import QGridLayout
import time

print("=" * 70)
print("🎮 REAL-TIME 3D ACOUSTIC LEVITATION SIMULATOR")
print("=" * 70)
print()

# Check GPU
if torch.cuda.is_available():
    device = torch.device('cuda')
    gpu_name = torch.cuda.get_device_name(0)
    print(f"✓ GPU: {gpu_name}")
    print(f"✓ CUDA: {torch.version.cuda}")
    print(f"✓ PyTorch: {torch.__version__}")
else:
    device = torch.device('cpu')
    print("⚠️  GPU not detected, using CPU (will be slower)")
print()

# Physical constants (as tensors)
SPEED_OF_SOUND = torch.tensor(343.0, device=device)
AIR_DENSITY = torch.tensor(1.225, device=device)

class AcousticSimulator:
    """GPU-accelerated acoustic field calculator"""
    
    def __init__(self, device='cuda'):
        self.device = device
        self.emitter_positions = []
        self.emitter_phases = []
        self.frequency = 40000.0  # Hz
        self.power = 1.0
        self.particle_size = 3.0  # mm
        
        # Particles for live simulation
        self.particles = []
        
        # Performance tracking
        self.last_calc_time = 0
        
    def set_emitters(self, positions, phases=None):
        """Set emitter positions (Nx3 array)"""
        self.emitter_positions = torch.tensor(positions, 
                                             dtype=torch.float32, 
                                             device=self.device)
        
        if phases is None:
            self.emitter_phases = torch.zeros(len(positions), 
                                             device=self.device)
        else:
            self.emitter_phases = torch.tensor(phases, 
                                              dtype=torch.float32,
                                              device=self.device)
    
    def calculate_field_gpu(self, grid_points):
        """
        Calculate acoustic potential at grid points
        
        Args:
            grid_points: (N, 3) tensor of evaluation points
        
        Returns:
            (N,) tensor of Gor'kov potential values
        """
        start = time.time()
        
        wavelength = SPEED_OF_SOUND / self.frequency
        k = 2 * torch.pi / wavelength
        
        # Grid points: (N, 3)
        # Emitter positions: (M, 3)
        # Distance matrix: (N, M)
        
        # Reshape for broadcasting
        points = grid_points.unsqueeze(1)  # (N, 1, 3)
        emitters = self.emitter_positions.unsqueeze(0)  # (1, M, 3)
        
        # Distance from each point to each emitter
        r = torch.sqrt(torch.sum((points - emitters)**2, dim=2))  # (N, M)
        r = torch.clamp(r, min=1e-6)
        
        # Phases
        phases = self.emitter_phases.unsqueeze(0)  # (1, M)
        
        # Complex pressure from each emitter
        pressure_amp = self.power * 1000.0  # Scale by power
        p_real = (pressure_amp / r) * torch.cos(k * r + phases)
        p_imag = (pressure_amp / r) * torch.sin(k * r + phases)
        
        # Sum contributions
        p_total_real = p_real.sum(dim=1)
        p_total_imag = p_imag.sum(dim=1)
        
        # Magnitude squared
        p_mag_sq = p_total_real**2 + p_total_imag**2
        
        # Gor'kov potential
        particle_radius = (self.particle_size / 1000) / 2
        V0 = (4/3) * torch.pi * particle_radius**3
        particle_density = torch.tensor(84.0, device=self.device)
        f1 = 1 - (AIR_DENSITY / particle_density)
        
        U = -V0 * (f1 / (2 * AIR_DENSITY * SPEED_OF_SOUND**2)) * p_mag_sq
        
        self.last_calc_time = time.time() - start
        
        return U
    
    def add_emitter(self, position):
        """Add emitter at position [x, y, z]"""
        if len(self.emitter_positions) == 0:
            self.emitter_positions = torch.tensor([position], 
                                                  dtype=torch.float32,
                                                  device=self.device)
            self.emitter_phases = torch.zeros(1, device=self.device)
        else:
            new_pos = torch.tensor([position], 
                                  dtype=torch.float32,
                                  device=self.device)
            self.emitter_positions = torch.cat([self.emitter_positions, new_pos])
            self.emitter_phases = torch.cat([self.emitter_phases, 
                                           torch.zeros(1, device=self.device)])
    
    def remove_emitter(self):
        """Remove last emitter"""
        if len(self.emitter_positions) > 0:
            self.emitter_positions = self.emitter_positions[:-1]
            self.emitter_phases = self.emitter_phases[:-1]
    
    def add_particle(self, position, velocity=[0, 0, 0]):
        """Add particle for real-time simulation"""
        self.particles.append({
            'pos': torch.tensor(position, dtype=torch.float32, device=self.device),
            'vel': torch.tensor(velocity, dtype=torch.float32, device=self.device)
        })

class InteractiveWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        self.simulator = AcousticSimulator(device=device)
        
        # Initialize with Flower of Life
        self.init_flower_of_life()
        
        self.init_ui()
        
        # Timer for real-time updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_visualization)
        self.timer.start(33)  # ~30 FPS
        
        self.fps_counter = 0
        self.fps_time = time.time()
        
    def init_flower_of_life(self):
        """Initialize with 7-emitter Flower of Life"""
        wavelength = 343.0 / 40000.0
        r1 = 2.5 * wavelength
        
        positions = [[0, 0, 0]]
        for i in range(6):
            theta = i * np.pi / 3
            positions.append([r1 * np.cos(theta), r1 * np.sin(theta), 0])
        
        self.simulator.set_emitters(positions)
    
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle('🎮 Real-Time Acoustic Levitation Simulator')
        self.setGeometry(100, 100, 1600, 900)
        
        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout()
        main_widget.setLayout(layout)
        
        # Left side: 3D view
        self.plotter = Plotter()
        layout.addWidget(self.plotter.iren.interactor, stretch=3)
        
        # Right side: Controls
        controls = self.create_controls()
        layout.addWidget(controls, stretch=1)
        
        # Initial visualization
        self.update_visualization()
    
    def create_controls(self):
        """Create control panel"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Box)
        layout = QVBoxLayout()
        frame.setLayout(layout)
        
        # Title
        title = QLabel("🎛️ CONTROLS")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        # Frequency slider
        layout.addWidget(QLabel("Frequency (kHz):"))
        self.freq_slider = QSlider(Qt.Horizontal)
        self.freq_slider.setMinimum(20)
        self.freq_slider.setMaximum(60)
        self.freq_slider.setValue(40)
        self.freq_slider.valueChanged.connect(self.on_freq_change)
        layout.addWidget(self.freq_slider)
        self.freq_label = QLabel("40.0 kHz")
        layout.addWidget(self.freq_label)
        
        # Power slider
        layout.addWidget(QLabel("Power:"))
        self.power_slider = QSlider(Qt.Horizontal)
        self.power_slider.setMinimum(10)
        self.power_slider.setMaximum(200)
        self.power_slider.setValue(100)
        self.power_slider.valueChanged.connect(self.on_power_change)
        layout.addWidget(self.power_slider)
        self.power_label = QLabel("100%")
        layout.addWidget(self.power_label)
        
        # Particle size slider
        layout.addWidget(QLabel("Particle Size (mm):"))
        self.size_slider = QSlider(Qt.Horizontal)
        self.size_slider.setMinimum(10)
        self.size_slider.setMaximum(80)
        self.size_slider.setValue(30)
        self.size_slider.valueChanged.connect(self.on_size_change)
        layout.addWidget(self.size_slider)
        self.size_label = QLabel("3.0 mm")
        layout.addWidget(self.size_label)
        
        # Buttons
        btn_add = QPushButton("➕ Add Random Emitter")
        btn_add.clicked.connect(self.add_random_emitter)
        layout.addWidget(btn_add)
        
        btn_remove = QPushButton("➖ Remove Last Emitter")
        btn_remove.clicked.connect(self.remove_emitter)
        layout.addWidget(btn_remove)
        
        btn_particle = QPushButton("🎯 Drop Particle")
        btn_particle.clicked.connect(self.drop_particle)
        layout.addWidget(btn_particle)
        
        btn_reset = QPushButton("🔄 Reset to FoL")
        btn_reset.clicked.connect(self.reset_fol)
        layout.addWidget(btn_reset)
        
        # Stats
        layout.addWidget(QLabel(""))
        self.stats_label = QLabel("Stats:")
        self.stats_label.setStyleSheet("font-family: monospace;")
        layout.addWidget(self.stats_label)
        
        layout.addStretch()
        
        return frame
    
    def on_freq_change(self, value):
        self.simulator.frequency = value * 1000.0
        self.freq_label.setText(f"{value}.0 kHz")
    
    def on_power_change(self, value):
        self.simulator.power = value / 100.0
        self.power_label.setText(f"{value}%")
    
    def on_size_change(self, value):
        self.simulator.particle_size = value / 10.0
        self.size_label.setText(f"{value/10.0:.1f} mm")
    
    def add_random_emitter(self):
        # Random position within ±30mm
        pos = [np.random.uniform(-0.03, 0.03) for _ in range(3)]
        self.simulator.add_emitter(pos)
    
    def remove_emitter(self):
        self.simulator.remove_emitter()
    
    def drop_particle(self):
        # Drop from above center
        pos = [0, 0, 0.02]  # 20mm above
        self.simulator.add_particle(pos, [0, 0, -0.001])
    
    def reset_fol(self):
        self.init_flower_of_life()
        self.simulator.particles = []
    
    def update_visualization(self):
        """Update 3D visualization"""
        self.plotter.clear()
        
        # Create 3D grid
        grid_size = 40
        extent = 0.03  # ±30mm
        
        x = np.linspace(-extent, extent, grid_size)
        y = np.linspace(-extent, extent, grid_size)
        z = np.linspace(-extent/2, extent/2, grid_size//2)
        
        X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
        
        # Flatten to points
        points = np.stack([X.ravel(), Y.ravel(), Z.ravel()], axis=1)
        points_tensor = torch.tensor(points, dtype=torch.float32, device=device)
        
        # Calculate field on GPU
        if len(self.simulator.emitter_positions) > 0:
            U = self.simulator.calculate_field_gpu(points_tensor)
            U_np = U.cpu().numpy()
            
            # Reshape
            U_grid = U_np.reshape(X.shape)
            
            # Create PyVista grid
            grid = pv.StructuredGrid(X, Y, Z)
            grid['potential'] = U_grid.ravel()
            
            # Volume rendering
            self.plotter.add_volume(grid, cmap='RdYlBu_r', opacity='sigmoid',
                                   scalar_bar_args={'title': 'Potential (J)'})
        
        # Plot emitters
        if len(self.simulator.emitter_positions) > 0:
            emitters_np = self.simulator.emitter_positions.cpu().numpy()
            emitter_cloud = pv.PolyData(emitters_np)
            self.plotter.add_mesh(emitter_cloud, color='black', point_size=20,
                                 render_points_as_spheres=True)
        
        # FPS counter
        self.fps_counter += 1
        if time.time() - self.fps_time > 1.0:
            fps = self.fps_counter / (time.time() - self.fps_time)
            
            stats = f"FPS: {fps:.1f}\n"
            stats += f"Emitters: {len(self.simulator.emitter_positions)}\n"
            stats += f"Calc Time: {self.simulator.last_calc_time*1000:.1f}ms\n"
            stats += f"GPU: {gpu_name if device.type=='cuda' else 'CPU'}"
            
            self.stats_label.setText(stats)
            
            self.fps_counter = 0
            self.fps_time = time.time()

def main():
    app = QApplication(sys.argv)
    window = InteractiveWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    print("Starting interactive simulator...")
    print()
    print("Controls:")
    print("  - Sliders: Adjust frequency, power, particle size")
    print("  - Buttons: Add/remove emitters, drop particles, reset")
    print("  - Mouse: Rotate (left), pan (right), zoom (scroll)")
    print()
    print("=" * 70)
    print()
    
    main()
