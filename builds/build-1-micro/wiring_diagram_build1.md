# Build 1 - Wiring Diagram (7-Emitter Array)

## 🔌 Complete Electrical Connections

### Hardware Required
- 7× HC-SR04 ultrasonic transducers (40kHz)
- 1× Arduino Nano
- 7× N-Channel MOSFETs (IRLZ44N or similar, logic-level)
- 7× 10kΩ resistors (pull-down)
- 1× 12V 2A power supply
- Jumper wires (22 AWG recommended)
- Breadboard or prototype PCB

---

## 📊 Connection Table

### Emitter Connections

| Emitter | Position | Arduino Pin | MOSFET Gate | Power | Ground |
|---------|----------|-------------|-------------|-------|--------|
| **Center** | 0° | D2 | Q1 Gate | 12V | GND |
| **Ring 1** | 0° | D3 | Q2 Gate | 12V | GND |
| **Ring 2** | 60° | D4 | Q3 Gate | 12V | GND |
| **Ring 3** | 120° | D5 | Q4 Gate | 12V | GND |
| **Ring 4** | 180° | D6 | Q5 Gate | 12V | GND |
| **Ring 5** | 240° | D7 | Q6 Gate | 12V | GND |
| **Ring 6** | 300° | D8 | Q7 Gate | 12V | GND |

### MOSFET Connections (Per Channel)

```
Arduino Pin → 10kΩ Resistor → MOSFET Gate
                               MOSFET Source → GND
                               MOSFET Drain → Emitter (-) terminal
12V Supply → Emitter (+) terminal
```

---

## 🔧 Detailed Wiring Schematic (ASCII)

```
                    +12V POWER SUPPLY
                          |
                          +--------------------------+
                          |                          |
                    +-----+-----+              +-----+-----+
                    |           |              |           |
                [Emitter C]  [Emitter 1]   [Emitter 2] ... [Emitter 6]
                    |  +        |  +           |  +
                    |  |        |  |           |  |
                    |  +--------+--+-----------+--+--- 12V Rail
                    |           |              |
                    |-          |-             |-
                    |           |              |
                    D           D              D
                   /|          /|             /|
                  / |         / |            / |
            G ---+  |    G --+  |       G --+  |
                 |  |        |  |           |  |
                 |  S        |  S           |  S
                 |  |        |  |           |  |
                 |  +--------+--+-----------+--+--- GND Rail
                 |           |              |
              10kΩ        10kΩ           10kΩ
                 |           |              |
                 +--------+--+-----------+--+--- GND
                          |
        +----------------+|
        |                 |
    [Arduino Nano]        |
        |                 |
    D2  +-----------------+  (Center emitter)
    D3  +--------------------+ (Ring emitter 1)
    D4  +--------------------+ (Ring emitter 2)
    D5  +--------------------+ (Ring emitter 3)
    D6  +--------------------+ (Ring emitter 4)
    D7  +--------------------+ (Ring emitter 5)
    D8  +--------------------+ (Ring emitter 6)
        |
    GND +--------+
                 |
    VIN +--------+--- 12V (from power supply)
                      
```

---

## ⚡ Power Distribution

### Power Requirements
- Per emitter: ~1.5W @ 12V = 125mA
- Total (7 emitters): 10.5W = 875mA
- **Recommended supply:** 12V 2A (leaves headroom)

### Power Bus Layout
```
12V Supply (+) ──┬── Emitter C (+)
                 ├── Emitter 1 (+)
                 ├── Emitter 2 (+)
                 ├── Emitter 3 (+)
                 ├── Emitter 4 (+)
                 ├── Emitter 5 (+)
                 └── Emitter 6 (+)

GND Rail ────────┬── All MOSFET Sources
                 ├── All 10kΩ resistors
                 ├── Arduino GND
                 └── Power Supply GND
```

---

## 🎛️ Control Signal Phase Alignment

### Phase Relationships (Critical!)

**All emitters MUST be in-phase for constructive interference!**

| Emitter | Phase | Arduino Signal |
|---------|-------|----------------|
| All 7 | 0° | Synchronized PWM @ 40kHz |

**Implementation in code:**
```cpp
// All pins driven identically
digitalWrite(D2, HIGH);
digitalWrite(D3, HIGH);
digitalWrite(D4, HIGH);
digitalWrite(D5, HIGH);
digitalWrite(D6, HIGH);
digitalWrite(D7, HIGH);
digitalWrite(D8, HIGH);
delayMicroseconds(12.5); // Half period @ 40kHz
```

