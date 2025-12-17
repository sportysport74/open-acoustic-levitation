# Build 1: Troubleshooting Guide

**Having issues? You're not alone. Here's how to fix common problems.**

---

## General Debugging Process

**Before diving into specific issues:**

1. **Stay calm** - Every build has problems, they're solvable
2. **Isolate the problem** - Test one thing at a time
3. **Document** - Take photos, notes, measurements
4. **Ask for help** - Community is here for you

**Basic diagnostic procedure:**
```
1. Power check → Is everything getting power?
2. Continuity check → Are connections solid?
3. Component check → Do individual parts work?
4. System check → Does it work together?
```

---

## Issue #1: No Sound from Buzzers

### Symptoms
- Upload successful, no errors
- Arduino powered, LED on
- But no sound at all (dead silent)
- Phone spectrum analyzer shows nothing

### Possible Causes & Solutions

**Cause A: Frequency too high for human hearing**

Actually not a problem! 40kHz is ultrasonic (inaudible).

**Test:** Use phone app (Spectroid, etc.) to detect 40kHz signal  
**Solution:** If app shows 40kHz peak, system is working (even if you can't hear it)

---

**Cause B: Wiring problem**

**Check:**
- [ ] Arduino pin → Amplifier input connection
- [ ] Amplifier output → Buzzer connection
- [ ] All grounds connected (common ground is critical)

**Test:** Use multimeter
1. Set to continuity mode (beeps when connected)
2. Touch one probe to Arduino pin
3. Touch other to amp input pin
4. Should beep (if not, connection is broken)

**Solution:** Fix the broken connection

---

**Cause C: Amplifier not powered**

**Check:**
- [ ] 12V power supply plugged in and working
- [ ] Power cable to breadboard secure
- [ ] Amplifier module LED lit (if it has one)
- [ ] Voltage at amp VCC pin (should be ~12V)

**Test with multimeter:**
1. Set to DC voltage (20V range)
2. Black probe to GND rail
3. Red probe to +12V rail
4. Should read 11-12.5V

**Solution:** 
- Tighten connections
- Replace power supply if voltage is wrong
- Check for short circuits (using continuity mode)

---

**Cause D: Wrong frequency in code**

**Check:** Open Arduino code, look for:
```cpp
const unsigned long CARRIER_FREQ = 40000;
```

**Common mistake:** Typing `4000` instead of `40000` (off by 10×)

**Solution:** Fix typo, re-upload code

---

**Cause E: Buzzer polarity wrong (unlikely)**

Most piezo buzzers work either way with AC signal, but some are polarized.

**Test:** Swap red and black wires on one buzzer, re-test

**Solution:** If it works, swap all buzzers to match

---

## Issue #2: Object Falls Immediately

### Symptoms
- Sound clearly audible (40kHz generation working)
- Test object placed at levitation height
- But falls straight down, no "stickiness"

### Possible Causes & Solutions

**Cause A: Height too high**

Levitation only works in narrow range (~2-8mm for Build 1)

**Test:** 
1. Hold object at 10mm → slowly lower
2. At some point should feel upward pressure
3. This is the sweet spot

**Solution:** Lower object to 3-5mm height, try again

---

**Cause B: Object too heavy**

Build 1 maximum: ~30-50g depending on setup

**Test:** Weigh object (including reflector plate)

**Solution:**
- Use lighter object (ping pong ball = 2.7g is ideal)
- Make reflector smaller
- Remove excess hot glue

---

**Cause C: Missing or poor reflector plate**

Reflector is critical - directs acoustic waves.

**Check:**
- [ ] Reflector attached to object bottom
- [ ] Reflector facing DOWN (shiny side toward array)
- [ ] Reflector flat and smooth (no wrinkles)
- [ ] Reflector diameter appropriate (6-10cm for ping pong ball)

**Solution:** 
- Add reflector if missing
- Smooth out wrinkles in foil
- Ensure tight attachment (no gaps)

---

**Cause D: Insufficient acoustic power**

Not enough force to overcome gravity.

**Check:**
- [ ] All 7 emitters producing sound (test individually)
- [ ] Power supply voltage adequate (12V, not 5V or 9V)
- [ ] No damaged buzzers (check solder joints)

**Test:** Hold phone near each emitter, verify 40kHz signal

**Solution:**
- Fix non-working emitters
- Increase power supply voltage (try 15V if amps support it)
- In code, increase EPSILON (more parametric gain)

---

**Cause E: Geometry wrong**

If emitters not in correct Flower of Life pattern, constructive interference fails.

**Measure:**
- Distance from center to each ring emitter (should be 21.4mm ±1mm)
- Distance between adjacent ring emitters (should be ~21.4mm)
- All should be roughly equal

**Solution:** 
- Remount emitters if positions are way off (>2mm error)
- Or adjust in code (change PHASE_OFFSETS array to compensate)

---

## Issue #3: Object Drifts Sideways

### Symptoms
- Object levitates initially
- But slowly or quickly slides off to one side
- Falls off edge of array

### Possible Causes & Solutions

**Cause A: Center emitter not at center**

E0 (center emitter) creates vertical stability. If off-center, lateral forces unbalanced.

**Measure:** 
- Distance from E0 to each edge of platform
- Should be equal in all directions

**Solution:** 
- If E0 is >2mm off-center, remount it correctly
- Or physically center the platform under the object

---

**Cause B: Asymmetric emitter positions**

Ring emitters should form perfect hexagon.

**Check:** Measure position of each E1-E6
- All should be same distance from center (21.4mm)
- Adjacent emitters should be ~21.4mm apart

**Solution:**
- If one emitter is mispositioned, remount it
- Or adjust its phase in code to compensate

---

**Cause C: One or more emitters not working**

Creates asymmetric acoustic field.

**Test:** Run `test_single_emitter.ino`
- Verify each emitter produces sound
- Mark any dead emitters

**Solution:**
- Check wiring to dead emitter(s)
- Re-solder if joint is broken
- Replace buzzer if damaged

---

**Cause D: Amplifier gain mismatch**

If one amp is louder than others, imbalanced field.

**Check:**
- All amps same model
- No gain adjustment pots on amps (or all set same)

**Solution:**
- Use identical amplifier modules
- If amps have trim pots, adjust for equal output

---

**Cause E: Air currents**

Gentle breeze from AC vent, fan, or breathing can push object.

**Test:** 
- Place tissue paper near array
- Check for movement (indicates air current)

**Solution:**
- Move array away from vents
- Turn off fans
- Build windscreen (acrylic box around array, open bottom)

---

**Cause F: Tilted mounting surface**

If table/platform isn't level, gravity creates lateral component.

**Check:** Use spirit level or phone level app

**Solution:** Level the surface, or shim under array

---

## Issue #4: Loud Squealing/Screeching

### Symptoms
- Extremely loud, unpleasant high-pitched noise
- May be intermittent or constant
- Possibly painful to ears

### Possible Causes & Solutions

**Cause A: Frequency too low**

Below 20kHz enters audible range.

**Check code:**
```cpp
const unsigned long CARRIER_FREQ = 40000;
```

Should be 40000, not 4000 or 400.

**Solution:** Fix typo, re-upload

---

**Cause B: Acoustic feedback**

Array too close to reflective surfaces (walls, table).

**Test:** 
- Move array to open area
- Cover nearby walls with foam/blankets

**Solution:**
- Move array >1 meter from walls
- Add acoustic dampening (foam panels)
- Point array away from hard surfaces

---

**Cause C: Mechanical resonance**

Table or structure vibrating at audible frequency.

**Test:**
- Touch table - does buzzing stop?
- Move array to different surface

**Solution:**
- Isolate array (place on foam pad)
- Use heavier, more rigid platform
- Damp vibrations (rubber feet, foam)

---

**Cause D: Amplifier clipping**

Over-driven amplifiers produce harsh harmonics.

**Check:**
- Power supply voltage (should be 12V, not 15-18V)
- Amplifier specs (PAM8403 is 2×3W max)

**Solution:**
- Reduce voltage
- Add current limiting resistor (1Ω in series with buzzer)
- In code, reduce duty cycle:
```cpp
// Instead of full square wave:
if (signal > 0) {
  digitalWrite(pin, HIGH);
  delayMicroseconds(10);  // Reduced from 12
  digitalWrite(pin, LOW);
  delayMicroseconds(14);  // Extended from 12
}
```

---

## Issue #5: Unstable Oscillation

### Symptoms
- Object levitates but bounces/vibrates wildly
- Amplitude of oscillation grows
- Eventually object is ejected

### Possible Causes & Solutions

**Cause A: Parametric instability**

Too much parametric gain → exponential growth.

**Solution:** Reduce EPSILON in code
```cpp
const float EPSILON = 0.05;  // Was 0.10, now reduced
```

Start at 0.05, gradually increase until stable.

---

**Cause B: Mechanical resonance**

Object vibrating at natural frequency.

**Check:** 
- Object rigidity (should not be floppy)
- Mounting of reflector (should be solid)

**Solution:**
- Use stiffer object
- Better gluing of reflector
- Add small weight to change resonance frequency

---

**Cause C: Control loop instability**

If using advanced code with feedback, PID gains might be too high.

**Solution:** 
- Reduce proportional gain (Kp)
- Increase derivative gain (Kd) for damping
- Start with: Kp=20, Ki=1, Kd=5

---

**Cause D: Table vibration**

Array shaking → object bouncing.

**Test:** Touch table during operation (does stability improve?)

**Solution:**
- Mount on heavier, more rigid surface
- Isolate from floor vibrations (foam feet)
- Move away from sources of vibration (loud music, etc.)

---

## Issue #6: Components Overheating

### Symptoms
- Amplifiers or buzzers hot to touch (>50°C)
- Smell of burning electronics
- Unexpected shutdown

### Possible Causes & Solutions

**Cause A: Short circuit**

Buzzer wires touching, or power rails shorted.

**Check with multimeter:**
- Resistance between +12V and GND rails (should be >1kΩ)
- Resistance across buzzer terminals (should be 10-100Ω)

**Solution:**
- Find and fix short
- Check for stray wire strands
- Inspect solder joints

---

**Cause B: Over-voltage**

Power supply too high.

**Measure:** Voltage at amp VCC pin (should be 11-13V)

**Solution:**
- Use correct 12V supply
- Add voltage regulator if needed
- Replace supply if outputting wrong voltage

---

**Cause C: Amplifier driving too much current**

Buzzer impedance too low.

**Check:** Buzzer spec sheet (should be 8Ω or higher)

**Solution:**
- Add 1Ω series resistor to each buzzer
- Or use higher impedance buzzers

---

**Cause D: Inadequate cooling**

Components packed too tight, no airflow.

**Solution:**
- Space out components on breadboard
- Add small fan (40mm computer fan)
- Remove from enclosed space
- Add heatsinks to amp chips (if accessible)

---

**Cause E: Continuous high power**

Running at full power 24/7 overheats components.

**Solution:**
- Reduce duty cycle (see earlier code example)
- Implement idle mode (lower power when not levitating)
- Add thermal shutdown (monitor temps, reduce power if hot)

---

## Issue #7: Arduino Upload Failures

### Symptoms
- "avrdude: stk500_recv(): programmer is not responding"
- "Error uploading to board"
- Compiler errors

### Solutions by Error Type

**"Programmer not responding":**

- [ ] Correct COM port selected? (Tools → Port)
- [ ] USB cable good? (try different cable/port)
- [ ] Driver installed? (CH340 driver for clones)
- [ ] Press reset button on Arduino, then upload immediately

**"Permission denied" (Linux/Mac):**
```bash
sudo usermod -a -G dialout $USER
# Log out and back in
```

**Compiler errors:**

- [ ] Board set to "Arduino Nano" (Tools → Board)
- [ ] Processor set to "ATmega328P" (Tools → Processor)
- [ ] Try "ATmega328P (Old Bootloader)" if standard doesn't work

**Still failing:**

1. Try different computer
2. Test Arduino with simple Blink sketch
3. Arduino may be damaged (rare)

---

## Issue #8: Inconsistent Performance

### Symptoms
- Works sometimes, not others
- Performance varies day-to-day
- Random failures

### Possible Causes & Solutions

**Cause A: Loose connections**

Breadboard connections work loose over time.

**Solution:**
- Press all components firmly into breadboard
- Re-seat jumper wires
- For permanent fix, solder to perfboard

---

**Cause B: Environmental changes**

Temperature, humidity, air pressure affect acoustics.

**Monitor:**
- Temperature (optimal: 20-25°C)
- Humidity (optimal: 30-60%)
- Barometric pressure (affects air density)

**Solution:**
- Maintain consistent environment
- Re-calibrate frequency for conditions
- Account for seasonal variation

---

**Cause C: Power supply instability**

Voltage droop, ripple, or noise.

**Test:** 
- Measure voltage with oscilloscope (check for AC ripple)
- Use multimeter (check for voltage drop under load)

**Solution:**
- Use higher-quality PSU
- Add large capacitor (1000μF) across power rails
- Use separate PSU for Arduino (USB power)

---

**Cause D: Buzzer degradation**

Piezo elements can weaken over time, especially if over-driven.

**Test:** 
- Measure impedance (should be stable)
- Listen to each buzzer (should sound similar)

**Solution:**
- Replace weak buzzers
- Reduce drive power to extend life

---

## Issue #9: Can't Replicate Published Results

### Symptoms
- Following guide exactly
- But performance significantly worse than expected
- Object won't levitate at all, or very unstable

### Possible Explanations

**Different components:**
- Your buzzers may differ from reference design
- PAM8403 has many clones with varying quality
- Arduino clone behaves slightly differently

**Solution:** 
- Try adjusting frequency (sweep 38-42kHz)
- Adjust epsilon (try 0.05 to 0.20)
- Post detailed specs on forum for help

---

**Measurement error:**
- Emitter positions measured incorrectly
- Height not accurate
- Test object weight unknown

**Solution:**
- Re-measure everything carefully
- Use calipers (±0.1mm accuracy)
- Weigh test object on precise scale

---

**Environmental factors:**
- Your room acoustics very different
- Air pressure/temp far from standard
- EMI from other devices

**Solution:**
- Test in different location
- Shield from RF interference (aluminum foil tent)
- Check for ultrasonic noise sources (some electronics emit 40kHz)

---

## General Tips for Troubleshooting

### Use Divide-and-Conquer

1. **Test subsystems separately**
   - Power supply → Arduino → Amplifiers → Buzzers
   - Find which stage is broken

2. **Swap components**
   - Replace suspected bad part with known good
   - Isolates hardware vs. software problems

3. **Simplify**
   - Start with single emitter, verify it works
   - Add emitters one at a time
   - Find where problem appears

### Document Everything

Take photos and notes:
- Component positions
- Wiring connections
- Parameter values that worked
- Error messages
- Measurement data

**This helps YOU debug and helps OTHERS help you.**

### Ask for Help

**When posting to forum/Discord:**

1. **Clear description** of problem
2. **Photos** of setup (multiple angles)
3. **Code** you're running (paste to pastebin)
4. **What you've tried** already
5. **Measurements** (voltages, frequencies, etc.)

**Example good post:**

> "Build 1 not levitating. Object falls immediately.
> 
> Setup:
> - 7× Murata MA40S4S buzzers
> - 4× PAM8403 amps
> - Arduino Nano clone (CH340)
> - 12V 2A PSU
> 
> Tested:
> - All emitters produce 40kHz (verified with Spectroid app)
> - Voltage at amps: 11.8V
> - Used ping pong ball with 8cm foil reflector (total 8g)
> - Tried heights 2mm to 10mm
> 
> Photos: [imgur album link]
> Code: [pastebin link]
> 
> Any ideas?"

**That gets quick, helpful responses!**

---

## Still Stuck?

**Resources:**

1. **GitHub Issues:** https://github.com/[repo]/issues
   - Search existing issues first
   - Open new issue with details

2. **Discord Server:** [invite link]
   - Real-time help
   - Share photos/videos
   - Community members usually respond within hours

3. **Email:** [contact email]
   - For private inquiries
   - Usually respond within 24-48 hours

4. **FAQ:** See `docs/faq.md`
   - Common questions answered

**Remember:** Every successful build started with problems. Debugging is part of the learning process. Don't give up!

---

*"The difference between success and failure is one more attempt."*  
*- Unknown*

*"Troubleshooting is where the real learning happens."*  
*- Every engineer, ever*