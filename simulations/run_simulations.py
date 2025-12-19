#!/usr/bin/env python3
"""
Open Acoustic Levitation - Master Simulation Suite
===================================================

Unified command-line interface for all acoustic levitation simulations.

Usage:
    python run_simulations.py --geometry fol --emitters 7 --output results/
    python run_simulations.py --monte-carlo --trials 100
    python run_simulations.py --phase-optimize --target 0,0,10
    python run_simulations.py --compare-all --export-data

Authors: Sportysport & Claude (Anthropic)
License: MIT
"""

import argparse
import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import json
import csv
from datetime import datetime

# ============================================================================
# ARGUMENT PARSER
# ============================================================================

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Open Acoustic Levitation Simulation Suite',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single geometry simulation
  python run_simulations.py --geometry fol --emitters 7
  
  # Compare multiple geometries
  python run_simulations.py --compare-all
  
  # Monte Carlo analysis (100 random trials)
  python run_simulations.py --monte-carlo --trials 100
  
  # Phase optimization
  python run_simulations.py --phase-optimize --target 0,0,10
  
  # Export data for external analysis
  python run_simulations.py --geometry fol --export-data --output data/
  
  # Reproduce Marzo 2015 benchmark
  python run_simulations.py --benchmark marzo2015
  
Geometries:
  fol       : Flower of Life (golden ratio spacing)
  fibonacci : Fibonacci spiral
  hexagonal : Hexagonal uniform spacing
  square    : Square grid
  random    : Random placement
  marzo     : Marzo holographic array
  brandt    : Brandt standing wave
        """
    )
    
    # Geometry selection
    parser.add_argument('--geometry', '-g', 
                       choices=['fol', 'fibonacci', 'hexagonal', 'square', 
                               'random', 'marzo', 'brandt'],
                       help='Array geometry to simulate')
    
    parser.add_argument('--emitters', '-n', type=int, default=7,
                       choices=[7, 19, 37],
                       help='Number of emitters (7, 19, or 37)')
    
    # Comparison modes
    parser.add_argument('--compare-all', action='store_true',
                       help='Compare all geometries side-by-side')
    
    parser.add_argument('--monte-carlo', action='store_true',
                       help='Run Monte Carlo analysis with random trials')
    
    parser.add_argument('--trials', type=int, default=100,
                       help='Number of Monte Carlo trials (default: 100)')
    
    # Phase optimization
    parser.add_argument('--phase-optimize', action='store_true',
                       help='Enable phase optimization mode')
    
    parser.add_argument('--target', type=str,
                       help='Target focal point (x,y,z in mm, e.g., "0,0,10")')
    
    parser.add_argument('--twin-trap', action='store_true',
                       help='Optimize for twin trap configuration')
    
    # Benchmarking
    parser.add_argument('--benchmark', 
                       choices=['marzo2015', 'brandt2001', 'tinylev'],
                       help='Reproduce published benchmark result')
    
    # Simulation parameters
    parser.add_argument('--frequency', '-f', type=float, default=40.0,
                       help='Carrier frequency in kHz (default: 40.0)')
    
    parser.add_argument('--grid-size', type=int, default=80,
                       help='Grid resolution (default: 80)')
    
    parser.add_argument('--particle-size', type=float, default=3.0,
                       help='Particle diameter in mm (default: 3.0)')
    
    # Animation
    parser.add_argument('--animate', action='store_true',
                       help='Generate animated GIF of particle trajectories')
    
    parser.add_argument('--animation-time', type=float, default=1.0,
                       help='Animation duration in seconds (default: 1.0)')
    
    # Output options
    parser.add_argument('--output', '-o', type=str, default='results/',
                       help='Output directory (default: results/)')
    
    parser.add_argument('--export-data', action='store_true',
                       help='Export raw data (CSV, JSON) for external analysis')
    
    parser.add_argument('--export-positions', action='store_true',
                       help='Export emitter positions to CSV')
    
    parser.add_argument('--export-fields', action='store_true',
                       help='Export potential field grids to CSV')
    
    # Visualization
    parser.add_argument('--colormap', default='RdYlBu_r',
                       help='Matplotlib colormap (default: RdYlBu_r)')
    
    parser.add_argument('--dpi', type=int, default=300,
                       help='Output image DPI (default: 300)')
    
    parser.add_argument('--no-show', action='store_true',
                       help="Don't display plots (save only)")
    
    # Performance
    parser.add_argument('--use-gpu', action='store_true',
                       help='Use GPU acceleration (requires PyTorch)')
    
    parser.add_argument('--numba', action='store_true',
                       help='Use Numba JIT compilation for speed')
    
    parser.add_argument('--parallel', action='store_true',
                       help='Use parallel processing for Monte Carlo')
    
    # Misc
    parser.add_argument('--seed', type=int,
                       help='Random seed for reproducibility')
    
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress all output except errors')
    
    return parser.parse_args()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    args = parse_arguments()
    
    # Set up output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Set random seed if provided
    if args.seed is not None:
        np.random.seed(args.seed)
    
    # Print banner
    if not args.quiet:
        print("=" * 70)
        print("OPEN ACOUSTIC LEVITATION - SIMULATION SUITE")
        print("=" * 70)
        print()
        print(f"Configuration:")
        print(f"  Geometry: {args.geometry if args.geometry else 'N/A (comparison mode)'}")
        print(f"  Emitters: {args.emitters}")
        print(f"  Frequency: {args.frequency} kHz")
        print(f"  Grid size: {args.grid_size}×{args.grid_size}")
        print(f"  Output: {output_dir}")
        print()
    
    # Route to appropriate simulation
    if args.compare_all:
        from simulation_modules.geometry_comparison import run_comparison
        run_comparison(args, output_dir)
    
    elif args.monte_carlo:
        from simulation_modules.monte_carlo import run_monte_carlo
        run_monte_carlo(args, output_dir)
    
    elif args.phase_optimize:
        from simulation_modules.phase_optimization import run_phase_optimization
        run_phase_optimization(args, output_dir)
    
    elif args.benchmark:
        from simulation_modules.benchmarks import run_benchmark
        run_benchmark(args, output_dir)
    
    elif args.geometry:
        from simulation_modules.single_geometry import run_single_geometry
        run_single_geometry(args, output_dir)
    
    else:
        print("Error: Must specify --geometry, --compare-all, --monte-carlo, "
              "--phase-optimize, or --benchmark")
        print("Run with --help for usage information")
        sys.exit(1)
    
    if not args.quiet:
        print()
        print("=" * 70)
        print("SIMULATION COMPLETE")
        print(f"Results saved to: {output_dir}")
        print("=" * 70)

if __name__ == '__main__':
    main()