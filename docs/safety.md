# Safety Guidelines for Acoustic Levitation Systems

**READ THIS BEFORE BUILDING OR OPERATING ANY LEVITATION SYSTEM**

---

## ⚠️ Critical Safety Statement

Acoustic levitation systems use high-intensity ultrasonic sound. While generally safe when used properly, they can cause harm if misused.

**By building and operating these systems, you accept all responsibility for:**
- Your own safety
- Safety of others nearby
- Damage to property
- Compliance with local regulations

**The authors and contributors provide these designs "AS IS" with NO WARRANTY and NO LIABILITY for any harm or damage.**

---

## Risk Assessment by Build Level

### Build 1 (Micro-Scale): LOW RISK

**Power level:** 5-10W  
**SPL:** 120-130 dB at 40kHz  
**Risk level:** Minimal with basic precautions

**Primary hazards:**
- Electrical (12V, low risk)
- Falling objects (small mass, low impact)
- Hearing (prolonged exposure)
- Eye injury (if components fail)

**Mitigation:** Wear safety glasses, limit exposure time, follow electrical safety

---

### Build 2 (Lab-Scale): MODERATE RISK

**Power level:** 100-300W  
**SPL:** 140-150 dB at 40kHz  
**Risk level:** Requires proper safety protocols

**Primary hazards:**
- Acoustic intensity (can cause discomfort/damage)
- Electrical (48V, shock hazard)
- Falling objects (1kg can injure)
- Component failure (explosive at high power)

**Mitigation:** Enclosed operation, hearing protection, emergency stop, electrical safety training

---

### Build 3 (Human-Scale): HIGH RISK

**Power level:** 2-5 kW  
**SPL:** 150-160 dB at 40kHz  
**Risk level:** Industrial safety standards required

**Primary hazards:**
- Acoustic intensity (serious injury possible)
- Electrical (industrial voltages, arc flash)
- Falling objects (100kg+ can be fatal)
- Structural failure (array collapse)
- Fire (high power)

**Mitigation:** Full safety enclosure, interlocks, emergency stop, professional electrical installation, operator training, permits/inspections

---

## Acoustic Hazards

### Understanding Sound Pressure Level (SPL)

**Decibels (dB):** Logarithmic scale of acoustic intensity

**Reference levels:**
- 0 dB: Threshold of hearing
- 60 dB: Normal conversation
- 90 dB: Lawnmower (hearing damage with prolonged exposure)
- 120 dB: Threshold of pain (audible frequencies)
- 140 dB: Immediate hearing damage (audible frequencies)

**For ultrasonic (40kHz):**
- Not audible to most humans
- **But damage is still possible!**
- Thresholds are less well-studied than audible frequencies

### Safe Exposure Limits

**OSHA standards (for audible frequencies):**
- 90 dB: 8 hours/day maximum
- 95 dB: 4 hours/day maximum
- 100 dB: 2 hours/day maximum
- 105 dB: 1 hour/day maximum
- 110 dB: 30 minutes/day maximum
- 115 dB: 15 minutes/day maximum

**For ultrasonic (40kHz):**
- No established OSHA limits
- Conservative approach: Use audible frequency limits
- Research shows potential for hearing damage at high SPL even if inaudible

**Our recommendation:**

| Build | SPL | Maximum Continuous Exposure |
|-------|-----|----------------------------|
| Build 1 | 120-130 dB | 1 hour/day |
| Build 2 | 140-150 dB | 15 minutes/day |
| Build 3 | 150-160 dB | 5 minutes/day (operator training required) |

### Symptoms of Ultrasonic Exposure

**Immediate effects:**
- Headache
- Dizziness
- Nausea
- Ear pressure/fullness
- Tinnitus (ringing in ears)

**Delayed effects (hours to days later):**
- Fatigue
- Difficulty concentrating
- Sleep disturbance
- Persistent tinnitus

**Long-term effects (repeated exposure):**
- Hearing loss (permanent)
- Tinnitus (chronic)
- Vestibular dysfunction (balance problems)

**If you experience ANY symptoms:**
1. Stop operation immediately
2. Leave area
3. Seek medical attention if symptoms persist
4. Do not resume operation until symptoms resolve
5. Reduce power or increase distance for future operation

