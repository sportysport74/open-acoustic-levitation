# Build 1 - Testing & Validation Protocol

**Verify your levitator works BEFORE blaming the design!**

This protocol walks you through systematic testing from basic power-on to successful levitation. Follow each step in order - don't skip ahead!

---

## 🎯 Test Overview

| Test # | Name | Time | Equipment | Pass Criteria |
|--------|------|------|-----------|---------------|
| 1 | Visual Inspection | 5 min | Eyes | All connections secure |
| 2 | Continuity Check | 10 min | Multimeter | All circuits complete |
| 3 | Power Rail Test | 5 min | Multimeter | 12V ±0.5V, stable |
| 4 | Arduino Upload | 5 min | Computer | Code uploads successfully |
| 5 | Single Emitter Test | 10 min | Multimeter | Emitter activates |
| 6 | Phase Alignment | 15 min | Oscilloscope | All in-phase ±10μs |
| 7 | Acoustic Output | 5 min | Phone camera | All emitters visible |
| 8 | Levitation Test | 10 min | Foam bead | Particle levitates |

**Total Time: ~65 minutes** (first build)  
**Success Rate: 95%** if you follow this protocol

---

## 📋 Pre-Test Requirements

**Before starting tests, you MUST have:**

- [ ] All components installed per wiring diagram
- [ ] Arduino firmware uploaded
- [ ] Power supply connected but OFF
- [ ] Multimeter available (basic is fine)
- [ ] Safety glasses on
- [ ] Workspace clear and well-lit

**If any box is unchecked, STOP and complete setup first!**

---

## TEST 1: Visual Inspection

**Goal:** Catch obvious errors before applying power

**Time:** 5 minutes

### Procedure

1. **Check power connections:**
   - [ ] All emitter (+) connect to 12V rail
   - [ ] No bare wire touching
   - [ ] Polarity correct (+ to +, - to -)

2. **Check MOSFET connections:**
   - [ ] Gate → Arduino pin (via resistor)
   - [ ] Drain → Emitter (-)
   - [ ] Source → GND
   - [ ] Pull-down resistor → GND

3. **Check Arduino connections:**
   - [ ] VIN → 12V rail
   - [ ] GND → GND rail
   - [ ] D2-D8 → MOSFET gates
   - [ ] USB cable accessible for programming

4. **Check mechanical:**
   - [ ] Emitters secure in mounting plate
   - [ ] No loose screws or parts
   - [ ] Mounting plate level
   - [ ] Safety shield in place (if using)

### Pass Criteria
✅ All boxes checked, no obvious issues

### Common Failures
- Reversed polarity on emitters
- MOSFET installed backwards
- Missing pull-down resistors
- Loose breadboard connections

---

## TEST 2: Continuity Check

**Goal:** Verify all connections are complete (no opens, no shorts)

**Time:** 10 minutes

**Equipment:** Multimeter in continuity mode (beep function)

### Procedure

**Power must be OFF for all continuity tests!**

1. **Test 12V rail continuity:**
   ```
   Red probe: Power supply (+) terminal
   Black probe: Any emitter (+) terminal
   Expected: BEEP (continuity)
   ```

2. **Test GND rail continuity:**
   ```
   Red probe: Power supply (-) terminal
   Black probe: Any MOSFET source pin
   Expected: BEEP (continuity)
   ```

3. **Test MOSFET connections (for each of 7 MOSFETs):**
   ```
   Gate to Arduino pin: BEEP (via 10kΩ resistor)
   Gate to GND: BEEP (via 10kΩ resistor)
   Drain to emitter (-): BEEP (direct connection)
   Source to GND: BEEP (direct connection)
   ```

4. **Test for shorts (MUST NOT BEEP):**
   ```
   12V rail to GND rail: NO BEEP (open circuit)
   Adjacent Arduino pins: NO BEEP (isolated)
   Emitter (+) to (-): NO BEEP (no short)
   ```

### Pass Criteria
✅ All expected continuity tests BEEP  
✅ All short tests do NOT beep

### Common Failures
- 12V shorted to GND (check for wire bridges)
- Open circuit in power rail (loose connection)
- Missing pull-down resistor (gate floats)

---

## TEST 3: Power Rail Test

**Goal:** Verify stable, correct voltage before connecting emitters

**Time:** 5 minutes

