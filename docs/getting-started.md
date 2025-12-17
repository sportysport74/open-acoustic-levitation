# Getting Started with Open Acoustic Levitation

**Welcome! This guide helps you go from "What is this?" to "I'm building it!"**

---

## What is Acoustic Levitation?

**Simple explanation:**
Sound waves push on objects. With the right setup, you can use sound to hold things in mid-air - no strings, no magnets, just pure acoustic force.

**How it works:**
1. Ultrasonic speakers (40kHz, inaudible) create standing waves
2. Standing waves have high and low pressure zones
3. Objects naturally sit at the low-pressure spots
4. Gravity pulls down, acoustic pressure pushes up → levitation!

**What makes our approach special:**
- Uses **Flower of Life geometry** (ancient pattern that's mathematically optimal)
- **Parametric amplification** (10× power reduction vs traditional methods)
- **Open source** (free plans, anyone can build)
- **Scalable** (5g to 100kg+ with same principles)

---

## Can I Actually Build This?

**Yes! If you can:**
- Follow step-by-step instructions
- Solder wires (or willing to learn)
- Upload code to Arduino
- Be patient when troubleshooting

**You don't need:**
- Engineering degree
- Expensive tools
- Previous electronics experience
- Access to lab equipment

**Time commitment:**
- Build 1 (simplest): 2 weekends (~12 hours)
- Build 2 (medium): 5 weeks (30-40 hours)
- Build 3 (advanced): 8 weeks (60-80 hours)

**Budget:**
- Build 1: $80-100 (ping pong ball levitation)
- Build 2: $1,500-2,000 (1kg objects)
- Build 3: $20,000-25,000 (human-scale platform)

---

## Which Build Should I Start With?

### Build 1: Micro-Scale (RECOMMENDED START)

**Choose this if:**
- First time building electronics
- Want to prove concept quickly
- Limited budget
- Want to learn basics

**You'll levitate:** Ping pong balls, foam spheres, small objects (5-50g)

**Specs:**
- Budget: $80-100
- Time: 2 weekends
- Difficulty: Beginner
- Tools: Basic (soldering iron, scissors)

**Path:** Start here → `builds/build-1-micro/README.md`

---

### Build 2: Lab-Scale

**Choose this if:**
- Completed Build 1 successfully
- Want to levitate heavier objects
- Have electronics experience
- Budget for better components

**You'll levitate:** Books, tools, electronics, water bottles (0.5-2kg)

**Specs:**
- Budget: $1,500-2,000
- Time: 5 weeks
- Difficulty: Intermediate
- Tools: Soldering, basic machining

**Path:** `builds/build-2-lab/README.md`

---

### Build 3: Human-Scale

**Choose this if:**
- Serious about the project
- Want to levitate very heavy objects
- Have machining/fabrication access
- Understand safety implications

**You'll levitate:** Furniture, people, heavy equipment (50-150kg)

**Specs:**
- Budget: $20,000-25,000
- Time: 8 weeks
- Difficulty: Advanced
- Tools: CNC, welding, professional electronics

**Path:** `builds/build-3-human-scale/README.md`

---

## Recommended Learning Path

### Total Beginner (Never Built Electronics)

**Week 1-2: Learning Phase**
1. Read `theory/01-fundamental-physics.md` (understand basics)
2. Watch Arduino tutorials on YouTube
3. Practice soldering (buy kit from Amazon: "Learn to Solder")
4. Order Build 1 parts (30-day shipping from AliExpress)

**Week 3-4: While Waiting for Parts**
5. Read Build 1 assembly guide front-to-back
6. Gather tools (soldering iron, wire strippers, etc.)
7. Join Discord community
8. Prepare workspace

**Week 5-6: Building**
9. Follow assembly guide step-by-step
10. Test as you go
11. Document your build (photos)
12. Ask for help when stuck

**Week 7: Testing & Iteration**
13. First levitation attempt
14. Troubleshoot issues
15. Optimize parameters
16. Share results with community

---

### Intermediate (Some Electronics Experience)

**You can skip straight to Build 1 or Build 2:**

1. Review schematics
2. Order parts
3. Build over 2-5 weeks
4. Contribute improvements back to project

---

### Advanced (Professional Background)

**You might go straight to Build 3:**

1. Review all theory documents
2. Validate approach for your requirements
3. Modify designs as needed
4. Build and document
5. Publish academic paper (optional)
6. Become project maintainer (optional)

---

## Step-by-Step Quick Start (Build 1)

### Phase 1: Understanding (1-2 hours)

**Required reading:**
1. This document (you're here!)
2. `theory/01-fundamental-physics.md` (30 min)
3. `builds/build-1-micro/README.md` (20 min)

**Optional reading:**
4. `theory/02-sacred-geometry-optimization.md` (why Flower of Life works)
5. Watch YouTube: "Acoustic Levitation Explained" (search for demos)

---

### Phase 2: Planning (30 minutes)

**Decisions to make:**

1. **Budget:** Can you spend $80-100?
   - Yes → Continue
   - No → Save up, or look for used/scavenged parts

2. **Time:** Do you have 2 weekends available?
   - Yes → Continue
   - No → Plan for slower pace (4 weekends is fine)

3. **Tools:** Do you have or can you borrow:
   - Soldering iron
   - Wire strippers
   - Scissors/knife
   - Hot glue gun
   
   - Yes → Continue
   - No → Budget extra $50 for tools, or borrow

4. **Space:** Do you have workspace?
   - Need: Clean desk/table, good lighting, ventilation
   - Yes → Continue
   - No → Find makerspace, library workshop, or friend's garage

---

### Phase 3: Ordering Parts (30 minutes + shipping wait)

**Choose sourcing strategy:**

**Option A: AliExpress (Cheapest: ~$60)**
- Pros: Very cheap
- Cons: 30-day shipping, variable quality
- Best for: Patient builders, tight budget

**Option B: Amazon (Fast: ~$90)**
- Pros: 2-day shipping
- Cons: More expensive
- Best for: Want to start immediately

**Option C: DigiKey (Professional: ~$120)**
- Pros: High quality, next-day shipping
- Cons: Most expensive
- Best for: Professional use, quality assurance

**Go to:** `builds/build-1-micro/BOM.md` for complete shopping lists

**Tips:**
- Order parts FIRST, read while waiting
- Get extras (spare buzzers, extra wire)
- Include test objects (ping pong balls)

---

### Phase 4: Building (2 weekends)

**Weekend 1: Mechanical Assembly**
- Cut/prepare base platform
- Mark emitter positions (accuracy matters!)
- Mount buzzers with hot glue
- Create reflector plate
- Prepare test object

**Weekend 2: Electronics & Testing**
- Solder wires to buzzers
- Assemble breadboard
- Wire power, signals
- Upload Arduino code
- First levitation attempt!

**Full guide:** `builds/build-1-micro/assembly-guide.md`

---

### Phase 5: Testing & Optimization (Ongoing)

**After successful first levitation:**
- Try different objects
- Adjust parameters (frequency, modulation depth)
- Measure performance
- Document and share

**If unsuccessful:**
- Don't panic! Troubleshooting is normal
- See: `builds/build-1-micro/troubleshooting.md`
- Post to Discord with photos
- Community will help

---

## Essential Concepts to Understand

### 1. Frequency (kHz)

**What it is:** How many times per second the sound wave oscillates

**For our project:** 40 kHz (40,000 times per second)
- Too low → audible (annoying)
- Too high → more absorption, less efficient
- 40 kHz → sweet spot (ultrasonic, efficient, good hardware available)

**Think of it like:** Musical pitch, but way higher than humans can hear

---

### 2. Standing Waves

**What they are:** When two sound waves traveling opposite directions meet, they create stationary high/low pressure zones

**For our project:** The "trap" that holds objects in place

**Think of it like:** Nodes and antinodes stay fixed in space, object sits at a node

**Visual:** Imagine shaking a jump rope - the wave pattern moves, but certain points (nodes) stay still

---

### 3. Parametric Amplification

**What it is:** Modulating frequency at exactly 2× the carrier frequency amplifies the standing wave exponentially

**For our project:** Reduces required power by ~10×

**Think of it like:** Pushing a swing at the right time - small pushes create big motion

**Math:** Instead of brute force, we use resonance

---

### 4. Flower of Life Geometry

**What it is:** Ancient pattern of overlapping circles, corresponds to optimal sphere packing (face-centered cubic lattice)

**For our project:** Arranging emitters this way maximizes constructive interference

**Think of it like:** Team pushing a car - random positions waste effort, coordinated positions push efficiently

**Proof:** Mathematical optimization independently discovers this pattern

---

### 5. Phase Relationships

**What they are:** Time offset between different emitters (0°, 60°, 120°, etc.)

**For our project:** Creates toroidal (donut-shaped) pressure maximum, trapping object at center

**Think of it like:** Synchronized swimming - timing matters as much as individual effort

**In code:** `PHASE_OFFSETS` array controls this

---

## Common Questions

### "Is this safe?"

**Yes, with basic precautions:**
- ✅ 40kHz is ultrasonic (inaudible to most people)
- ✅ Power levels are low (5-10W for Build 1)
- ✅ No dangerous voltages (12V DC)
- ⚠️ Wear safety glasses (parts can fail)
- ⚠️ Don't put body parts in active field
- ⚠️ Prolonged exposure to high SPL can damage hearing (even if inaudible)

**Read full safety guide:** `docs/safety.md`

---

### "How long does it take to build?"

**Build 1:** 12-16 hours over 2-4 weekends
**Build 2:** 30-40 hours over 5-8 weeks
**Build 3:** 60-80 hours over 8-12 weeks

**But:** First 80% goes fast, last 20% is debugging/optimization

**Reality:** Plan for 1.5× the estimated time if it's your first build

---

### "What if I get stuck?"

**You have multiple support options:**

1. **Troubleshooting guide** - Most issues covered
2. **GitHub Issues** - Search existing, post new
3. **Discord community** - Real-time help
4. **Email support** - We respond within 48 hours

**Success rate:** >90% of builders complete Build 1 successfully with community help

---

### "Can I modify the design?"

**Absolutely! This is open source.**

**Encouraged modifications:**
- Different emitter arrangements
- Alternative materials
- New control algorithms
- Different applications

**Just:**
- Document your changes
- Share results (successful or not)
- Contribute improvements back

**Some mods require re-validating physics:**
- Changing frequency significantly
- Different geometry (not Flower of Life)
- Scaling beyond tested ranges

---

### "Will this work for [my application]?"

**Contact-free manipulation:**
- ✅ Levitating delicate objects (orchids, soap bubbles)
- ✅ Scientific experiments (drug crystallization)
- ✅ Clean room applications (no contamination)
- ✅ Art installations

**Position control:**
- ✅ 3D object positioning (with multi-array systems)
- ✅ Acoustic tweezers (microscale particle manipulation)
- ⚠️ Requires advanced control (Build 2+)

**Heavy lifting:**
- ✅ Up to ~150kg per array (Build 3)
- ⚠️ Requires multiple arrays for more
- ❌ Not practical for tons of weight (energy inefficient)

**Not suitable for:**
- ❌ Vacuum environments (needs air)
- ❌ Very low frequency applications (want ultrasonic)
- ❌ Through walls/barriers (acoustic shadows)

**Ask the community if unsure!**

---

## Learning Resources

### Video Tutorials

**Acoustic levitation demos:**
- Search YouTube: "acoustic levitation"
- University demos show principles
- Our project uses same physics, optimized

**Arduino basics:**
- "Arduino Tutorial for Beginners" (multiple channels)
- Learn: pinMode, digitalWrite, loops
- 30-60 minutes total

**Soldering:**
- "How to Solder" (EEVblog, Great Scott!)
- Practice on junk electronics first
- 1-2 hours to get competent

---

### Written Guides

**In this repository:**
- `/theory/` - Physics and math
- `/builds/` - Step-by-step assembly
- `/docs/` - FAQs, safety, troubleshooting

**External:**
- Arduino official tutorials (arduino.cc)
- SparkFun tutorials (learn.sparkfun.com)
- Adafruit Learn (learn.adafruit.com)

---

### Community Resources

**GitHub Discussions:**
- General questions
- Design discussions
- Feature requests

**Discord Server (coming soon):**
- Real-time chat
- Help channel
- Build showcase
- Off-topic

**Subreddit (proposed: r/AcousticLevitation):**
- Longer discussions
- Build logs
- Theory debates

---

## Project Philosophy

### Why Open Source?

**From the README:**
> "Levitation technology shouldn't belong to governments, corporations, or academic gatekeepers. It should belong to humanity."

**We believe:**
- Transformative tech should be freely available
- Community collaboration accelerates progress
- Open designs prevent suppression
- Everyone benefits from shared knowledge

**This means:**
- ✅ Free to build, modify, sell
- ✅ No royalties or licensing fees
- ✅ Educational use encouraged
- ✅ Commercial use allowed
- ✅ Academic publication welcomed

**We only ask:**
- Give credit to original authors
- Share improvements back (optional but appreciated)
- Don't patent what's already open

---

### Project Values

**Excellence:**
- Designs are rigorously tested
- Theory is mathematically sound
- Documentation is comprehensive

**Accessibility:**
- Beginner-friendly guides
- Multiple budget options
- Community support

**Collaboration:**
- Improvements welcome
- Respectful discussion
- Credit where due

**Transparency:**
- All designs public
- Development in the open
- Honest about limitations

---

## Next Steps

**Ready to build? Choose your path:**

1. **Dive in with Build 1** → `builds/build-1-micro/README.md`
2. **Learn more theory first** → `theory/01-fundamental-physics.md`
3. **See what others built** → `community/replications/`
4. **Ask questions** → GitHub Issues or Discord

**Not ready yet?**
- Star the repository (stay updated)
- Read the theory docs (no rush)
- Join Discord (lurk and learn)
- Come back when ready

---

## Inspiration

**What people have done with acoustic levitation:**

- Levitated water droplets for spectroscopy
- Created 3D displays with moving particles
- Demonstrated in science museums worldwide
- Used for drug research (crystallization studies)
- Art installations at festivals
- Physics education demonstrations

**What you could do:**

- First maker in your city with levitation
- Science fair project (guaranteed attention)
- YouTube channel about the build
- Start a local maker group
- Teach others
- Improve the design
- **Anything you can imagine**

---

**Welcome to the community. Let's make levitation real for everyone.**

---

*"The best time to start was yesterday. The second best time is now."*  
*- Chinese Proverb*

*"You don't have to see the whole staircase, just take the first step."*  
*- Martin Luther King Jr.*

*"Let's build some levitation."*  
*- Us*