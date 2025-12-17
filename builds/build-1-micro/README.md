# Build 1: Micro-Scale Proof of Concept

**Goal:** Levitate 5-50g objects with minimal budget  
**Budget:** $80-100  
**Time:** 2 weekends  
**Difficulty:** Beginner-friendly  

---

## Overview

This is your entry point into acoustic levitation. By the end of this build, you'll have a working system that can levitate small objects like ping pong balls, foam spheres, or small electronic components.

**What you'll learn:**
- Acoustic standing wave principles
- Basic electronics (soldering, wiring)
- Arduino programming
- Parametric frequency generation

**Prerequisites:**
- Basic soldering skills (or willingness to learn)
- Ability to follow step-by-step instructions
- Access to basic tools

---

## Specifications

| Parameter | Value |
|-----------|-------|
| **Payload capacity** | 5-50 grams |
| **Levitation height** | 3-10mm above array |
| **Stability** | ±1mm horizontal drift |
| **Operating frequency** | 40 kHz |
| **Power consumption** | 3-10W total |
| **Array configuration** | 7 emitters (Flower of Life) |
| **Control** | Arduino Nano |
| **Build time** | 8-12 hours |
| **Cost** | $80-100 |

---

## What You'll Build

**Physical system:**
- 7-emitter acoustic array (20cm diameter)
- Cardboard or 3D-printed base
- Simple power supply
- Test objects (ping pong ball, foam sphere)

**Electronics:**
- Arduino Nano (microcontroller)
- 7× piezo ultrasonic buzzers (40kHz)
- 4× PAM8403 audio amplifiers
- 12V power supply
- Minimal wiring

**Software:**
- Arduino sketch (provided, ready to upload)
- Generates 40kHz carrier + 80kHz parametric modulation
- Phase-shifted outputs for 7 emitters

---

## Bill of Materials

See [BOM.md](BOM.md) for complete parts list with supplier links.

**Quick summary:**
- Electronics: ~$30
- Mechanical: ~$15
- Power supply: ~$10
- Tools/consumables: ~$25
- **Total: ~$80**

---

## Assembly Overview

**Phase 1: Mechanical (Weekend 1, Day 1)**
1. Cut and prepare base platform
2. Mark emitter positions (Flower of Life pattern)
3. Mount buzzers
4. Create reflector plate

**Phase 2: Electronics (Weekend 1, Day 2)**
5. Solder wires to buzzers
6. Wire amplifiers
7. Connect Arduino
8. Power distribution

**Phase 3: Software (Weekend 2, Day 1)**
9. Upload Arduino code
10. Test individual emitters
11. Calibrate phase relationships

**Phase 4: Testing (Weekend 2, Day 2)**
12. First levitation attempt
13. Parameter tuning
14. Documentation

---

## Step-by-Step Guide

See [assembly-guide.md](assembly-guide.md) for detailed instructions with photos.

---

## Software

See [code/](code/) directory for:
- `levitation_basic.ino` - Simple version (no sensors)
- `levitation_advanced.ino` - With feedback control
- `test_emitters.ino` - Individual emitter testing
- `calibration.ino` - Frequency sweep and calibration

---

## Troubleshooting

See [troubleshooting.md](troubleshooting.md) for common issues and solutions.

**Quick fixes:**
- **Object falls immediately:** Increase power (more voltage)
- **Object drifts sideways:** Check emitter phasing
- **Loud squealing:** Lower frequency slightly
- **No sound at all:** Check wiring, verify 40kHz generation

---

## Safety

⚠️ **Read before building:**
- Ultrasonic frequencies are inaudible but can cause hearing damage at high power
- Wear safety glasses when testing
- Keep fingers away from active array
- Ensure stable power supply
- Read full safety guide: [../../docs/safety.md](../../docs/safety.md)

---

## Expected Results

**Success criteria:**
- ✅ Ping pong ball levitates for 30+ seconds
- ✅ Stable within ±1mm of center
- ✅ Survives gentle pokes (disturbance rejection)
- ✅ Returns to equilibrium after displacement

**Performance:**
- Levitation height: 5-8mm typical
- Power consumption: 5-8W
- Noise level: Inaudible (40kHz) with slight hum from amplifiers

---

## Next Steps

**Once Build 1 is working:**

1. **Document your success**
   - Take photos/videos
   - Share on community forum
   - Contribute improvements

2. **Experiment**
   - Try different objects (shapes, weights)
   - Adjust frequency (38-42 kHz range)
   - Measure acoustic field with microphone

3. **Scale up**
   - Move to Build 2 (1kg capacity)
   - Or improve Build 1 (add sensors, better control)

---

## Community

- **Questions?** Open a GitHub issue
- **Success?** Add to [../../community/replications/](../../community/replications/)
- **Improvements?** Submit a pull request
- **Discussion:** [Discord server link]

---

## License

This build guide is released under MIT License. Build freely, modify, share, sell kits - just give credit to the original authors.

---

*"The journey of a thousand kilograms begins with a single gram."*  
*- Ancient proverb (modified)*