---

## 🧪 Testing & Verification

### Step 1: Continuity Check
1. Power OFF
2. Multimeter in continuity mode
3. Verify each MOSFET drain connects to emitter (-)
4. Verify all emitter (+) connect to 12V rail
5. Verify all grounds connected

### Step 2: Power Test
1. **Disconnect emitters** temporarily
2. Power ON (12V supply)
3. Measure Arduino VIN: Should read ~12V
4. Measure 12V rail: Should read 12V
5. Upload test sketch (single pin toggle)
6. Verify MOSFET switching with multimeter

### Step 3: Phase Verification (Requires Oscilloscope)
1. Connect all emitters
2. Upload synchronous PWM code
3. Probe any two emitter signals simultaneously
4. **Must be perfectly aligned** (±5μs tolerance)
5. If misaligned: Check for wire length differences

### Step 4: Acoustic Test
1. Power ON with all emitters connected
2. Should hear faint ultrasonic whine
3. Use phone camera: Emitters should flicker in unison
4. Place foam bead above center: Should levitate!

---

## 🚨 Safety Warnings

**BEFORE POWERING ON:**
- [ ] Double-check all connections
- [ ] Verify MOSFET orientation (check datasheet)
- [ ] Ensure power supply is 12V DC (NOT AC!)
- [ ] Add fuse (2A) in 12V line
- [ ] Keep fingers away from emitters during operation

**HIGH VOLTAGE PRESENT:**
- MOSFETs can generate 100V+ spikes during switching
- Use snubber diodes across emitters if experiencing EMI
- Keep setup away from sensitive electronics

**HEARING PROTECTION:**
- 40kHz is "ultrasonic" but harmonics are audible
- Limit exposure to <15 minutes per hour
- Never operate at full power near ears

---

## 🔍 Troubleshooting

### No Levitation

**Symptom:** Emitters make sound but no trapping
**Causes:**
1. Phase misalignment (most common)
   - Solution: Verify with oscilloscope, fix code timing
2. Insufficient power
   - Solution: Upgrade to 12V 3A supply
3. Wrong frequency
   - Solution: Verify 40kHz with frequency counter

### Emitters Not Activating

**Symptom:** No sound from emitters
**Causes:**
1. MOSFET not switching
   - Check gate voltage: Should toggle 0V/5V
   - Verify MOSFET orientation
2. Broken emitter
   - Swap with known-good emitter
3. Power supply failure
   - Check 12V rail with multimeter

### Overheating

**Symptom:** MOSFETs or emitters getting hot
**Causes:**
1. Excessive duty cycle
   - Reduce to 80% max
2. Insufficient heatsinking
   - Add heatsinks to MOSFETs
3. Shorted emitter
   - Disconnect and test each individually

### Erratic Behavior

**Symptom:** Intermittent levitation
**Causes:**
1. Loose connections
   - Solder all critical joints
2. EMI from switching
   - Add 0.1μF capacitors across emitters
3. Power supply ripple
   - Add 1000μF capacitor to 12V rail

---

## 📸 Photos (To Be Added)

*Upload your wiring photos to help others!*

**Needed:**
- Breadboard layout (top view)
- MOSFET connections (close-up)
- Power distribution (annotated)
- Final assembly

**Submit to:** `/community/builds/build-1-wiring/`

---

## 🔗 Related Files

- **Firmware:** `/builds/build-1-micro/code/levitation_basic.ino`
- **CAD Model:** `/builds/build-1-micro/cad/fol_7_emitter_mount.scad`
- **BOM:** `/builds/build-1-micro/BOM.csv`
- **Theory:** `/theory/01-fundamental-physics.md`

---

## ✅ Pre-Flight Checklist

Before first power-on:

- [ ] All emitter (+) connected to 12V rail
- [ ] All emitter (-) connected to MOSFET drains
- [ ] All MOSFET sources connected to GND
- [ ] All MOSFET gates have 10kΩ pull-down resistors
- [ ] Arduino D2-D8 connected to MOSFET gates
- [ ] Arduino VIN connected to 12V
- [ ] Arduino GND connected to GND rail
- [ ] Power supply is 12V DC, 2A minimum
- [ ] Fuse (2A) in 12V line
- [ ] Firmware uploaded and verified
- [ ] Workspace clear of flammable materials
- [ ] Safety glasses on
- [ ] Hearing protection available

**Only power ON when ALL boxes checked!**

---

*Last updated: December 19, 2025*
*Version: 1.0*
*Questions? Open an issue on GitHub*
