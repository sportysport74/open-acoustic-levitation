# Build 2: Lab-Scale Demonstrator (1kg Capacity)

**Status:** Design complete, community testing in progress  
**Budget:** $1,500-2,000  
**Difficulty:** Intermediate  
**Timeline:** 5 weeks

---

## Overview

Build 2 scales up from proof-of-concept to serious lab equipment. Levitate objects from 0.5kg to 2kg with sub-millimeter stability. Features FPGA control, professional transducers, and sensor feedback.

**Specifications:**
- Payload: 0.5-2kg
- Height: 10-30mm
- Stability: <0.5mm RMS
- Power: 100-300W
- Array: 7× 40W Langevin transducers
- Control: FPGA (Xilinx Artix-7)
- Sensors: Distance, current, IMU

---

## What's Different from Build 1?

| Feature | Build 1 | Build 2 |
|---------|---------|---------|
| **Transducers** | Piezo buzzers ($1) | Langevin (40W, $85) |
| **Control** | Arduino Nano | FPGA (Arty A7) |
| **Amplifiers** | PAM8403 (3W) | Modified Behringer A800 |
| **Power** | 12V 2A (24W) | 48V 80A (3.8kW capable) |
| **Sensors** | None | Distance, current, IMU |
| **Stability** | ±1mm | <0.5mm RMS |
| **Complexity** | Weekend project | 5-week build |

---

## Key Innovations

**1. Langevin Transducers**
- Industrial ultrasonic design
- 40W continuous output
- Efficient coupling
- Robust construction

**2. FPGA Control**
- 10kHz control loop (vs 1kHz Arduino)
- Hardware PLL for phase-locking
- Real-time sensor fusion
- Precise timing (nanosecond resolution)

**3. Closed-Loop Feedback**
- Distance sensors measure height
- IMU tracks tilt/acceleration
- Current sensors monitor power
- LQR controller for optimal response

**4. Parametric Enhancement**
- Software-configurable modulation
- Adaptive epsilon (adjusts to load)
- Frequency tracking
- Resonance optimization

---

## Bill of Materials

**Complete BOM:** See `BOM.md` in this directory

**Major components:**
- 7× Steminc SMC4028S40F1 transducers: ~$595
- Digilent Arty A7-35T FPGA board: $129
- 4× Behringer A800 amplifiers (modified): ~$800
- 3× MeanWell 48V 80A power supplies: ~$450
- Sensors, wiring, mechanical: ~$300

**Total: ~$1,900**

---

## Assembly Process

**Phase 1: Mechanical (Week 1)**
- CNC aluminum base plate
- Mount transducers with precision
- Build enclosure

**Phase 2: Electronics (Week 2-3)**
- Modify amplifiers for 40kHz
- Wire power distribution
- Connect sensors
- FPGA setup

**Phase 3: Software (Week 3-4)**
- Verilog HDL for signal generation
- Python control interface
- Calibration routines

**Phase 4: Testing (Week 4-5)**
- Staged power-up
- Frequency optimization
- Control loop tuning
- Performance validation

**Full guide:** `assembly-guide.md` (coming soon)

---

## Expected Performance

**Levitation metrics:**
- 500g object: 15-25mm height, <0.3mm RMS stability
- 1kg object: 12-20mm height, <0.5mm RMS stability
- 2kg object: 10-15mm height, <0.8mm RMS stability

**System performance:**
- Settling time: <3 seconds
- Disturbance rejection: 5mm displacement recovers in 2s
- Continuous operation: 4+ hours
- Power efficiency: 150-300W depending on mass

---

## Applications

**Research:**
- Containerless processing (no contact with walls)
- Drug crystallization studies
- Acoustic field mapping
- Educational demonstrations

**Development:**
- Test platform for advanced control algorithms
- Sensor fusion research
- Parametric optimization studies
- Proof-of-concept for industrial systems

---

## Prerequisites

**Required skills:**
- Electronics (intermediate soldering, circuit debugging)
- Programming (Verilog basics, Python)
- Mechanical (drilling, measuring, assembly)
- Safety (understand high-power operation)

**Required tools:**
- Soldering station
- Oscilloscope (100MHz)
- Multimeter
- Drill press or CNC
- Basic hand tools

**Recommended experience:**
- Completed Build 1 successfully
- FPGA development (or willing to learn)
- Power electronics basics
- Lab safety training

---

## Status and Community

**Design status:** ✅ Complete, validated  
**Documentation:** 🔄 In progress  
**Community builds:** 🔄 Testing phase  

**Next steps:**
1. Complete assembly guide
2. Release FPGA code
3. Validation by 3+ independent builders
4. Iterate based on feedback

---

## Get Started

**Ready to build?**
1. Read `BOM.md` for parts list
2. Review `theory/04-scaling-laws.md` for understanding
3. Join Discord #build-2 channel
4. Order parts (8-week lead time for transducers)
5. Follow updates in repository

**Questions?** Open GitHub issue tagged "build-2"

---

*Full documentation coming soon. Watch repository for updates.*