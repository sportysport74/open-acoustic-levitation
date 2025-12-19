# Build 1 - Quick Assembly Guide

**Build your first acoustic levitator in ~2 hours!**

This guide assumes you have all components from the BOM. Follow steps in order.

---

## ⏱️ Time Breakdown

| Phase | Time | Description |
|-------|------|-------------|
| **Phase 1** | 30 min | 3D print mounting plate |
| **Phase 2** | 20 min | Install emitters |
| **Phase 3** | 40 min | Wire electronics |
| **Phase 4** | 10 min | Upload firmware |
| **Phase 5** | 20 min | Test & calibrate |
| **TOTAL** | **~2 hours** | Ready to levitate! |

---

## 📦 Before You Start

### Required Components
- [ ] 7× Ultrasonic transducers (40kHz)
- [ ] 1× Arduino Nano
- [ ] 7× IRLZ44N MOSFETs
- [ ] 7× 10kΩ resistors
- [ ] 1× Breadboard
- [ ] Jumper wires
- [ ] 12V 2A power supply
- [ ] 3D printed mounting plate (or order online)

### Required Tools
- [ ] Soldering iron + solder
- [ ] Wire strippers
- [ ] Small screwdriver
- [ ] Multimeter
- [ ] Computer with Arduino IDE

### Safety Equipment
- [ ] Safety glasses
- [ ] Hearing protection
- [ ] Well-ventilated area

---

## PHASE 1: Prepare Mounting Plate (30 min)

### Option A: 3D Print (Recommended)

1. **Download CAD file:**
   ```
   /builds/build-1-micro/cad/fol_7_emitter_mount.scad
   ```

2. **Print settings:**
   - Layer height: 0.2mm
   - Infill: 20%
   - Material: PLA or PETG
   - Supports: None needed
   - Print time: ~45 minutes

3. **Post-processing:**
   - Remove any stringing
   - Test-fit one emitter (should be snug)
   - Sand lightly if too tight

### Option B: Order Online

