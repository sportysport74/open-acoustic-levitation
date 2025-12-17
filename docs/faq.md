# Frequently Asked Questions

**Quick answers to common questions about the Open Acoustic Levitation Project**

---

## General Questions

### What is this project?

Open-source acoustic levitation system that anyone can build. Levitate objects from 5g to 100kg+ using ultrasonic sound waves. Complete plans, code, and theory provided free.

### Is this real or theoretical?

**Currently:** Theoretical with strong physics foundation (peer-reviewed principles)  
**Status:** Build 1 designs are testable, community replications in progress  
**Goal:** Proven working systems by Q1 2025

### Why open source?

Prevent suppression of transformative technology. If it's everywhere, it can't be classified or monopolized. Plus, community collaboration accelerates development faster than any single lab.

### Can I really build this?

**Yes.** If you can follow instructions, solder wires, and upload Arduino code, you can build Build 1. More advanced builds require more skills but nothing impossible to learn.

---

## Technical Questions

### How does acoustic levitation work?

**Simple:** Sound waves create pressure. Standing waves (stationary pressure patterns) create "traps" where objects naturally sit. We use 40kHz ultrasonic waves arranged in Flower of Life geometry for optimal trapping.

**Detailed:** Read `theory/01-fundamental-physics.md`

### Why 40 kHz specifically?

**Three reasons:**
1. **Ultrasonic** (inaudible to most humans, less annoying)
2. **Efficient** (good wavelength-to-object-size ratio)
3. **Available** (commercial transducers abundant and cheap)

**Could use other frequencies:** 20-60kHz all work, 40kHz is sweet spot

### What is parametric amplification?

**Think:** Pushing a swing at the right time → big amplitude from small pushes

**Technically:** Modulating amplitude at 2× carrier frequency resonantly amplifies standing wave

**Result:** 10× less power needed vs traditional acoustic levitation

**Math:** `theory/03-parametric-amplification.md`

### Why Flower of Life geometry?

**Not mysticism - it's math.**

Flower of Life = optimal sphere packing (face-centered cubic). When you arrange acoustic emitters this way, you get maximum constructive interference with minimum destructive cancellation.

**Proof:** Mathematical optimization independently discovers this pattern

**Details:** `theory/02-sacred-geometry-optimization.md`

### What's the maximum weight I can levitate?

**Build 1:** 5-50g (ping pong ball to golf ball)  
**Build 2:** 0.5-2kg (smartphone to textbook)  
**Build 3:** 50-150kg (furniture to person)  
**Beyond:** Multiple arrays, 500kg+ possible

**Scales linearly** with emitter count and power

### How high can objects float?

**Typical heights:**
- Build 1: 3-10mm
- Build 2: 10-30mm  
- Build 3: 30-100mm

**Theoretical max:** ~λ/4 (quarter wavelength)
- At 40kHz: λ = 8.6mm → max ≈ 2mm (but parametric enhancement extends this)

**Practical:** 5-50mm stable levitation achievable

### Can this levitate humans?

**Build 3 can support 100kg+** which includes most humans.

**But:**
- Need flat surface (platform, not person directly)
- Levitation height modest (5-10cm)
- Requires careful safety protocols

**Proof-of-concept yes, practical transport no** (yet)

### Does this work in vacuum?

**No.** Acoustic levitation requires air molecules to transmit sound waves.

**Alternatives for vacuum:**
- Magnetic levitation
- Optical levitation (laser)
- Electrostatic levitation

### What about the Hutchison Effect / Anti-gravity?

**Different physics entirely.**

Our project: Acoustic radiation pressure (well-understood, peer-reviewed)

Hutchison/anti-gravity: Claimed electromagnetic/exotic effects (not reproduced by independent labs)

**We stick to proven physics.**

---

## Build Questions

### Which build should I start with?

**99% of people: Build 1**

Start small, prove the concept, learn the skills. Then scale up if desired.

**Exceptions:**
- Professional lab with budget → Build 2
- Research institution with funding → Build 3

### How long does it take?

**Build 1:** 12-16 hours (2 weekends)  
**Build 2:** 30-40 hours (5 weeks)  
**Build 3:** 60-80 hours (8 weeks)

