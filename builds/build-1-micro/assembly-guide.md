# Build 1: Step-by-Step Assembly Guide

**Estimated time:** 8-12 hours over 2 weekends  
**Difficulty:** Beginner-friendly with patience

---

## Before You Start

### Pre-Assembly Checklist

**Parts arrived?**
- [ ] All electronics from BOM
- [ ] Base platform material
- [ ] Test objects (ping pong ball, etc.)

**Tools ready?**
- [ ] Soldering iron heated and tested
- [ ] Wire strippers working
- [ ] Hot glue gun heated
- [ ] Ruler/calipers available
- [ ] Scissors/knife sharp

**Workspace prepared?**
- [ ] Clean, flat surface
- [ ] Good lighting
- [ ] Ventilation (for soldering)
- [ ] Fire-safe area (hot glue, soldering)

**Mindset:**
- [ ] Not rushed (this takes time)
- [ ] Willing to make mistakes and learn
- [ ] Camera ready for documentation
- [ ] Music/podcast queued (it's a long build!)

---

## Phase 1: Mechanical Assembly (Day 1, 2-3 hours)

### Step 1: Prepare Base Platform

**Option A: Cardboard**

1. Find sturdy cardboard (3-5mm thick)
   - Cereal box, Amazon box, etc.
   - Should not flex easily

2. Draw 25cm diameter circle
   - Use compass or trace round object
   - Mark center point clearly

3. Cut carefully
   - Sharp scissors or box cutter
   - Smooth edges with sandpaper

4. Reinforce (optional)
   - Glue two layers together for stiffness
   - Let dry 30 minutes

**Option B: Plywood**

1. Obtain 6mm (1/4") plywood, 30cm × 30cm

2. Mark 25cm diameter circle
   - Use compass
   - Double-check center

3. Cut with jigsaw or have hardware store cut it

4. Sand edges smooth
   - 120 grit sandpaper
   - Remove splinters

5. Optional: Paint/seal
   - Spray paint or wood finish
   - Let dry completely

---

### Step 2: Calculate and Mark Emitter Positions

**Critical step - accuracy matters!**

**Geometry:**
- 7 emitters in Flower of Life pattern
- 1 center, 6 in ring around it
- Ring radius r₁ = 21.4mm (for 40kHz)

**Marking procedure:**

1. **Find and mark center point**
   - Measure 12.5cm from edge in two perpendicular directions
   - Mark with pen
   - This is emitter E0 position

2. **Mark ring of 6 emitters**
   
   Use protractor and ruler:
   - From center, measure 21.4mm at 0° (right) → Mark E1
   - Measure 21.4mm at 60° (upper right) → Mark E2
   - Measure 21.4mm at 120° (upper left) → Mark E3
   - Measure 21.4mm at 180° (left) → Mark E4
   - Measure 21.4mm at 240° (lower left) → Mark E5
   - Measure 21.4mm at 300° (lower right) → Mark E6

3. **Verify accuracy**
   - Distance from center to each: 21.4mm ± 0.5mm
   - Distance between adjacent ring emitters: ~21.4mm
   - Pattern should look like flower petals

**If you don't have protractor:**

Use this template:
```
     E3
      *
   E4 * * E2
      *
   E5 *E0* E1
      *
      * * 
     E6
```

Print grid paper, scale to 21.4mm spacing, trace positions.

---

### Step 3: Prepare Ultrasonic Buzzers

**Inspect buzzers:**

1. Identify pins
   - Usually 2 pins on bottom
   - Look for + and - markings (sometimes absent)
   - Consult datasheet or measure with multimeter

2. Test continuity
   - Buzzers are capacitive, should show high resistance
   - Both buzzers in same batch should measure similar

3. Identify top surface
   - Metal mesh or plastic cap
   - This is the emitting surface
   - Must face UPWARD when installed

---

### Step 4: Mount Buzzers to Base

**Using hot glue (easiest):**

1. Heat hot glue gun (5 minutes warm-up)

2. For each buzzer position:
   
   a. Apply small ring of hot glue around marked position
      - Not ON the mark (you need to see it)
      - Leave center open for pins
   
   b. Quickly place buzzer
      - Align center with mark
      - Press gently until glue cools (30 seconds)
      - Check alignment while glue is still soft
   
   c. Verify vertical
      - Buzzer should be perpendicular to base
      - Emitting surface facing UP
      - Not tilted (affects acoustic pattern)

3. Let all glue fully cure (15 minutes)

**Using foam tape (alternative):**

1. Cut small squares of double-sided foam tape

2. Stick to buzzer back

3. Remove backing, press firmly to base at mark

4. Hold 10 seconds for good adhesion

**For wooden base with drill:**

1. Drill 2 small holes (1mm diameter) at each position
   - Spacing matches buzzer pins
   - Careful not to split wood

2. Push buzzer pins through holes

3. Bend pins outward on bottom to secure

4. Optional: Add hot glue on top for extra strength

---

### Step 5: Create Reflector Plate

**Purpose:** Mounted to test object, reflects acoustic waves downward

**Materials:**
- Cardboard disk 8cm diameter
- Aluminum foil
- Glue stick

**Procedure:**

1. Cut cardboard circle 8cm diameter
   - Use compass or trace round object
   - Smooth edges

2. Apply thin layer of glue to one side

3. Place aluminum foil smoothly
   - Minimize wrinkles (affects reflections)
   - Press out air bubbles
   - Wrap edges around back

4. Let dry completely (20 minutes)

5. Trim excess foil around edges

**Result:** Shiny, flat, smooth reflector

**Later:** Attach to test object with more hot glue

---

### Step 6: Prepare Test Object

**Option A: Ping Pong Ball**

1. Take ping pong ball (2.7g)

2. Find "seam" (printed logo side)
   - This will be bottom (flattest area)

3. Attach reflector plate
   - Hot glue around edge of plate
   - Press onto ball at seam
   - Hold until cool
   - Reflector should be flat, not tilted

4. Measure total weight
   - Should be 5-10g total
   - If heavier, use less glue or smaller reflector

**Option B: Foam Sphere**

1. Take foam ball 40-50mm diameter

2. Hot glue reflector to flattest spot

3. Let cool completely

**Option C: Styrofoam Ball**

1. Similar to foam sphere

2. Be gentle - styrofoam melts with hot glue
   - Use LOW temp glue gun
   - Or use white craft glue (slower but safer)

**Storage:** Set aside until testing phase

---

**END OF DAY 1**

**What you've accomplished:**
✅ Base platform ready  
✅ All 7 buzzers mounted in correct pattern  
✅ Reflector plate created  
✅ Test object prepared  

**Take photos!** Document your work for troubleshooting later.

---

## Phase 2: Electronics Assembly (Day 2, 3-4 hours)

### Step 7: Prepare Wires for Buzzers

**You need:**
- 7× pairs of wires (one red, one black per buzzer)
- Each wire ~20cm long (8 inches)

**Procedure:**

1. Cut 14 wires total
   - 7 red (~20cm each)
   - 7 black (~20cm each)

2. Strip both ends
   - Remove 5mm insulation from each end
   - Twist stranded wire tightly

3. Pre-tin wire ends (optional but recommended)
   - Heat wire end with soldering iron
   - Touch solder to wire (not iron!)
   - Let solder wick into strands
   - Creates solid connection surface

4. Label wires
   - Use tape or marker
   - "E0-Red", "E0-Black", "E1-Red", etc.
   - Critical for later troubleshooting

---

### Step 8: Solder Wires to Buzzers

**Safety first:**
- Work in ventilated area
- Don't breathe solder fumes
- Iron is HOT (350°C/660°F)
- Use helping hands or tape to hold parts

**For each buzzer:**

1. Identify buzzer polarity
   - Look for + or - marking
   - If unmarked, consult datasheet
   - **Or:** Doesn't matter for AC (we're using 40kHz AC)

2. Position buzzer
   - Clamp in helping hands or tape down
   - Pins accessible

3. Solder red wire to one pin
   - Touch iron to pin (heat the pin, not the wire)
   - Wait 2-3 seconds for pin to heat
   - Touch solder to junction (wire + pin)
   - Solder should flow smoothly
   - Remove solder, then iron
   - Don't move for 5 seconds (let cool)

4. Solder black wire to other pin
   - Same process

5. Inspect joint
   - Should be shiny, smooth cone shape
   - Not dull, blobby, or cold (bad solder joint)
   - No shorts between pins

6. Strain relief (important!)
   - Hot glue wire to buzzer body
   - Prevents pulling force from breaking solder joint
   - Let glue cool before moving

7. Repeat for all 7 buzzers

**Common mistakes:**
- ❌ Not heating pin enough → cold solder joint
- ❌ Too much solder → shorts or ugly joint
- ❌ Moving while cooling → cracked joint
- ❌ No strain relief → joints break easily

**Testing:** Gently tug each wire. Should not pull off.

---

### Step 9: Set Up Breadboard

**Layout plan:**
```
[Power rails]  + + + + + + + + + + + + + +
               - - - - - - - - - - - - - -

[Row 1-5]      Arduino Nano
[Row 7-10]     Amp 1
[Row 12-15]    Amp 2  
[Row 17-20]    Amp 3
[Row 22-25]    Amp 4
```

**Procedure:**

1. Place Arduino Nano on breadboard
   - Straddles center channel
   - USB port facing you for easy access
   - Pins 1-15 on left, 16-30 on right

2. Place 4× PAM8403 amplifier modules
   - Space them out (see layout above)
   - Leave room for jumper wires

3. Verify nothing overlaps or shorts

---

### Step 10: Wire Power Distribution

**Power bus:**
- Top rail: +12V (red wire)
- Bottom rail: GND (black wire)

**Connections:**

1. **12V input:**
   - Solder wires to barrel jack (if not pre-wired)
   - Red → center pin (+12V)
   - Black → outer sleeve (GND)
   
2. **Connect barrel jack to breadboard:**
   - Red wire → top rail (+12V)
   - Black wire → bottom rail (GND)

3. **Power all amplifiers:**
   - For each amp:
     - Jumper from +12V rail to amp VCC pin
     - Jumper from GND rail to amp GND pin

4. **Power Arduino:**
   - Jumper from +12V rail to Arduino VIN pin
   - Jumper from GND rail to Arduino GND pin
   - **OR:** Power Arduino via USB (easier for first test)

**Visual check:**
- All amplifier modules have power connections
- No loose wires
- No shorts (check with multimeter if unsure)

---

### Step 11: Wire Amplifier Inputs

**Signal routing:**
- Arduino generates 7 PWM signals (40kHz square waves)
- Each signal goes to one amplifier channel input

**Arduino PWM pins:**
- D3, D5, D6, D9, D10, D11, D13 (7 pins capable of PWM)

**Amplifier assignment:**
```
Amp 1 Left  ← Arduino D3  → Emitter E0
Amp 1 Right ← Arduino D5  → Emitter E1
Amp 2 Left  ← Arduino D6  → Emitter E2
Amp 2 Right ← Arduino D9  → Emitter E3
Amp 3 Left  ← Arduino D10 → Emitter E4
Amp 3 Right ← Arduino D11 → Emitter E5
Amp 4 Left  ← Arduino D13 → Emitter E6
Amp 4 Right ← (unused)
```

**For each connection:**

1. Use jumper wire (M-M or M-F depending on amp module pins)

2. Connect Arduino pin → Amplifier input pin
   - Check amp pinout (usually marked L_IN, R_IN)

3. **Also connect grounds:**
   - Arduino GND → Each amp GND
   - Creates common ground reference
   - Critical for clean signal

**After all wired:**
- 7 signal wires (Arduino → Amps)
- Ground connections between Arduino and amps
- Total: ~15 jumper wires

---

### Step 12: Connect Buzzers to Amplifiers

**Output wiring:**

Each amplifier channel outputs to one buzzer.

**For each buzzer:**

1. Take red and black wires from buzzer

2. Connect to amplifier output:
   - Red → Amp "+" output
   - Black → Amp "-" output
   - (Polarity doesn't matter for AC, but stay consistent)

3. Verify connection:
   - Tight fit in breadboard holes
   - No loose wires
   - Correct amp channel (check your labels!)

**Double-check routing:**
```
E0 (center)     → Amp 1 Left
E1 (0°)         → Amp 1 Right
E2 (60°)        → Amp 2 Left
E3 (120°)       → Amp 2 Right
E4 (180°)       → Amp 3 Left
E5 (240°)       → Amp 3 Right
E6 (300°)       → Amp 4 Left
```

**This mapping is critical for correct phasing!**

---

### Step 13: Final Electrical Inspection

**Before powering on:**

1. **Visual inspection:**
   - [ ] All connections secure
   - [ ] No loose wires touching
   - [ ] Buzzer wires organized (not tangled)
   - [ ] Power connections correct polarity
   - [ ] Arduino USB cable accessible

2. **Continuity checks (if you have multimeter):**
   - [ ] +12V rail NOT shorted to GND
   - [ ] Each amp has power (measure between VCC and GND)
   - [ ] Each buzzer connected to an amp output

3. **Photo documentation:**
   - Take clear photo of entire setup
   - Useful for troubleshooting later
   - Show to community if you need help

---

**END OF DAY 2**

**What you've accomplished:**
✅ All wires soldered to buzzers  
✅ Breadboard laid out  
✅ Power distribution wired  
✅ Signal routing complete  
✅ Buzzers connected to outputs  

**Ready for software!**

---

## Phase 3: Software Upload (Day 3, 1-2 hours)

### Step 14: Install Arduino IDE

**If you already have Arduino IDE:** Skip to Step 15

**First time setup:**

1. Download Arduino IDE
   - Go to: https://www.arduino.cc/en/software
   - Choose your OS (Windows, Mac, Linux)
   - Download and install

2. Launch Arduino IDE

3. Select board type
   - Tools → Board → Arduino Nano
   - Tools → Processor → ATmega328P
   - (If using old Nano, might be "ATmega328P (Old Bootloader)")

4. Select COM port
   - Plug in Arduino via USB
   - Tools → Port → Select the new port that appeared
   - (Windows: COM3, COM4, etc.)
   - (Mac: /dev/cu.usbserial-xxxx)
   - (Linux: /dev/ttyUSB0)

5. Test with blink sketch
   - File → Examples → 01.Basics → Blink
   - Click Upload (right arrow button)
   - Arduino LED should blink (verify upload works)

---

### Step 15: Download Levitation Code

**Option A: From GitHub**

1. Go to: `https://github.com/[YOUR_REPO]/open-acoustic-levitation`

2. Navigate to: `software/arduino/build-1/`

3. Download `levitation_basic.ino`

**Option B: Copy from repository**

If you cloned the repo:
```
cd open-acoustic-levitation/software/arduino/build-1/
```

Files available:
- `levitation_basic.ino` - Start here (no sensors)
- `test_single_emitter.ino` - Test individual buzzers
- `test_all_emitters.ino` - Test all at once
- `levitation_parametric.ino` - Advanced with modulation

---

### Step 16: Upload Test Code

**Start simple - test one emitter first:**

1. Open `test_single_emitter.ino` in Arduino IDE

2. Review code (understanding is optional):
```cpp
// Generates 40kHz square wave on pin D3
void setup() {
  pinMode(3, OUTPUT);
}

void loop() {
  // 40kHz = 25 microseconds period
  // 50% duty cycle = 12.5μs HIGH, 12.5μs LOW
  digitalWrite(3, HIGH);
  delayMicroseconds(12);
  digitalWrite(3, LOW);
  delayMicroseconds(12);
}
```

3. Click Upload (→ button)

4. Wait for "Upload complete"

5. **Test:**
   - Hold phone near E0 (center emitter)
   - Use spectrum analyzer app (free: "Spectroid" for Android)
   - Should see peak at 40kHz
   - May hear very faint high-pitched tone (some people can hear 40kHz)

**Success?** → E0 is working!

**No signal?** → Check:
- [ ] Amp 1 powered (LED on amp module)
- [ ] Wiring from D3 → Amp 1 Left Input
- [ ] Wiring from Amp 1 Left Output → E0 buzzer
- [ ] Buzzer not damaged (check solder joints)

---

### Step 17: Test All Emitters Individually

**Modify test code to cycle through all 7:**
```cpp
int emitterPins[] = {3, 5, 6, 9, 10, 11, 13};

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 7; i++) {
    pinMode(emitterPins[i], OUTPUT);
  }
}

void loop() {
  for (int i = 0; i < 7; i++) {
    Serial.print("Testing emitter ");
    Serial.println(i);
    
    // Generate 40kHz for 2 seconds
    for (long j = 0; j < 80000; j++) {
      digitalWrite(emitterPins[i], HIGH);
      delayMicroseconds(12);
      digitalWrite(emitterPins[i], LOW);
      delayMicroseconds(12);
    }
    
    delay(500); // Pause between emitters
  }
}
```

**Upload and test:**
- Each emitter should produce 40kHz tone for 2 seconds
- Cycle repeats
- Use spectrum analyzer to verify

**Mark any non-working emitters for troubleshooting later**

---

### Step 18: Upload Main Levitation Code

**Now the real code:**

1. Open `levitation_basic.ino`

2. Review key parameters at top:
```cpp
#define CARRIER_FREQ 40000      // 40kHz
#define PARAM_FREQ 80000        // 80kHz (2× carrier)
#define EPSILON 0.10            // 10% modulation depth
```

3. Upload to Arduino

4. Open Serial Monitor (Tools → Serial Monitor)
   - Baud rate: 9600
   - Should see: "Levitation system starting..."

---

**END OF DAY 3**

**What you've accomplished:**
✅ Arduino IDE installed and working  
✅ Test code uploaded successfully  
✅ All 7 emitters verified functional  
✅ Main levitation code uploaded  

**Ready for first levitation attempt!**

---

## Phase 4: First Levitation (Day 4, 2-3 hours)

### Step 19: Safety Setup

**Before powering on full system:**

1. **Protect your hearing**
   - Even though 40kHz is ultrasonic, harmonics can be audible
   - Keep volume moderate during testing
   - If you hear loud squealing, reduce power immediately

2. **Protect your eyes**
   - Wear safety glasses
   - Parts can fail explosively if overpowered
   - Hot glue can pop off

3. **Safe environment**
   - Clear workspace
   - Non-flammable surface
   - Fire extinguisher nearby (just in case)
   - Keep hands/face away from active array

4. **Emergency stop**
   - Know where power plug is
   - Can quickly disconnect if needed

---

### Step 20: Initial Power-On Test

**Bring system to life gradually:**

1. **Connect power**
   - Plug 12V adapter into wall
   - Connect to barrel jack
   - Arduino should power on (LED lights)
   - Amplifier LEDs should light

2. **Visual check**
   - Any smoke? (STOP if yes)
   - Any burning smell? (STOP if yes)
   - Any hot components? (Touch carefully)
   - Everything look normal? → Good!

3. **Listen**
   - You might hear:
     - Very faint high-pitched whine (normal)
     - Amplifier hum (normal)
     - Loud screeching (NOT normal - reduce power)

4. **Measure acoustic field (optional)**
   - Use phone spectrum analyzer app
   - Hold near array center, ~5cm above
   - Should see strong peak at 40kHz
   - Maybe also peak at 80kHz (parametric modulation)

---

### Step 21: First Levitation Attempt

**The moment of truth!**

**Setup:**
1. Place array on stable table
   - Level surface
   - Good lighting
   - Camera ready!

2. Position yourself
   - Seated, comfortable
   - Can reach array easily
   - Can see Serial Monitor on computer

3. Prepare test object
   - Ping pong ball with reflector attached
   - Have spares ready

**Procedure:**

1. **Power on system**
   - Arduino boots
   - 40kHz generation starts
   - Check Serial Monitor for status

2. **Hold test object**
   - Hold ping pong ball by the sides (not top/bottom)
   - Position ~5mm above array center
   - Reflector plate facing down toward emitters

3. **Very slowly lower ball**
   - Move downward mm by mm
   - Feel for resistance (acoustic pressure pushing up)
   - At ~3-5mm height, you should feel strong upward force

4. **Release gently**
   - Let go slowly (don't drop it)
   - Ball should "stick" in the field
   - Might bounce a bit initially

5. **Observe**
   - Does it stay airborne?
   - How stable is it?
   - Can it recover from small pokes?

---

### Step 22: Troubleshooting First Attempt

**If ball falls immediately:**

**Problem:** Insufficient acoustic force

**Solutions to try:**
1. Lower the ball more (try 2-3mm height)
2. Reduce ball weight (smaller reflector)
3. Check all emitters producing sound (listen carefully)
4. Increase Arduino code frequency slightly (try 41kHz)

**If ball drifts sideways:**

**Problem:** Asymmetric field or phasing issues

**Solutions:**
1. Check emitter positions (should be symmetric)
2. Verify E0 is exactly at center
3. Check all amplifiers producing equal output
4. Verify pin mapping in code matches physical layout

**If ball oscillates wildly:**

**Problem:** Too much parametric gain or instability

**Solutions:**
1. Reduce EPSILON in code (try 0.05 instead of 0.10)
2. Check for mechanical resonances (table vibrating?)
3. Reduce power supply voltage (try 9V)

**If you hear loud screaming noise:**

**Problem:** Acoustic feedback or wrong frequency

**Solutions:**
1. Check frequency setting (should be 40000, not 4000)
2. Add acoustic dampening (foam around array)
3. Move away from walls (reflections cause feedback)

---

### Step 23: Parameter Tuning

**Once you get basic levitation, optimize it:**

**Frequency sweep:**

1. Try frequencies 38,000 to 42,000 Hz in 500 Hz steps
2. For each frequency:
   - Upload code
   - Attempt levitation
   - Note stability and height
3. Find frequency with best performance
4. This is your array's resonance frequency

**Modulation depth (EPSILON):**

1. Try values: 0.05, 0.08, 0.10, 0.12, 0.15
2. For each:
   - Upload code
   - Test levitation
   - Note if more or less stable
3. Higher epsilon = more power, but can cause instability
4. Sweet spot usually 0.08-0.12

**Phase tuning (advanced):**

If you're comfortable with code:
```cpp
// Try different phase offsets for ring emitters
// Current code has 0°, 60°, 120°, 180°, 240°, 300°
// Try tweaking by ±5-10°
```

---

### Step 24: Testing Different Objects

**Try various test objects:**

| Object | Expected | Notes |
|--------|----------|-------|
| Ping pong ball (2.7g) | ✓ Easy | Best starting point |
| Foam ball (5g) | ✓ Easy | Very stable |
| Small styrofoam ball (3g) | ✓ Easy | Might blow away |
| Paper disk (8cm, 1g) | ✓ Moderate | Can flutter |
| Small electronics part (10g) | ⚠️ Hard | Needs more power |
| Water droplet | ❌ Very hard | Advanced, don't try yet |

**For each object:**
1. Attach reflector plate
2. Measure total weight
3. Attempt levitation
4. Adjust height and parameters
5. Document results (photo/video)

---

### Step 25: Measure Performance

**Quantify your success:**

**Levitation height:**
- Use ruler or calipers
- Measure from array surface to object bottom
- Typical: 3-8mm

**Stability:**
- Use camera with grid overlay
- Record 30 seconds
- Measure horizontal drift
- Goal: <1mm drift

**Power consumption:**
- Measure with Kill-A-Watt meter or multimeter
- At wall plug (includes inefficiencies)
- Typical: 5-10W total

**Disturbance rejection:**
- Gently poke object sideways (~5mm displacement)
- Time how long to return to center
- Goal: <5 seconds

**Maximum mass:**
- Gradually increase object weight
- Find mass where levitation fails
- Typical for Build 1: 15-30g maximum

---

### Step 26: Documentation & Sharing

**Capture your success!**

**Photos:**
- Overall setup (wide shot)
- Close-up of array
- Levitating object
- From multiple angles

**Video:**
- Object levitating (30+ seconds continuous)
- Disturbance rejection test
- Time-lapse of assembly (if you filmed it)

**Data:**
- Fill out performance table
- Save measured parameters
- Note what worked and what didn't

**Share with community:**
1. Create post in `/community/replications/`
2. Include:
   - Photos/videos
   - BOM modifications (if any)
   - Measured performance
   - Tips for others
3. Link to any forum posts or social media

**Help others:**
- Answer questions in GitHub issues
- Share your troubleshooting discoveries
- Suggest documentation improvements

---

## What's Next?

### Option A: Improve Build 1

**Easy upgrades:**
- Add distance sensors (VL53L0X) for height measurement
- Add acoustic feedback (40kHz receivers)
- Implement PID control for better stability
- Add LCD display showing parameters

**Medium upgrades:**
- Upgrade to better transducers (Langevin type)
- Build proper PCB (no more breadboard)
- Add Bluetooth control (phone app)
- Levitate multiple objects simultaneously

**Advanced:**
- Add lateral positioning control
- Implement object tracking with camera
- Create "choreographed" levitation patterns
- Acoustic tweezers (manipulate tiny particles)

---

### Option B: Scale Up to Build 2

**Build 2 specs:**
- 1 kg payload capacity
- FPGA control
- Professional transducers
- Sensor feedback
- Budget: ~$5,000

**Read:** `builds/build-2-lab/README.md`

---

### Option C: Experiment & Research

**Scientific exploration:**
- Map acoustic field with microphone array
- Measure frequency response
- Test parametric gain experimentally
- Validate theoretical predictions

**Creative applications:**
- Levitate delicate objects (orchid, soap bubble)
- Create art installations
- Demo at science fairs
- Teach physics concepts

---

## Appendix A: Common Issues Reference

### Issue: No levitation at all

**Symptoms:** Ball just falls

**Check:**
1. All emitters working (test individually)
2. Correct frequency (40,000 not 4,000)
3. Sufficient power (12V supply, not 5V)
4. Object has reflector plate
5. Array geometry correct (measure positions)

### Issue: Lateral drift

**Symptoms:** Object slides off to one side

**Check:**
1. Center emitter (E0) exactly at center
2. Ring emitters symmetric
3. All amplifiers equal gain
4. Level mounting surface
5. No air currents (fans, AC vents)

### Issue: Loud noise

**Symptoms:** High-pitched screaming

**Check:**
1. Frequency not too low (<30kHz becomes audible)
2. No acoustic feedback (array too close to walls)
3. Amplifier gain not maxed out
4. No mechanical resonances (table, enclosure)

### Issue: Unstable oscillation

**Symptoms:** Object bounces wildly

**Check:**
1. Parametric modulation depth too high (reduce EPSILON)
2. Object too light (acoustic streaming blows it around)
3. Mechanical vibrations (isolate array from table)
4. Phase relationships incorrect (verify code)

### Issue: Component heating

**Symptoms:** Amplifiers, buzzers, or Arduino getting hot

**Check:**
1. Not short-circuited (check with multimeter)
2. Amplifier output not exceeding buzzer rating
3. Adequate ventilation
4. Reduce duty cycle in code (80% instead of 50%)

---

## Appendix B: Theory Refresher

**Why does this work?**

1. **Acoustic radiation pressure:** Sound waves exert force on objects
2. **Standing waves:** Create regions of high/low pressure
3. **Flower of Life geometry:** Optimal emitter spacing for constructive interference
4. **Parametric pumping:** Modulating at 2× frequency amplifies standing wave
5. **Result:** Stable levitation with minimal power

**Read more:** `/theory/` directory

---

## Appendix C: Code Explanation

**Key sections of `levitation_basic.ino`:**
```cpp
// Pin definitions (PWM-capable pins on Arduino Nano)
const int emitterPins[7] = {3, 5, 6, 9, 10, 11, 13};

// Frequencies
const long CARRIER_FREQ = 40000;     // 40 kHz carrier
const long PARAM_FREQ = 80000;       // 80 kHz parametric
const float EPSILON = 0.10;          // 10% modulation depth

// Phase offsets for Flower of Life geometry
const float phaseOffsets[7] = {
  0,                  // E0: center
  0,                  // E1: 0°
  PI/3,               // E2: 60°
  2*PI/3,             // E3: 120°
  PI,                 // E4: 180°
  4*PI/3,             // E5: 240°
  5*PI/3              // E6: 300°
};

void setup() {
  // Initialize all pins as outputs
  for (int i = 0; i < 7; i++) {
    pinMode(emitterPins[i], OUTPUT);
  }
  
  Serial.begin(9600);
  Serial.println("Levitation system starting...");
}

void loop() {
  // Calculate current time in microseconds
  unsigned long t = micros();
  
  // Parametric modulation envelope
  float envelope = 1.0 + EPSILON * sin(2 * PI * PARAM_FREQ * t / 1e6);
  
  // For each emitter
  for (int i = 0; i < 7; i++) {
    // Calculate phase-shifted carrier with parametric envelope
    float phase = 2 * PI * CARRIER_FREQ * t / 1e6 + phaseOffsets[i];
    float signal = envelope * sin(phase);
    
    // Convert to digital (square wave approximation)
    digitalWrite(emitterPins[i], signal > 0 ? HIGH : LOW);
  }
}
```

**What each part does:**
- `emitterPins[]`: Maps physical buzzers to Arduino pins
- `CARRIER_FREQ`: Main 40kHz oscillation
- `PARAM_FREQ`: 80kHz modulation (2× carrier)
- `EPSILON`: Modulation depth (how much parametric pumping)
- `phaseOffsets[]`: Phase shift for each emitter (creates toroidal trap)
- `envelope`: Multiplies carrier amplitude at parametric frequency
- `signal`: Final output (carrier × envelope × phase offset)

---

## Appendix D: Improvements for Version 2

**After successful Build 1, consider:**

**Hardware upgrades:**
- [ ] Replace PAM8403 amps with TPA3116 (more power)
- [ ] Add VL53L0X sensors for height measurement
- [ ] Use Teensy 4.1 instead of Arduino (faster, more PWM pins)
- [ ] 3D print proper enclosure
- [ ] Add LED status indicators

**Software improvements:**
- [ ] Implement PID control loop
- [ ] Add sensor fusion (multiple measurements)
- [ ] Frequency auto-tuning (sweep and lock to resonance)
- [ ] Serial commands for real-time parameter adjustment
- [ ] Data logging to SD card

**Mechanical refinements:**
- [ ] CNC-machined aluminum base (better than cardboard)
- [ ] Adjustable emitter mounts (for fine-tuning positions)
- [ ] Acoustic dampening enclosure (reduce noise)
- [ ] Multiple test objects on rotating platform

---

## Need Help?

**Stuck? Don't give up!**

- **GitHub Issues:** Post your problem with photos
- **Discord:** Real-time help from community
- **Email:** [contact info]
- **Troubleshooting guide:** `troubleshooting.md` in this directory

**Remember:** Everyone struggles on their first build. The community is here to help!

---

## Congratulations!

**You've built a working acoustic levitation system!**

You now understand:
- ✅ Acoustic standing waves
- ✅ Parametric amplification
- ✅ Sacred geometry optimization
- ✅ Microcontroller programming
- ✅ Electronic circuit assembly

**This is just the beginning.**

You've proven the physics works. Now imagine what's possible:
- Levitating larger objects (Build 2, Build 3)
- New applications (medicine, manufacturing, art)
- Further optimizations (lower power, higher stability)
- Sharing knowledge (help others build)

**Welcome to the levitation community!**

---

*"Any sufficiently advanced technology is indistinguishable from magic."*  
*- Arthur C. Clarke*

*"You just built magic. Now make it real for others."*  
*- Us*