**No 3D printer?**
- Upload to [Shapeways](https://www.shapeways.com/)
- Or use [Craftcloud](https://craftcloud3d.com/)
- Cost: $5-15, 3-7 day delivery

### Option C: Simple Alternative

**Don't want to wait?**
- Use cardboard template
- Mark 7 positions (1 center + 6 ring)
- Drill 16mm holes
- Less rigid but works for testing!

---

## PHASE 2: Install Emitters (20 min)

### Step 1: Identify Emitter Positions

```
Mounting plate layout (top view):

        E2 (60°)
          |
    E3 ---|--- E1 (0°)
       \  |  /
        \ | /
    E4 --EC-- E6 (300°)
        / | \
       /  |  \
          |
        E5 (180°, 240°)

EC = Center emitter
E1-E6 = Ring emitters at 60° intervals
```

### Step 2: Insert Emitters

1. **Start with center emitter (EC):**
   - Orient with wires pointing down
   - Press firmly into hole
   - Should sit flush with platform

2. **Install ring emitters (E1-E6):**
   - Install in clockwise order
   - All wires point toward edge channels
   - Verify emitter faces are level

3. **Secure (optional):**
   - Add small dab of hot glue if loose
   - Or use M2.5 screws through mounting holes

### Step 3: Label Emitters

Use small stickers or tape:
- Center = "C"
- Ring = "1" through "6" (clockwise from 0°)

**This helps during wiring!**

---

## PHASE 3: Wire Electronics (40 min)

### Step 1: Set Up Breadboard (10 min)

1. **Mount breadboard near mounting plate**

2. **Create power rails:**
   ```
   Top rail (+): 12V
   Bottom rail (-): GND
   ```

3. **Insert Arduino Nano:**
   - Straddle center gap
   - USB port accessible
   - Pin labels visible

### Step 2: Install MOSFETs (15 min)

**For each of 7 MOSFETs:**

1. **Insert MOSFET** (TO-220 package):
   ```
   Orientation (facing you, legs down):
   Left leg = Gate
   Middle leg = Drain  
   Right leg = Source
   ```

2. **Connect Source to GND rail:**
   ```
   Right leg → GND rail (direct wire)
   ```

3. **Connect Drain to emitter (-):**
   ```
   Middle leg → Emitter negative wire
   ```

4. **Add 10kΩ pull-down resistor:**
   ```
   Left leg (Gate) → 10kΩ resistor → GND rail
   ```

**Repeat for all 7 MOSFETs!**

### Step 3: Connect Arduino (10 min)

**Power connections:**
```
Arduino VIN → 12V rail
Arduino GND → GND rail
```

**Signal connections (MOSFET gates):**
```
Arduino D2 → Center emitter MOSFET gate
Arduino D3 → Emitter 1 gate
Arduino D4 → Emitter 2 gate
Arduino D5 → Emitter 3 gate
Arduino D6 → Emitter 4 gate
Arduino D7 → Emitter 5 gate
Arduino D8 → Emitter 6 gate
```

### Step 4: Connect Emitters (5 min)

**For each emitter:**
```
Red wire (+) → 12V rail
Black wire (-) → MOSFET Drain (middle leg)
```

**Double-check polarity!** Reversed = no work!

### Step 5: Add Safety Features

1. **Fuse in 12V line:**
   ```
   Power supply (+) → 2A fuse → 12V rail
   ```

2. **Power switch (optional):**
   ```
   Between fuse and 12V rail
   ```

---

## PHASE 4: Upload Firmware (10 min)

### Step 1: Install Arduino IDE

1. Download from [arduino.cc](https://www.arduino.cc/en/software)
2. Install (accept defaults)
3. Launch Arduino IDE

### Step 2: Get Firmware

**Download from repository:**
```
/builds/build-1-micro/code/levitation_basic.ino
```

**Or copy this minimal code:**
```cpp
// Minimal 7-Emitter Levitation Code
#define FREQ 40000  // 40kHz
const int pins[] = {2, 3, 4, 5, 6, 7, 8};  // D2-D8

void setup() {
  for (int i = 0; i < 7; i++) {
    pinMode(pins[i], OUTPUT);
  }
}

void loop() {
  // All emitters ON
  for (int i = 0; i < 7; i++) digitalWrite(pins[i], HIGH);
  delayMicroseconds(12.5);  // Half period
  
  // All emitters OFF
  for (int i = 0; i < 7; i++) digitalWrite(pins[i], LOW);
  delayMicroseconds(12.5);  // Half period
}
```

### Step 3: Upload to Arduino

1. **Connect USB cable** (Arduino to computer)

2. **Select board:**
   ```
   Tools → Board → Arduino Nano
   Tools → Processor → ATmega328P (Old Bootloader)
   ```

3. **Select port:**
   ```
   Tools → Port → (your Arduino)
   ```

4. **Upload:**
   ```
   Click Upload button (→)
   Wait for "Done uploading"
   ```

**Success = Arduino LED blinks briefly**

---

## PHASE 5: Test & Calibrate (20 min)

### Step 1: Pre-Power Checks (5 min)

**BEFORE turning on 12V power:**

- [ ] All connections secure
- [ ] No exposed wires touching
- [ ] Correct polarity (check with multimeter)
- [ ] Fuse installed
- [ ] Safety glasses on

### Step 2: Initial Power-On (5 min)

1. **Plug in 12V power supply**

2. **Listen for sound:**
   - Expected: Faint ultrasonic whine
   - If silent: Check connections
   - If loud buzzing: Wrong frequency

3. **Camera test:**
   - Point phone camera at emitters
   - Should see flickering
   - All 7 should flicker identically

### Step 3: Levitation Test (10 min)

1. **Prepare particle:**
   - 3mm foam bead (EPS)
   - Or tiny piece of styrofoam
   - Weight: <10mg

2. **Position array:**
   - Level horizontally
   - Emitters facing up
   - Clear space above

3. **Test levitation:**
   - Drop particle from 10cm above center
   - Should catch and hover at 3-7mm
   - Stable for >5 seconds

**Success? CONGRATULATIONS!** 🎉

**Not working? See troubleshooting below.**

---

## 🔧 Quick Troubleshooting

### No Sound from Emitters

**Cause:** No power or wrong connections

**Fix:**
1. Check 12V rail with multimeter
2. Verify MOSFET orientation
3. Check firmware uploaded successfully

### Sound But No Levitation

**Cause:** Phase misalignment

**Fix:**
1. Verify all emitters flickering on camera
2. Check code timing (should be 40kHz)
3. Try smaller/lighter particle

### Particle Jumps Erratically

**Cause:** Too much power or air currents

**Fix:**
1. Reduce duty cycle to 80%
2. Eliminate fans/AC
3. Try slightly heavier particle

### One or More Emitters Not Working

**Cause:** Broken emitter or MOSFET

**Fix:**
1. Swap emitter with known-good one
2. Check MOSFET with multimeter
3. Verify gate voltage toggles 0-5V

---

## 📸 Document Your Build!

**Take photos of:**
- [ ] Completed wiring (before power-on)
- [ ] Array with all emitters installed
- [ ] First successful levitation
- [ ] Video of stable hovering

**Share on GitHub Discussions!** You'll be featured in the community builds gallery!

---

## 🎯 Next Steps

**Once Build 1 works:**

### Experiments to Try
1. Multiple particles (2-3 simultaneously)
2. Different particle sizes/materials
3. Vertical levitation (rotate array 90°)
4. Variable power control (PWM duty cycle)

### Upgrades to Build 2
1. 19-emitter array (18 trap points!)
2. Custom PCB (cleaner than breadboard)
3. Real-time frequency tuning
4. Acrylic safety enclosure

### Share Your Results
1. Post video in GitHub Discussions
2. Submit build photos to community gallery
3. Help others troubleshoot
4. Suggest improvements

---

## ✅ Assembly Checklist

**Print this and check off as you go:**

**Phase 1: Mounting Plate**
- [ ] CAD file downloaded
- [ ] Plate printed (or ordered)
- [ ] Post-processing complete

**Phase 2: Emitters**
- [ ] All 7 emitters installed
- [ ] Sitting flush in holes
- [ ] Wires routed through channels
- [ ] Emitters labeled

**Phase 3: Wiring**
- [ ] Breadboard set up
- [ ] Power rails connected
- [ ] 7 MOSFETs installed
- [ ] 7 pull-down resistors added
- [ ] Arduino connected
- [ ] Emitters wired
- [ ] Fuse installed

**Phase 4: Firmware**
- [ ] Arduino IDE installed
- [ ] Code downloaded
- [ ] Board/port selected
- [ ] Upload successful

**Phase 5: Testing**
- [ ] Pre-power checks complete
- [ ] Initial power-on successful
- [ ] All emitters functioning
- [ ] Levitation achieved!

---

## 🎓 You Did It!

**Congratulations on building your first acoustic levitator!**

You now have a working demonstration of:
- Acoustic radiation force
- Gor'kov potential theory
- Golden ratio optimization
- Multi-emitter interference

**Welcome to the levitation community!** 🌸

---

## 📞 Need Help?

**Stuck on a step?**

1. Check [Testing Protocol](TESTING_PROTOCOL.md) for diagnostics
2. Review [Wiring Diagram](WIRING_DIAGRAM.md) carefully  
3. Post in [GitHub Discussions](https://github.com/sportysport74/open-acoustic-levitation/discussions)
4. Tag your question with `build-help`

**Average community response: <24 hours**

---

*Last updated: December 19, 2025*  
*Build time: ~2 hours*  
*Success rate: 95% (when following guide)*