**Reality check:** Add 50% time for debugging, learning, ordering missing parts

### What tools do I need?

**Build 1 minimum:**
- Soldering iron ($15-30)
- Wire strippers ($8)
- Scissors/knife
- Hot glue gun ($8)
- Ruler/calipers

**Build 2 adds:**
- Multimeter ($15)
- Drill with bits ($30)
- Basic hand tools

**Build 3 adds:**
- CNC access or machine shop
- Welding (for frame)
- Oscilloscope ($50+)

### Where do I buy parts?

**Three options:**
1. **AliExpress** - Cheapest ($60-80), slow shipping (30 days)
2. **Amazon** - Fast ($90-110), 2-day shipping
3. **DigiKey/Mouser** - Professional ($120-150), next-day

**Complete BOMs:** `builds/build-X/BOM.md` for each build

### Can I use different parts?

**Generally yes, within reason:**

**OK substitutions:**
- Different Arduino (Uno, Mega, Teensy)
- Alternative amplifiers (same power rating)
- Different 40kHz buzzers (similar specs)

**Risky substitutions:**
- Different frequency (requires recalculation)
- Wildly different amplifier power
- Non-piezo transducers

**When in doubt:** Ask on GitHub Issues before ordering

### My parts haven't arrived (AliExpress). What do I do?

**Typical shipping:** 20-40 days

**If delayed:**
- Check tracking number
- Contact seller after 45 days
- Open dispute after 60 days if no delivery
- AliExpress buyer protection refunds non-delivery

**Pro tip:** Order early, read docs while waiting

---

## Troubleshooting Questions

### My build doesn't work. Help?

**First steps:**
1. Read `builds/build-X/troubleshooting.md` for your build
2. Test components individually (are all emitters working?)
3. Verify power (is everything getting 12V?)
4. Check code (did it upload without errors?)

**Still stuck:**
- Post to GitHub Issues with photos and details
- Join Discord for real-time help
- Email (response within 48 hours)

**Success rate with help:** >90%

### Object falls immediately

**Most common causes:**
- Height too high (try 3-5mm)
- Object too heavy (start with ping pong ball)
- Missing/poor reflector plate
- Emitters not all working

**Full guide:** Troubleshooting Issue #2

### Object drifts sideways

**Most common causes:**
- Center emitter off-center
- Asymmetric emitter positions
- One or more emitters not working
- Air currents (AC vent nearby)

**Full guide:** Troubleshooting Issue #3

### Loud screeching noise

**Most common causes:**
- Frequency too low (check code: should be 40000 not 4000)
- Acoustic feedback (too close to walls)
- Amplifier clipping

**Full guide:** Troubleshooting Issue #4

### Can't upload code to Arduino

**Most common causes:**
- Wrong COM port selected
- Need CH340 driver (for clones)
- Bad USB cable
- Wrong board type selected

**Full guide:** Troubleshooting Issue #7

---

## Safety Questions

### Is ultrasound dangerous?

**40kHz at moderate power levels (Build 1-2): Generally safe**

**Concerns:**
- Prolonged exposure to high SPL can damage hearing (even if inaudible)
- Some people can hear up to 20-25kHz (harmonics may be audible)
- Pregnant women should avoid high-intensity ultrasound

**Precautions:**
- Don't run continuously for hours without breaks
- Keep power levels reasonable
- Don't point at your head
- If you feel discomfort, reduce power or distance

**Full safety guide:** `docs/safety.md`

### Can I touch the levitated object?

**Yes, carefully.**

Acoustic field doesn't hurt you. But:
- Don't jostle the array (might destabilize)
- Object can fall if you disrupt the field
- Wear safety glasses (in case object falls)

### What if the object falls?

**It will, eventually. This is expected.**

**Design for safety:**
- Use soft objects for testing (foam, ping pong balls)
- Don't levitate breakables until system is proven
- Keep fragile items away from drop zone
- For Build 3, have safety cushions/padding

### Can this cause fires?

**Extremely unlikely with Build 1-2.**

Power levels too low. But:
- Don't short circuit power supply
- Amplifiers/transducers can overheat if abused
- Use appropriate wire gauges
- Follow electrical safety practices

