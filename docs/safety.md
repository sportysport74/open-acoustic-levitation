# Safety Guide - Acoustic Levitation

⚠️ **READ THIS BEFORE BUILDING OR OPERATING ANY ACOUSTIC LEVITATION DEVICE**

## Overview

Acoustic levitation uses high-intensity ultrasonic sound waves (typically 40 kHz) to create standing wave patterns that can trap and manipulate small objects. While fascinating, this technology involves real hazards that must be understood and managed.

---

## 🚨 Critical Safety Warnings

### 1. Hearing Damage Risk

**THE DANGER:**
- 40 kHz is technically "ultrasonic" (above 20 kHz human hearing range)
- **However:** Transducers produce harmonics and subharmonics in audible range
- High sound pressure levels (>110 dB SPL) can cause permanent hearing damage
- Young people (under 25) can often hear up to 22-24 kHz - partial ultrasonic perception is possible

**PROTECTION REQUIRED:**
- ✅ Wear hearing protection (earplugs or earmuffs) when operating above 50% power
- ✅ Limit exposure time: <15 minutes per hour at high power
- ✅ Never operate at full power in enclosed spaces
- ✅ Keep devices at least 50cm away from your head
- ❌ **NEVER point active emitters at your ears**

**WARNING SIGNS OF OVEREXPOSURE:**
- Ringing in ears (tinnitus)
- Temporary hearing loss or muffling
- Headache or pressure sensation
- Dizziness or nausea

*If you experience any of these, STOP IMMEDIATELY and rest for 24 hours.*

---

### 2. Transducer Overheating

**THE DANGER:**
- Ultrasonic transducers generate significant heat during operation
- Overheating causes:
  - Permanent depoling (loss of piezoelectric properties)
  - Cracked ceramics
  - Solder joint failure
  - Fire hazard (rare but possible)

**SAFE OPERATING LIMITS:**

| Build Level | Max Power/Emitter | Max Duty Cycle | Cooling Required |
|-------------|-------------------|----------------|------------------|
| Build 1 (7)  | 2W continuous     | 100% (with heatsinks) | Passive aluminum fins |
| Build 2 (19) | 5W continuous     | 80% (4 sec on, 1 sec off) | Active cooling fan |
| Build 3 (37) | 10W continuous    | 60% (pulse mode) | Water cooling or forced air |

**TEMPERATURE MONITORING:**
- Install thermistors on at least 3 emitters (center + 2 outer)
- Set firmware cutoff at 65°C (149°F)
- Add visual/audible temperature warnings at 55°C

**HEATSINK REQUIREMENTS:**
- Build 1: 20mm × 20mm aluminum heatsink per emitter (optional but recommended)
- Build 2: 30mm × 30mm heatsink + 40mm cooling fan (required)
- Build 3: Custom water cooling loop or industrial blower (required)

---

### 3. Electrical Safety

**HIGH VOLTAGE HAZARDS:**
- Transducers require 20-40V peak-to-peak drive signals
- Amplifier circuits can produce 100V+ spikes during switching
- Risk of electric shock if touched while powered

**SAFE PRACTICES:**
- ✅ Use isolated power supplies (no direct AC mains connection)
- ✅ Add proper grounding to all metal enclosures
- ✅ Include fuses: 2A for Build 1, 5A for Build 2, 10A for Build 3
- ✅ Use insulated wire (rated for 300V minimum)
- ✅ Add emergency shutoff switch within arm's reach
- ❌ **NEVER touch circuits while powered**
- ❌ **NEVER operate with exposed high-voltage traces**

**CAPACITOR DISCHARGE:**
- Power supply capacitors can hold dangerous charge after power-off
- Wait 60 seconds after unplugging before touching circuits
- Use a 10kΩ bleed resistor across main power capacitor

---

### 4. Particle Selection Safety

**SAFE PARTICLES:**
- ✅ Expanded polystyrene foam beads (EPS)
- ✅ Ping pong balls (celluloid or ABS)
- ✅ Paper confetti
- ✅ Small water droplets (<2mm)
- ✅ Styrofoam peanuts

**UNSAFE PARTICLES - DO NOT USE:**
- ❌ **Metal objects** (create eddy currents, can become projectiles)
- ❌ **Sharp objects** (safety hazard if ejected)
- ❌ **Toxic materials** (beryllium, lead, asbestos)
- ❌ **Flammable liquids** (alcohol, acetone, gasoline)
- ❌ **Living insects** (ethical concerns + unpredictable behavior)
- ❌ **Any particle >20mm diameter** (exceeds acoustic wavelength limit)

**PARTICLE SIZE LIMITS:**

For 40 kHz (λ = 8.575 mm):
- **Optimal:** 0.1λ to 0.5λ (0.86mm to 4.3mm diameter)
- **Maximum:** 0.8λ (6.9mm diameter)
- **Above 0.8λ:** Trapping becomes unstable, particles may be ejected violently