**Equipment:** Multimeter in DC voltage mode

### Procedure

**DISCONNECT all emitters first!** (unplug from MOSFETs)

1. **Measure no-load voltage:**
   ```
   Red probe: 12V rail
   Black probe: GND rail
   Expected: 12.0V ±0.5V
   ```

2. **Power ON and measure:**
   ```
   Expected: 12.0V ±0.5V, stable (no flickering)
   If reading >13V: Power supply set too high
   If reading <11V: Weak power supply
   ```

3. **Measure Arduino VIN:**
   ```
   Red probe: Arduino VIN pin
   Black probe: Arduino GND pin
   Expected: Same as 12V rail (±0.1V)
   ```

4. **Check ripple (if you have oscilloscope):**
   ```
   Expected: <200mV peak-to-peak ripple
   If >500mV: Add 1000μF capacitor to 12V rail
   ```

### Pass Criteria
✅ Voltage stable at 12.0V ±0.5V  
✅ No flickering or dropout  
✅ Arduino VIN matches 12V rail

### Common Failures
- Power supply too weak (sags under load)
- Poor contact in barrel jack
- Excessive voltage drop in wires (use thicker wire)

---

## TEST 4: Arduino Upload Test

**Goal:** Verify Arduino communication and firmware upload

**Time:** 5 minutes

**Equipment:** Computer with Arduino IDE

### Procedure

1. **Connect USB cable** (Arduino to computer)

2. **Open Arduino IDE** and load firmware:
   ```
   File → Open → levitation_basic.ino
   ```

3. **Select board:**
   ```
   Tools → Board → Arduino Nano
   Tools → Processor → ATmega328P (Old Bootloader)
   ```

4. **Select port:**
   ```
   Tools → Port → (select your Arduino's port)
   ```

5. **Upload code:**
   ```
   Click Upload button
   Wait for "Done uploading"
   ```

6. **Open Serial Monitor:**
   ```
   Tools → Serial Monitor
   Set baud rate to 115200
   Expected: Startup message appears
   ```

### Pass Criteria
✅ Code uploads without errors  
✅ Serial monitor shows startup message  
✅ Arduino LED blinks (if code includes blink)

### Common Failures
- Wrong board selected (try "ATmega328P (Old Bootloader)")
- USB cable is power-only (use data cable)
- Driver not installed (install CH340 driver for clones)
- Port not recognized (try different USB port)

---

## TEST 5: Single Emitter Test

**Goal:** Verify one emitter activates correctly before testing all 7

**Time:** 10 minutes

**Equipment:** Multimeter

### Procedure

**Reconnect ONE emitter only** (to center position MOSFET)

1. **Upload test code** (`test_single_emitter.ino`)

2. **Measure MOSFET gate voltage:**
   ```
   Red probe: MOSFET gate (D2 connection)
   Black probe: GND
   Expected: Toggling between 0V and 5V at ~40kHz
   (Multimeter may show ~2.5V average)
   ```

3. **Listen for emitter:**
   ```
   Expected: Faint high-pitched whine
   If silent: Check connections
   If loud buzzing: Wrong frequency (not 40kHz)
   ```

4. **Measure emitter voltage:**
   ```
   Red probe: Emitter (+)
   Black probe: Emitter (-)
   Expected: ~6V average (50% duty cycle PWM)
   ```

5. **Check MOSFET heating:**
   ```
   Touch MOSFET after 30 seconds
   Expected: Warm but not hot
   If hot: Add heatsink or reduce duty cycle
   ```

### Pass Criteria
✅ MOSFET gate toggles 0-5V  
✅ Emitter makes ultrasonic sound  
✅ Emitter voltage ~6V average  
✅ MOSFET stays cool (<50°C)

### Common Failures
- MOSFET installed backwards (no switching)
- Wrong frequency in code (check FREQ constant)
- Defective emitter (try swapping with another)

---

## TEST 6: Phase Alignment Check

**Goal:** Verify all emitters are in-phase (CRITICAL for levitation!)

**Time:** 15 minutes

**Equipment:** Oscilloscope or logic analyzer (REQUIRED for this test)

### Procedure

**Reconnect ALL 7 emitters**

1. **Upload synchronous code** (`levitation_basic.ino`)