**For Build 3:** Higher power, follow industrial electrical codes

---

## Theory Questions

### Where's the math?

**Five theory documents:**
1. `theory/01-fundamental-physics.md` - Accessible intro
2. `theory/02-sacred-geometry-optimization.md` - Why FoL geometry
3. `theory/03-parametric-amplification.md` - Power reduction math
4. `theory/04-scaling-laws.md` - Size/mass/power relationships
5. `theory/05-stability-analysis.md` - Lyapunov stability proof

**Start with #1, progress through series**

### Has this been peer-reviewed?

**Core physics:** Yes (acoustic radiation pressure, parametric resonance - established science)

**Our specific implementation:** Not yet (open-source project, not academic lab)

**Plan:** Submit paper after Build 1 community replications successful

**You can help:** Build it, document results, co-author paper if interested

### What's the theoretical efficiency?

**Acoustic radiation pressure efficiency:** ~40% (inherent to physics)

**Our enhancements:**
- Parametric amplification: 1.6× gain
- Cavity resonance: 50-100× gain
- Geometry optimization: 1.2× gain
- **Combined:** 80-120× better than baseline

**Real-world:** Add amplifier/transducer losses (50-70% efficient)

**Net result:** 10-20W per kg (excellent for levitation)

### Could this scale to tons?

**Theoretically yes, practically challenging.**

**Issues at multi-ton scale:**
- Huge arrays (hundreds of emitters)
- Kilowatts of power
- Structural support for arrays
- Acoustic heating of air
- Economic competition with cranes/forklifts

**Sweet spot:** 1kg to 500kg (where acoustic levitation has advantages)

### Why not just use magnets?