**EJECTION HAZARDS:**
- Particles can be ejected at >5 m/s if power is too high or suddenly cut
- Wear safety glasses when levitating particles >3mm
- Use transparent shields around levitation zone for Build 2/3

---

### 5. Phase Alignment Warnings

**DESTRUCTIVE INTERFERENCE RISK:**

When multiple emitters operate, phase relationships are CRITICAL:

**DANGER SCENARIO:**
- Incorrect phasing causes destructive interference
- Instead of levitating, particles are ACCELERATED
- Can create high-velocity projectiles (>10 m/s)

**SAFE PHASE PRACTICES:**
- ✅ Always test with single emitter first
- ✅ Add emitters one at a time while monitoring pressure field
- ✅ Use oscilloscope to verify all emitters are in-phase (±10° tolerance)
- ✅ Include firmware phase verification routine
- ❌ **NEVER operate with unknown phase relationships**

**PHASE TESTING PROCEDURE:**
1. Start with center emitter only (if multi-ring array)
2. Add one outer emitter and verify constructive interference
3. Measure sound pressure at trap center - should INCREASE by >50%
4. If pressure decreases, phase is inverted - fix immediately
5. Repeat for each emitter

**MICROPHONE SETUP FOR PHASE TESTING:**
- Use ultrasonic microphone (40 kHz response)
- Place at expected trap center (z = 5-10mm above array)
- Measure SPL - should be >120 dB with all emitters active
- If <100 dB, phase alignment is wrong

---

### 6. Biological Exposure Limits

**ULTRASONIC BIOEFFECTS:**

Research shows potential biological effects above certain exposure levels:

**SAFE EXPOSURE LIMITS (40 kHz):**
- **Spatial Peak Temporal Average Intensity (ISPTA):** <100 mW/cm²
- **Mechanical Index (MI):** <1.9
- **Thermal Index (TI):** <2.0

**DO NOT:**
- ❌ Place hands/arms in high-intensity acoustic field (>130 dB SPL)
- ❌ Expose skin to direct ultrasonic beam for >60 seconds
- ❌ Operate near pregnant women (unknown fetal effects)
- ❌ Use around young children (<12 years old)

**OBSERVED BIOEFFECTS AT HIGH INTENSITIES:**
- Skin warming (>140 dB SPL)
- Cavitation in fluids (>150 dB SPL, can damage tissues)
- Microstreaming effects in cells (research ongoing)

**If performing biological experiments:**
- Consult institutional biosafety committee
- Follow FDA/NIH guidelines for ultrasonic exposure
- Document all exposure parameters (frequency, intensity, duration)

---

## 🔬 Lab Safety Requirements

### Minimum Safety Equipment

**Required for all builds:**
- [ ] Safety glasses (ANSI Z87.1 rated)
- [ ] Hearing protection (NRR 25+ dB)
- [ ] Fire extinguisher (Class C electrical)
- [ ] First aid kit
- [ ] Emergency shutoff switch (large, red, easily accessible)

**Required for Build 2+:**
- [ ] Fume extractor (if soldering)
- [ ] Multimeter with voltage/current monitoring
- [ ] Thermal camera or IR thermometer
- [ ] Ultrasonic microphone for field measurement

**Required for Build 3:**
- [ ] Faraday cage or grounded enclosure
- [ ] Interlock switches on access panels
- [ ] Automatic shutoff on overtemperature
- [ ] Ventilation system (if using high power for extended periods)

---

## 🚑 Emergency Procedures

### Hearing Overexposure
1. Turn off device immediately
2. Move to quiet environment
3. Rest ears for 24 hours (no headphones, loud music, etc.)
4. If tinnitus persists >48 hours, see audiologist

### Thermal Burn from Transducer
1. Turn off device
2. Cool affected area with room-temperature water (not ice)
3. Do not apply ointments
4. If blistering occurs, seek medical attention

### Electrical Shock
1. Do not touch victim if still in contact with power source
2. Cut power at breaker/unplug device
3. Call emergency services if unconscious or burn visible
4. Perform CPR if trained and necessary

### Fire
1. Activate emergency shutoff
2. Use Class C fire extinguisher (do not use water!)
3. Evacuate if fire spreads beyond device
4. Call fire department if unable to extinguish within 10 seconds

---

## 📏 Safe Operating Procedures

### Before Every Use

1. **Visual Inspection:**
   - Check all wiring for fraying or exposed conductors
   - Verify heatsinks are attached and thermal paste is present
   - Ensure no particles are stuck to emitter surfaces
   - Confirm all mounting screws are tight

2. **Power-On Sequence:**
   - Connect to power supply (device OFF)
   - Turn on cooling system (if applicable)
   - Wait 5 seconds for cooling to stabilize
   - Power on control electronics
   - Ramp up emitter power slowly (10% increments)
   - Monitor temperature continuously