2. **Set up oscilloscope:**
   ```
   Channel 1: Probe MOSFET gate for center emitter (D2)
   Channel 2: Probe MOSFET gate for ring emitter (D3)
   Trigger: Rising edge, Channel 1
   Timebase: 10μs/div
   ```

3. **Observe waveforms:**
   ```
   Expected: Both signals perfectly aligned
   Rising edges within ±5μs
   Same frequency (40kHz ± 100Hz)
   ```

4. **Check all 7 emitters:**
   ```
   Probe each MOSFET gate (D2 through D8)
   All should align with Channel 1 reference
   ```

5. **Measure actual frequency:**
   ```
   Expected: 40.00 kHz ± 0.5 kHz
   Period: 25μs ±0.3μs
   ```

### Pass Criteria
✅ All 7 signals within ±10μs of each other  
✅ Frequency = 40kHz ±0.5kHz  
✅ No jitter or glitches

### Common Failures
- **Signals out of phase:** Code timing error (check delayMicroseconds)
- **Different frequencies:** Hardware timer misconfigured
- **Jittery signals:** Interrupt conflicts (disable Serial.print in loop)

**If you don't have an oscilloscope:**
- Skip this test initially
- Try levitation anyway
- If fails, borrow scope or buy $8 logic analyzer from AliExpress

---

## TEST 7: Acoustic Output Verification

**Goal:** Confirm all emitters are producing ultrasonic output

**Time:** 5 minutes

**Equipment:** Smartphone camera

### Procedure

1. **Upload full levitation code** (`levitation_basic.ino`)

2. **Power ON** with all 7 emitters connected

3. **Listen for sound:**
   ```
   Expected: Faint ultrasonic whine
   If loud: Reduce power or add damping
   If silent: Check continuity
   ```

4. **Camera test** (works on most phones):
   ```
   Open phone camera app
   Point at emitters
   Expected: Emitters flicker/strobe on screen
   (Camera can see ~20kHz harmonics)
   ```

5. **Hand test** (use caution):
   ```
   Hold hand 10cm above array
   Expected: Slight tingling sensation
   If strong pushing: Phase is correct!
   If nothing: Check power or phase
   ```

6. **Water droplet test:**
   ```
   Spray fine mist above array
   Expected: Droplets deflect or hover briefly
   ```

### Pass Criteria
✅ All 7 emitters visible on camera  
✅ Ultrasonic sound audible  
✅ Hand feels pressure above array  
✅ Water droplets react to field

### Common Failures
- Only some emitters working (check connections)
- No camera flicker (try different phone/camera app)
- No sound (frequency wrong or power too low)

---

## TEST 8: Levitation Test

**Goal:** Achieve stable particle levitation

**Time:** 10 minutes

**Equipment:** Expanded polystyrene bead (~3mm diameter)

### Procedure

1. **Prepare particle:**
   ```
   Material: EPS foam, ping pong ball piece, or styrofoam
   Size: 2-5mm diameter (optimal ~3mm)
   Weight: <10mg
   ```

2. **Position array:**
   ```
   Mount horizontally (emitters facing up)
   Ensure level (use spirit level)
   Clear space above (30cm minimum)
   ```

3. **Power ON** and wait 5 seconds for stabilization

4. **Attempt levitation:**
   ```
   Method 1: Drop particle from 10cm above center
   Method 2: Place on fingertip at z=5mm, slowly withdraw
   Method 3: Use tweezers to position at trap center
   ```

5. **Observe behavior:**
   ```
   Success: Particle hovers at z=3-7mm, stable
   Partial: Particle jumps but doesn't hover (try smaller/lighter)
   Failure: No interaction (troubleshoot below)
   ```

6. **Test stability:**
   ```
   Gently blow on particle (should return to center)
   Move hand near array (should remain stable)
   Turn off power (particle should fall immediately)
   ```

### Pass Criteria
✅ Particle levitates for >5 seconds  
✅ Stable at z=3-7mm height  
✅ Returns to center after disturbance  
✅ Falls immediately when power removed

### Common Failures & Solutions

**Particle doesn't levitate:**
1. Check phase alignment (Test 6)
2. Increase power (raise duty cycle to 100%)
3. Try smaller/lighter particle
4. Verify all 7 emitters working (Test 7)

**Particle jumps around erratically:**
1. Reduce power slightly
2. Ensure array is level
3. Eliminate air currents (turn off fans)
4. Try heavier particle (4-5mm)

