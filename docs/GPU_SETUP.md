# GPU Setup Guide for Open Acoustic Levitation
# ==============================================

This guide helps you set up GPU acceleration for running the advanced simulations.

## Quick Start

**If you just want to run the simulations (CPU is fine!):**
```bash
pip install -r requirements.txt
python simulations/monte_carlo_statistical_comparison.py
```

**If you have an NVIDIA GPU and want MAXIMUM SPEED:**
Follow the steps below!

---

## GPU Requirements

### Hardware
- NVIDIA GPU with CUDA support (RTX 5090/4090/3090/etc)
- 8GB+ VRAM recommended (16GB+ for mega simulations)

### Software
- NVIDIA GPU drivers (latest)
- CUDA Toolkit (13.0+ for RTX 50-series, 12.1+ for RTX 40/30-series)
- Python 3.8+

---

## Installation Steps

### Step 1: Verify GPU & CUDA

**Windows:**
```powershell
nvidia-smi
nvcc --version
```

**Linux:**
```bash
nvidia-smi
nvcc --version
```

**Expected output:**
- `nvidia-smi` shows your GPU name
- `nvcc` shows CUDA version (e.g., "release 13.0")

**If either command fails:**
- Install NVIDIA drivers: https://www.nvidia.com/Download/index.aspx
- Install CUDA Toolkit: https://developer.nvidia.com/cuda-downloads

---

### Step 2: Install PyTorch with GPU Support

**Choose the command for YOUR CUDA version:**

**CUDA 13.x (RTX 5090, RTX 50-series):**
```bash
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu130
```

**CUDA 12.1 (RTX 4090, RTX 40-series, RTX 3090, RTX 30-series):**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

**CUDA 11.8 (RTX 20-series, GTX 16-series):**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

### Step 3: Install Other Requirements

```bash
pip install -r requirements.txt
```

---

### Step 4: Verify GPU Detection

```bash
python -c "import torch; print('CUDA Available:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'No GPU')"
```

**Expected output:**
```
CUDA Available: True
GPU: NVIDIA GeForce RTX 5090
```

**If you see "CUDA Available: False":**
- You installed CPU-only PyTorch (go back to Step 2)
- CUDA drivers not installed properly
- PyTorch version doesn't match your CUDA version

---

## Running GPU Simulations

### Mega Monte Carlo (10,000 trials)

**GPU (recommended):**
```bash
cd simulations
python gpu_accelerated_suite.py
# Choose option 1 or 3
```

**Runtime:**
- RTX 5090: ~30 seconds
- RTX 4090: ~45 seconds
- RTX 3090: ~60 seconds

**CPU fallback (if GPU fails):**
```bash
python enhanced_monte_carlo_cpu.py  # 500 trials in ~10 minutes
```

### 37-Emitter Ultra-High-Res

**GPU only:**
```bash
cd simulations
python gpu_accelerated_suite.py
# Choose option 2 or 3
```

**Runtime:**
- RTX 5090: <1 second
- RTX 4090: ~2 seconds
- RTX 3090: ~3 seconds

---

## Troubleshooting

### "CUDA out of memory"

**Solution:** Reduce parameters in the script:
```python
# In gpu_accelerated_suite.py, change:
N_TRIALS = 5000  # Instead of 10000
GRID_SIZE = 150  # Instead of 200
```

### "Torch not compiled with CUDA enabled"

**Cause:** You have CPU-only PyTorch

**Solution:**
```bash
pip uninstall torch torchvision torchaudio -y
# Then reinstall with GPU support (see Step 2)
```

### "nvcc: command not found"

**Cause:** CUDA Toolkit not installed

**Solution:**
1. Download CUDA Toolkit: https://developer.nvidia.com/cuda-downloads
2. Install it
3. Reboot
4. Verify: `nvcc --version`

### GPU detected but simulations crash

**Possible causes:**
- Outdated GPU drivers
- CUDA version mismatch

**Solution:**
```bash
# Update GPU drivers
# Windows: GeForce Experience or nvidia.com
# Linux: sudo ubuntu-drivers autoinstall

# Verify CUDA version matches PyTorch
nvcc --version  # Should match cu130, cu121, etc.
```

### Very slow on GPU (slower than CPU)

**Cause:** Data transfer overhead for small problems

**Solution:** GPU shines on large problems:
- Use 10,000+ Monte Carlo trials
- Use 400×400 grids or larger
- Smaller problems run fine on CPU!

---

## Performance Benchmarks

**Monte Carlo (10,000 trials, 200×200 grid):**
| Hardware | Time | Speedup |
|----------|------|---------|
| CPU (AMD Ryzen 9) | ~6 hours | 1× |
| RTX 3090 | ~60 sec | 360× |
| RTX 4090 | ~45 sec | 480× |
| RTX 5090 | ~31 sec | 697× |

**37-Emitter (400×400 grid, 160K points):**
| Hardware | Time | Speedup |
|----------|------|---------|
| CPU | ~8 hours | 1× |
| RTX 3090 | ~3 sec | 9,600× |
| RTX 4090 | ~2 sec | 14,400× |
| RTX 5090 | <1 sec | 28,800× |

---

## Alternative: Use Google Colab (FREE GPU!)

**No GPU? Use Google's for free:**

1. Upload `simulations/` folder to Google Drive
2. Open Google Colab: https://colab.research.google.com/
3. Enable GPU: Runtime → Change runtime type → GPU → T4
4. Run:
```python
from google.colab import drive
drive.mount('/content/drive')

%cd /content/drive/MyDrive/simulations
!pip install torch torchvision

!python gpu_accelerated_suite.py
```

**Free tier limits:**
- ~12 hours GPU time per day
- T4 GPU (slower than RTX, but FREE!)

---

## Need Help?

**GPU not working?**
1. Check this guide first
2. Search existing issues: https://github.com/sportysport74/open-acoustic-levitation/issues
3. Open new issue with:
   - Output of `nvidia-smi`
   - Output of `nvcc --version`
   - Output of GPU detection test
   - Error message

**CPU simulations work fine!**
- GPU is optional for extra speed
- All science is valid on CPU
- 100-500 trial Monte Carlo is still excellent!

---

*Last updated: December 19, 2025*
*Tested on: RTX 5090, RTX 4090, RTX 3090*