3. **Functional Tests:**
   - Verify all emitters are oscillating (check with phone camera - you'll see flickering)
   - Measure sound pressure level (should be >110 dB at trap center)
   - Test with single foam bead before attempting larger particles

### During Operation

- Monitor temperature every 5 minutes (or continuously via display)
- Keep workspace clear of flammable materials
- Maintain ventilation (open window or fan)
- Never leave operating device unattended
- Limit continuous operation: 30 min (Build 1), 20 min (Build 2), 15 min (Build 3)

### After Use

1. Ramp power down slowly (don't shut off abruptly)
2. Allow cooling system to run for 2 minutes after power-off
3. Disconnect from power supply
4. Allow transducers to cool to room temperature (15-30 minutes)
5. Clean any debris from emitter surfaces with soft brush

---

## 🧪 Research Ethics

If using acoustic levitation for biological research:

**Invertebrates (insects, etc.):**
- Limit exposure to <5 minutes
- Monitor for stress behaviors (erratic movement)
- Provide recovery period between trials
- Follow institutional animal care guidelines

**Living cells/tissues:**
- Document all exposure parameters
- Compare with control samples
- Check for cavitation damage (cell lysis)
- Follow IRB/biosafety protocols

**DO NOT attempt:**
- Levitating vertebrate animals (mammals, birds, reptiles, amphibians, fish)
- Human levitation experiments (even partial - hand, finger, etc.)
- Any experiment not approved by ethics review board

---

## 📚 Regulatory Compliance

### United States

**FCC Regulations (RF Emissions):**
- 40 kHz is below FCC Part 15 regulated spectrum (>9 kHz is technically covered, but enforcement is rare)
- Maintain good shielding to prevent electromagnetic interference
- If selling devices commercially, may require FCC testing

**OSHA (Workplace Safety):**
- If used in workplace, follow OSHA noise exposure limits
- Post warning signs for ultrasonic hazards
- Provide PPE (hearing protection) to all workers

**FDA (Medical Devices):**
- If making therapeutic claims, device becomes medical device (requires 510(k) clearance)
- Research/educational use is exempt but document everything

### International

**CE Marking (Europe):**
- Required for commercial sale in EU
- Must meet EMC Directive 2014/30/EU
- Must meet Low Voltage Directive 2014/35/EU

**Other Regions:**
- Check local regulations for ultrasonic devices
- Some countries restrict high-power ultrasonic equipment
- Educational/research use is generally permitted

---

## ⚖️ Legal Disclaimer

**READ CAREFULLY:**

This project is provided for educational and research purposes only. The authors and contributors:

- Make NO warranties about safety or fitness for any purpose
- Are NOT liable for injuries, property damage, or hearing loss
- Are NOT responsible for regulatory non-compliance
- Do NOT endorse any specific use case

**BY BUILDING THIS DEVICE YOU AGREE:**
- You are solely responsible for safe operation
- You will follow all applicable laws and regulations
- You understand the risks and accept them voluntarily
- You will not hold authors liable for any damages

**If you are under 18:**
- Obtain parental/guardian permission
- Work under adult supervision at all times
- Follow all safety guidelines strictly

**Commercial Use:**
- This design is MIT licensed (free to use/modify)
- Commercial builders must obtain own safety certifications
- No liability extends to commercial derivatives

---

## 📞 Resources

**Emergency Contacts:**
- Local emergency services: 911 (US) / 112 (EU)
- Poison control: 1-800-222-1222 (US)
- Electrical safety: Contact local fire department non-emergency

**Safety Information:**
- OSHA Ultrasonic Guidelines: https://www.osha.gov/
- FDA Ultrasound Guidance: https://www.fda.gov/
- IEEE Standards (C95.1): Ultrasonic exposure limits

**Acoustic Safety Papers:**
- Duck, F. (2007). "Medical and non-medical protection standards for ultrasound and infrasound"
- Nyborg, W. L. (2001). "Biological effects of ultrasound: development of safety guidelines"

---

## ✅ Safety Checklist

Print this and check before EVERY use:

### Pre-Operation
- [ ] Safety glasses on
- [ ] Hearing protection on
- [ ] Fire extinguisher within reach
- [ ] Emergency shutoff accessible
- [ ] Workspace clear of flammables
- [ ] Ventilation adequate
- [ ] Visual inspection complete
- [ ] No bystanders within 2 meters

### During Operation
- [ ] Temperature <65°C
- [ ] Sound level <140 dB SPL (measured)
- [ ] All emitters functioning
- [ ] Cooling system operational
- [ ] No unusual odors (burning)
- [ ] No unusual sounds (crackling)
- [ ] Timer set for max operation duration

### Post-Operation
- [ ] Power ramped down slowly
- [ ] Cooling allowed to run
- [ ] Transducers cool to touch
- [ ] No damage observed
- [ ] Workspace cleaned
- [ ] Device secured/stored safely

---

**🛡️ WHEN IN DOUBT, DON'T TURN IT ON. Safety first, always.**

**Questions? See [FAQ](faq.md) or contact the community via GitHub Discussions.**

---

*Last updated: December 2025*
*Version: 1.0*