**Particle levitates but drifts:**
1. Check emitter spacing (should be precise)
2. Verify mounting plate not warped
3. One emitter may be weak (swap to test)

**Multiple particles interfere:**
1. Start with one particle only
2. Once stable, add second carefully
3. 7-emitter array supports 1-2 particles max

---

## 📊 Performance Metrics

**Record these values for your build:**

| Metric | Target | Your Result | Pass/Fail |
|--------|--------|-------------|-----------|
| Power supply voltage | 12.0V ±0.5V | _______ V | ☐ |
| Arduino VIN voltage | 12.0V ±0.5V | _______ V | ☐ |
| Operating frequency | 40.0 kHz ±0.5kHz | _______ kHz | ☐ |
| Phase alignment | ±10μs max | _______ μs | ☐ |
| Emitters functioning | 7/7 | _______ /7 | ☐ |
| Levitation height | 3-7mm | _______ mm | ☐ |
| Stable levitation time | >5 seconds | _______ sec | ☐ |
| MOSFET temperature | <50°C | _______ °C | ☐ |

**Share your results:** Post in GitHub Discussions!

---

## 🔧 Advanced Diagnostics

### Acoustic Pressure Measurement

**If you have access to ultrasonic microphone:**

1. Position mic at trap center (z=5mm)
2. Measure SPL with all emitters ON
3. Expected: 120-140 dB SPL @ 40kHz
4. If <110 dB: Increase power or fix phase
5. If >150 dB: Reduce power (hearing hazard)

### Force Measurement

**If you have precision scale:**

1. Place scale above array
2. Lower probe (1mm diameter) to trap center
3. Measure downward force with array ON
4. Expected: 0.5-2 mN (50-200 mg equivalent)
5. Compare to simulation predictions

### Thermal Imaging

**If you have thermal camera:**

1. Run array at full power for 10 minutes
2. Measure MOSFET temperatures
3. Expected: 40-60°C
4. If >70°C: Add heatsinks or active cooling

---

## 🎓 What Success Looks Like

**Video checklist:**
- [ ] Particle hovers steadily at 3-7mm
- [ ] Stays centered over array
- [ ] Resists gentle disturbances
- [ ] Falls instantly when power removed
- [ ] No erratic jumping or spinning
- [ ] All emitters flickering on camera
- [ ] No excessive heating

**Upload your success video to GitHub Discussions!**

---

## 🚨 Safety Verification

**Before considering build "complete," verify:**

- [ ] Power supply has fuse (2A)
- [ ] No exposed high-voltage connections
- [ ] MOSFETs have heatsinks (if >50°C)
- [ ] Safety shield in place
- [ ] Emergency shutoff accessible
- [ ] Hearing protection available
- [ ] Operating manual printed and available

---

## 📞 Getting Help

**If tests fail:**

1. **Check wiring diagram again** - 90% of failures are wiring errors
2. **Verify component values** - Wrong resistor/MOSFET causes issues
3. **Test components individually** - Isolate the problem
4. **Post in GitHub Discussions** with:
   - Which test failed
   - Exact symptoms
   - Photos of your setup
   - Measurements you took

**Community response time:** Usually <24 hours

---

## 🎯 Validation Certificate

**Once ALL tests pass, you've validated Build 1!**

```
┌──────────────────────────────────────────────────────────┐
│  OPEN ACOUSTIC LEVITATION - BUILD 1 VALIDATION           │
│                                                           │
│  Builder: _____________________________                   │
│  Date: ________________________________                   │
│  Location: ____________________________                   │
│                                                           │
│  All 8 tests passed: ☐ YES                               │
│  Levitation achieved: ☐ YES                              │
│                                                           │
│  Performance:                                             │
│  - Levitation height: _______ mm                         │
│  - Stable time: _______ seconds                          │
│  - Phase alignment: _______ μs                           │
│                                                           │
│  Witnessed by: ____________________                       │
│                                                           │
│  Share your success:                                      │
│  https://github.com/sportysport74/                       │
│  open-acoustic-levitation/discussions                    │
└──────────────────────────────────────────────────────────┘
```

**Print this certificate and sign it when you succeed!**

---

*Last updated: December 19, 2025*  
*Questions? Open a GitHub Issue tagged `testing-help`*