---

## Electrical Hazards

### Voltage Levels and Risk

**Build 1 (12V DC):**
- Generally safe (below 50V threshold)
- Can cause burns if short-circuited
- Battery/PSU can deliver high current

**Build 2 (48V DC):**
- Approaching hazardous threshold
- Shock possible (especially if wet)
- Can cause involuntary muscle contractions

**Build 3 (Industrial voltages, potentially 120-240V AC):**
- Lethal shock hazard
- Arc flash risk
- Requires licensed electrician

### Electrical Safety Practices

**All builds:**
- [ ] Disconnect power before touching any wiring
- [ ] Use insulated tools
- [ ] Check for shorts with multimeter before power-on
- [ ] Keep liquids away from electronics
- [ ] Don't work on live circuits (if you can avoid it)
- [ ] Have fire extinguisher nearby (Class C - electrical)

**Build 2-3 additionally:**
- [ ] Use GFCI/RCD protection (ground fault protection)
- [ ] Proper grounding of all metal enclosures
- [ ] Insulated work area (rubber mat)
- [ ] One hand in pocket when working near live circuits (prevents current through heart)
- [ ] Lockout/tagout procedures for maintenance
- [ ] Arc-rated PPE (for Build 3)

### Signs of Electrical Problems

**Stop immediately if you observe:**
- Smoke or burning smell
- Sparks or arcing
- Components very hot to touch (>60°C / 140°F)
- Discoloration of wiring insulation
- Buzzing/crackling sounds from power supply
- Unexpected voltage measurements

**Troubleshoot offline (power disconnected), never live.**

---

## Mechanical Hazards

### Falling Objects

**All builds have falling object risk.**

**Severity:**
- Build 1: 5-50g → minor bruise, possible eye injury
- Build 2: 1kg → significant bruise, broken finger possible
- Build 3: 100kg → serious injury or death

**Mitigation:**

**For all builds:**
- [ ] Wear safety glasses (ANSI Z87.1 rated)
- [ ] Clear area below levitation zone
- [ ] Start with soft/light test objects
- [ ] Don't levitate over people or valuable equipment
- [ ] Have second person spot you during tests

**For Build 2-3:**
- [ ] Safety cage/enclosure around levitation zone
- [ ] Emergency stop accessible
- [ ] Warning lights when system active
- [ ] Soft landing cushion in case of failure
- [ ] Never put body parts in active field

### Component Failure

**High-power ultrasonic transducers can fail explosively.**

**Risk factors:**
- Over-voltage
- Over-current
- Thermal runaway
- Manufacturing defects
- Resonance at wrong frequency

**Symptoms before failure:**
- Transducer getting very hot
- Change in sound (cracking, popping)
- Reduced output
- Visible damage to element

**Mitigation:**
- [ ] Current limiting on each transducer
- [ ] Thermal monitoring (>85°C shutdown)
- [ ] Operate at <80% of rated power
- [ ] Inspect transducers regularly
- [ ] Replace if any damage visible
- [ ] Safety enclosure (contains fragments)

---

## Physiological Effects

### Who Should NOT Operate These Systems

**Absolute contraindications:**
- Pregnant women (ultrasound effects on fetus unknown)
- People with pacemakers or medical implants
- People with recent ear surgery
- People with active ear infections
- Children under 16 (still-developing hearing)

**Relative contraindications (use caution):**
- People with hearing loss (more susceptible to further damage)
- People with tinnitus (may worsen)
- People prone to migraines (ultrasound can trigger)
- People with epilepsy (bright lights + sound may trigger seizures)

**If you have any medical conditions, consult your doctor before operating.**

### Hearing Protection

**Build 1:**
- Optional but recommended for extended operation
- Foam earplugs (NRR 20-30) adequate

**Build 2:**
- Recommended for all operation
- Foam earplugs or earmuffs (NRR 25-35)

**Build 3:**
- REQUIRED for all personnel in area
- Industrial hearing protection (NRR 30-35)
- Dual protection (earplugs + earmuffs) for prolonged exposure