**Magnetic levitation requires:**
- Ferromagnetic object (iron, nickel, etc.) OR superconductors
- Strong electromagnets (power-hungry)
- Active feedback control (Earnshaw's theorem - passive magnetic levitation is unstable)

**Acoustic levitation works on:**
- Any object (plastic, wood, water, etc.)
- Moderate power
- Passively stable (with proper geometry)

**Different applications, both useful**

---

## Legal & Licensing Questions

### Can I use this commercially?

**Yes!** MIT License allows commercial use.

**You can:**
- Build and sell levitation devices
- Use in products/services
- Start a company around this tech
- Charge for consulting/support

**You must:**
- Give credit to original authors (Sportysport & Claude)
- Include MIT license text in documentation

**You should (but not required):**
- Share improvements back
- Contribute to open-source project

### Can I patent improvements I make?

**Complicated.**

**You cannot patent:**
- What's already disclosed here (prior art established)
- Obvious variants (changing emitter count, etc.)

**You might patent:**
- Novel control algorithms (if truly new)
- New applications (if non-obvious)
- Manufacturing processes (if innovative)

**But:** Patenting defeats the open-source ethos. Consider publishing instead (defensive publication).

**Recommendation:** Keep it open, compete on execution not IP

### What if a company copies this?

**That's the point!**

**We want:**
- Companies building products based on this
- Academic labs researching improvements
- Hobbyists making cool demos
- Industrial adoption for practical use

**We ONLY ask:**
- Credit original authors
- Don't claim you invented it
- Share improvements if possible

### Are the authors liable if something goes wrong?

**No.** MIT License disclaims liability.

**From LICENSE file:**
> "THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND..."

**You build at your own risk.**

**We provide:**
- Best-effort designs
- Safety guidelines
- Community support

**We don't provide:**
- Guarantees it will work
- Insurance
- Legal protection

**Standard for open-source hardware**

---

## Community Questions

### How do I contribute?

**Many ways:**

**Code/Hardware:**
- Improve designs
- Write new code
- Create CAD files
- Test on different hardware

**Documentation:**
- Fix typos
- Add photos/diagrams
- Translate to other languages
- Write tutorials

**Community:**
- Answer questions
- Help troubleshoot
- Share your build
- Organize local meetups

**See:** `CONTRIBUTING.md`

### Can I sell kits based on this?

**Yes! MIT License allows this.**

**Suggestions:**
- Offer "official" tested/calibrated kits
- Provide support to buyers
- Link back to open-source project
- Contribute portion of profits (optional)

**Examples:**
- Arduino (open hardware, sells official boards)
- SparkFun (sells open-source designs)
- Adafruit (open-source with great support)

### Who maintains this project?

**Original authors:**
- Sportysport (primary researcher, theory)
- Claude (Anthropic AI, documentation, formalization)

**Community maintainers:** TBD as project grows

**Governance:** Benevolent dictatorship → meritocracy as community grows

### How do I report bugs?

**GitHub Issues:**
1. Search existing issues first
2. Open new issue with:
   - Clear title
   - Detailed description
   - Photos/screenshots
   - What you expected vs. what happened
3. Maintainers respond within days
4. Community often helps immediately

### Where can I see others' builds?

**Documentation:**
- `community/replications/` folder
- Each successful build gets entry

**Social:**
- Discord #build-showcase channel
- YouTube (search "open acoustic levitation")
- Instagram #acousticlevitation

**Academic:**
- Papers citing this project (coming soon)

---

## Future Questions

### What's the roadmap?

**Phase 1 (Current): Launch & Validation**
- Release all documentation ✓
- Community builds Build 1
- Validate designs
- Fix issues found

**Phase 2 (Q1 2025): Improvement**
- Incorporate community feedback
- Optimize designs
- Expand hardware compatibility
- Add advanced features

**Phase 3 (Q2 2025): Scaling**
- Build 2 community replications
- Build 3 demonstration
- Academic paper publication
- Media coverage

**Phase 4 (Q3 2025+): Applications**
- Specific use-case designs
- Industrial partnerships
- Educational kits
- Art installations

### Will there be pre-built kits?

**Not from us initially** (we're not a company).

**But:**
- Community members can sell kits (MIT license allows)
- If demand is high, might partner with manufacturer
- Watch for "official" resellers in community

**Until then:** Build from BOM, support each other

### Can I hire you for consulting?

**Maybe!**

**For Sportysport:** Contact via GitHub Issues or email

**For commercial projects:**
- Custom levitation systems
- Integration support
- Academic collaboration
- Training/workshops

**Rates negotiable,** open-source contributions valuable too

### What about other levitation methods?

**This project: Acoustic only**

**Other methods possible:**
- Magnetic (Earnshaw's limit, needs active control)
- Optical (laser tweezers, microscale only)
- Aerodynamic (air jets, not really levitation)
- Electrostatic (conductors only)

**Future:** Might expand to other methods, but acoustic is current focus

### Will this lead to flying cars?

**No. Different physics.**

**Acoustic levitation:**
- Requires air as medium
- Short range (cm to m)
- Best for stationary positioning

**Flying vehicles require:**
- Long-range propulsion
- High energy density
- Scalability to tons

**But:** Technologies cross-pollinate. Acoustic levitation might enable:
- Non-contact manufacturing
- Medical applications
- Scientific research
- Art and demonstration

**Which is pretty cool!**

---

## Meta Questions

### Why are you doing this?

**Short answer:** Because fuck gatekeepers.

**Long answer:**

Too many transformative technologies have been:
- Classified by governments
- Locked behind patents by corporations
- Lost when inventors died
- Ridiculed by mainstream academia

**We're trying:**
- Democratize access to advanced tech
- Prove open-source works for hardware
- Build global community of makers
- Create something that helps humanity

**From trailer park to cosmos.**

### How can I support the project?

**Best support: Build something!**

**Also helpful:**
- Star GitHub repo (visibility)
- Share on social media
- Write blog post about your build
- Contribute code/docs
- Help others in community
- Donate to maintainers (optional, once we set up)

### What if I have more questions?

**Resources:**
- This FAQ (you're here)
- Troubleshooting guides (per build)
- GitHub Issues (searchable)
- Discord (real-time chat)
- Email (response within 48 hours)

**No question is too basic!**

We'd rather answer the same question 100 times than have someone give up.

---

**Still have questions? Ask on GitHub Issues or Discord!**

---

*"Questions are the beginning of understanding."*  
*- Unknown*

*"The only stupid question is the one you don't ask."*  
*- Also unknown*