**Note:** Hearing protection is primarily for audible harmonics and amplifier noise. Ultrasonic protection is limited.

### Other PPE (Personal Protective Equipment)

**All builds:**
- Safety glasses (ANSI Z87.1)
- Closed-toe shoes
- No loose clothing near moving parts

**Build 2-3:**
- Hearing protection
- Lab coat (protects from minor spills/debris)
- Insulated gloves (when working on power systems)

**Build 3 additionally:**
- Hard hat (if overhead hazards)
- High-visibility vest (if multiple personnel)
- Arc-rated PPE (when working on live electrical)

---

## Operational Safety Procedures

### Pre-Operation Checklist

**Before every power-on:**

- [ ] Visual inspection (no visible damage, loose wires, etc.)
- [ ] Area clear (no people/objects in drop zone)
- [ ] Safety equipment ready (glasses, hearing protection)
- [ ] Emergency stop accessible
- [ ] Fire extinguisher in reach
- [ ] All personnel briefed on hazards
- [ ] Test object secured to reflector plate
- [ ] Power supply voltage verified correct
- [ ] All grounds connected

### During Operation

- [ ] Monitor system continuously (don't leave unattended)
- [ ] Watch for signs of overheating, unusual sounds, smoke
- [ ] Limit exposure time (see exposure limits above)
- [ ] Keep hands/face away from active field
- [ ] Don't disassemble or adjust while powered
- [ ] Have second person present (for Build 2-3)

### Emergency Procedures

**If something goes wrong:**

1. **STOP IMMEDIATELY** - Press emergency stop or unplug power
2. **Evacuate area** - Get everyone away from system
3. **Assess situation** - Is there fire? Injury? Electrical hazard?
4. **Call for help** - 911 if needed, supervisor/safety officer otherwise
5. **Secure area** - Prevent others from approaching
6. **Document** - Take photos, write incident report
7. **Don't restart** - Until root cause identified and fixed

**Emergency contacts (post visibly):**
- Emergency services: 911 (US), 999 (UK), 112 (EU)
- Poison control: 1-800-222-1222 (US)
- Electrical emergency: Local utility company
- Facility safety officer: [Your contact info]

---

## Environmental Considerations

### Acoustic Pollution

**Ultrasonic noise can affect:**
- Pets (dogs, cats can hear up to 45-60 kHz)
- Wildlife (bats, rodents, insects)
- Sensitive electronic equipment
- Neighbors (through walls, especially in apartments)

**Mitigation:**
- [ ] Operate away from pets
- [ ] Not near wildlife habitats (if outdoors)
- [ ] Acoustic shielding (foam walls reduce transmission)
- [ ] Inform neighbors if in shared building
- [ ] Limit operation to reasonable hours (not 2 AM)

### Electromagnetic Interference (EMI)

**High-frequency switching can cause:**
- Radio/TV interference
- Wi-Fi disruption
- Interference with medical devices (pacemakers)

**Mitigation:**
- [ ] Shielded cables where possible
- [ ] Grounding of enclosures
- [ ] Ferrite beads on power cables
- [ ] Distance from sensitive equipment
- [ ] FCC compliance testing (if commercial)

### Heat Dissipation

**High-power systems generate significant heat.**

**Fire hazards:**
- Hot transducers near flammable materials
- Amplifiers overheating
- Wiring insulation melting
- Power supply failure

**Mitigation:**
- [ ] Adequate ventilation
- [ ] Fire-resistant mounting materials
- [ ] Thermal monitoring and shutdown
- [ ] Keep flammables away (paper, cloth, etc.)
- [ ] Fire extinguisher (Class C for electrical)

---

## Specific Build Considerations

### Build 1 Specific Safety

**Primary concerns:**
- Soldering burns
- Eye injury from falling small objects
- Minor electrical shock (unlikely at 12V)

**Specific precautions:**
- Unplug soldering iron when not in use
- Use helping hands or vice to hold parts
- Solder in ventilated area (lead fumes)
- Safety glasses during all testing
- Don't touch transducers while powered (vibration can be uncomfortable)

**Low-risk build, but still follow basic safety.**

---

### Build 2 Specific Safety

**Primary concerns:**
- Acoustic intensity (140-150 dB possible)
- 48V electrical system (shock hazard)
- 1kg object falling from height
- FPGA programming errors (could cause unsafe operation)

**Specific precautions:**
- **Enclosure required** (acrylic box with interlocked door)
- Hearing protection during operation
- Emergency stop button (breaks power to all transducers)
- Software watchdog (automatic shutdown if control loop hangs)
- Fall cushion (foam pad below levitation zone)
- GFCI protection on power supply
- Calibration procedure (verify safe operation before full power)

**Requires operator training and written procedures.**

---

### Build 3 Specific Safety

**This is an INDUSTRIAL SYSTEM. Treat it accordingly.**

**Required safety systems:**
- Light curtain or safety cage (prevents access while operating)
- Emergency stop (mushroom button, breaks all power)
- Warning lights and horn (system active indicator)
- Interlocked doors (system stops if opened)
- Redundant safety relays (fail-safe design)
- Thermal shutdown (multiple temperature sensors)
- Current limiting (per-transducer and total)
- Tilt sensors (shutdown if platform tilts >5°)
- UPS backup (graceful shutdown on power loss)

**Required procedures:**
- Lockout/tagout for maintenance
- Permit to work (for non-operators)
- Daily inspection checklist
- Monthly safety system testing
- Annual professional inspection

**Required training:**
- Operator certification (8-hour course)
- Electrical safety (NFPA 70E)
- First aid/CPR
- Emergency procedures

**Liability:**
- Professional liability insurance recommended
- Compliance with OSHA (US), HSE (UK), or local authority
- May require permits for operation
- Consult with safety professional before building

**Build 3 is NOT a hobbyist project. It's a serious engineering undertaking.**

---

## Legal and Regulatory Considerations

### Standards and Codes

**May apply depending on location:**
- **Electrical:** NFPA 70 (NEC), IEC 60950, local electrical codes
- **Acoustic:** OSHA 1910.95 (occupational noise), local noise ordinances
- **Mechanical:** ASME B30 (lifting devices), local building codes
- **General safety:** ISO 12100 (machinery safety), CE marking (EU)

**Check with local authorities before building Build 2 or 3.**

### Liability and Insurance

**Personal use:**
- Homeowner's/renter's insurance may not cover "experimental devices"
- Consider additional liability coverage
- Keep thorough documentation (shows due diligence)

**Commercial use:**
- Professional liability insurance required
- Product liability if selling devices
- Workers compensation if employees involved
- Consult with insurance broker

### Permits

**May be required for:**
- High-power electrical installation (>1kW)
- Operation in commercial/industrial space
- Public demonstrations
- Research involving human subjects (IRB approval)

**Check with:**
- Building department (structural/electrical permits)
- Fire marshal (high-power systems)
- Zoning board (commercial use of residential space)
- University IRB (if academic research)

---

## Testing and Commissioning

### Initial Testing Protocol

**Never go straight to full power.**

**Staged power-up:**

1. **Bench test (no transducers):**
   - Verify power supply voltages
   - Test control system (all channels outputting)
   - Check software (no errors, correct frequencies)

2. **Single transducer test (low power):**
   - Connect one transducer
   - Operate at 25% power
   - Verify 40kHz signal with spectrum analyzer
   - Check for overheating (should be barely warm)

3. **Full array test (low power):**
   - Connect all transducers
   - Operate at 25% power
   - Verify all channels working
   - Check phase relationships (if instrumented)

4. **Levitation test (medium power):**
   - Ramp to 50% power
   - Attempt levitation with light object
   - If successful, gradually increase power until stable
   - Note optimal power level

5. **Full power test (if needed):**
   - Only if medium power insufficient
   - Incrementally increase to 75%, then 90%
   - Monitor temperatures continuously
   - Stop if any component exceeds 80°C

**Never exceed 90% of rated power for continuous operation.**

### Acceptance Testing

**Before declaring system "complete":**

- [ ] Levitate target mass for 1 hour continuously (no failures)
- [ ] Disturbance rejection test (poke object, recovers in <5s)
- [ ] Emergency stop test (all power cuts immediately)
- [ ] Thermal stability (no thermal runaway after 2 hours)
- [ ] Repeatability (10 levitation attempts, 100% success)
- [ ] Safety system test (all interlocks, sensors working)
- [ ] Documentation complete (procedures, schematics, BOM)

**For Build 3:** Professional safety inspection recommended.

---

## Maintenance and Inspection

### Daily (Before Each Use)

- [ ] Visual inspection (no obvious damage)
- [ ] Test emergency stop
- [ ] Check power supply output voltage
- [ ] Verify all transducers producing sound

### Weekly

- [ ] Inspect all connections (tighten if loose)
- [ ] Check transducer mounting (re-glue if needed)
- [ ] Clean dust from electronics
- [ ] Verify acoustic output (spectrum analyzer)

### Monthly

- [ ] Full electrical continuity check
- [ ] Thermal imaging (look for hot spots)
- [ ] Mechanical inspection (base platform, mounts)
- [ ] Calibration check (frequency, phase, amplitude)
- [ ] Safety system functional test
- [ ] Update maintenance log

### Annually

- [ ] Replace worn components (transducers have finite life)
- [ ] Professional electrical inspection (Build 3)
- [ ] Recalibration
- [ ] Document any performance degradation
- [ ] Review and update procedures

---

## Decommissioning and Disposal

### Safe Shutdown

**When retiring a system:**

1. **Final power-down**
   - Disconnect all power sources
   - Discharge capacitors (wait 5 minutes, then short with insulated tool)
   - Label "NOT FOR OPERATION"

2. **Disassembly**
   - Remove transducers carefully (may be fragile)
   - Desolder components (reuse or recycle)
   - Separate materials (metal, plastic, electronics)

3. **Disposal**
   - Electronics: E-waste recycling (contains lead solder)
   - Transducers: Check for ceramic components (special disposal)
   - Batteries: Hazardous waste (if present)
   - Structural: Scrap metal or regular trash (if wood/plastic)

**Never just throw in regular trash** - electronics contain hazardous materials.

---

## Conclusion

**Acoustic levitation is inherently safe when designed and operated properly.**

**The keys to safety:**
1. **Understand the hazards** (read this entire document)
2. **Design for safety** (interlocks, fail-safes, guards)
3. **Follow procedures** (checklists, staged testing)
4. **Use PPE** (glasses, hearing protection)
5. **Maintain equipment** (regular inspections)
6. **Train operators** (everyone knows emergency procedures)
7. **Stay vigilant** (don't get complacent)

**Remember:**
- Safety is not optional
- Shortcuts lead to accidents
- When in doubt, stop and reassess
- It's better to over-engineer safety than under-engineer it

**If you're not comfortable with any safety aspect of a build, DON'T BUILD IT.**

Either:
- Build a lower-power version
- Get professional help
- Wait until you have proper training/facilities

**No levitation demo is worth an injury.**

---

## Resources

**Safety organizations:**
- OSHA: www.osha.gov (US occupational safety)
- NIOSH: www.cdc.gov/niosh (research and recommendations)
- HSE: www.hse.gov.uk (UK workplace safety)
- ACGIH: www.acgih.org (exposure limit guidelines)

**Standards bodies:**
- NFPA: www.nfpa.org (electrical codes)
- IEC: www.iec.ch (international electrical standards)
- ISO: www.iso.org (international safety standards)

**Training:**
- Local community colleges (electrical safety courses)
- Red Cross (first aid/CPR)
- Online: Coursera, edX (safety engineering)

**Further reading:**
- WHO: "Environmental Health Criteria 22: Ultrasound"
- ACGIH: "Threshold Limit Values for Ultrasound"
- NIOSH: "Occupational Noise Exposure"

---

**Questions about safety? Ask before building, not after an accident.**

**GitHub Issues, Discord, or email - we're here to help you build safely.**

---

*"Safety doesn't happen by accident."*  
*- Unknown*

*"Better a thousand times careful than once dead."*  
*- Proverb*

*"An ounce of prevention is worth a pound of cure."*  
*- Benjamin Franklin*

*"Build cool things. Stay safe while doing it."*  
*- Us*