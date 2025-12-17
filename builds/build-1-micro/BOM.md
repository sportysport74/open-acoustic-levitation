# Build 1: Complete Bill of Materials

**Last Updated:** December 2024  
**Total Estimated Cost:** $80-100 USD

---

## Where to Buy

**Option A: AliExpress/Banggood (Cheapest, 30-day shipping)**
- Best for: Patient builders, minimum budget
- Total cost: ~$60 (but add $15 shipping)

**Option B: Amazon (Fast, 2-day shipping)**
- Best for: Want to start immediately
- Total cost: ~$90

**Option C: DigiKey/Mouser (Professional, next-day)**
- Best for: Need quality components fast
- Total cost: ~$120

**We'll provide links for all three options.**

---

## Electronics Components

### Microcontroller

| Part | Specs | Qty | Price (Ali) | Price (Amazon) | Price (DigiKey) |
|------|-------|-----|-------------|----------------|-----------------|
| **Arduino Nano clone** | ATmega328P, USB | 1 | $3 | $12 | $25 |

**Links:**
- AliExpress: Search "Arduino Nano CH340"
- Amazon: Search "Elegoo Nano V3"
- DigiKey: Real Arduino Nano (A000005)

**Notes:** Clone works fine for this project. If you have Arduino Uno, use that instead (code is compatible).

---

### Ultrasonic Emitters

| Part | Specs | Qty | Price (Ali) | Price (Amazon) | Price (DigiKey) |
|------|-------|-----|-------------|----------------|-----------------|
| **40kHz Piezo Buzzer** | 16mm, 40kHz±1kHz | 7 | $0.80 ea | $2 ea | $3 ea |

**Specific part numbers:**
- Murata MA40S4S (transmitter) - Best quality
- Generic 16mm 40kHz buzzer - Budget option

**Links:**
- AliExpress: Search "40khz ultrasonic sensor transmitter" (get 10-pack for $8)
- Amazon: Search "40kHz ultrasonic transducer"
- DigiKey: MA40S4S-ND

**IMPORTANT:** Get transmitters (marked with "T"), not receivers (marked with "R")

---

### Amplifiers

| Part | Specs | Qty | Price (Ali) | Price (Amazon) | Price (DigiKey) |
|------|-------|-----|-------------|----------------|-----------------|
| **PAM8403 Amplifier Module** | 2×3W, Class D | 4 | $1 ea | $2 ea | N/A |

**Why 4 amplifiers for 7 buzzers?**
- Each amp has 2 channels
- 4 amps = 8 channels (7 used, 1 spare)

**Links:**
- AliExpress: Search "PAM8403 amplifier module" (often sold in 5-packs for $5)
- Amazon: Search "PAM8403 mini amplifier"

**Alternative:** Single TPA3116D2 board (2×50W, $12) - overkill but works

---

### Power Supply

| Part | Specs | Qty | Price |
|------|-------|-----|-------|
| **12V DC Power Adapter** | 12V 2A (24W) | 1 | $8-12 |

**Options:**
- Old laptop charger (if 12V)
- Wall adapter (Amazon: "12V 2A power supply")
- Bench power supply (if you have one)

**Connector:** 5.5mm×2.1mm barrel jack (standard)

---

### Wiring & Connectors

| Part | Qty | Price | Where |
|------|-----|-------|-------|
| **Jumper wires** (M-M, M-F) | 40 pcs | $5 | Amazon "dupont jumper wires" |
| **22 AWG stranded wire** | 5 meters | $5 | Local hardware store or Amazon |
| **Breadboard** (400 tie-points) | 1 | $3 | Amazon/AliExpress |
| **DC barrel jack** (female) | 1 | $2 | Amazon "dc power jack" |
| **USB cable** (for Arduino) | 1 | Free | (use phone charger cable) |

---

### Optional: Sensors (Not Required for Basic Build)

| Part | Specs | Qty | Price |
|------|-------|-----|-------|
| **40kHz Ultrasonic Receiver** | MA40S4R or equiv | 2 | $1.50 ea |
| **Electret microphone** | Small MEMS | 1 | $2 |

**Use for:** Acoustic field measurement, frequency calibration

---

## Mechanical Components

### Base Platform

**Option A: Cardboard (Free)**
- Thickness: 3-5mm
- Source: Cereal box, Amazon box
- Cut to 25cm diameter circle

**Option B: Plywood (Best)**
- Thickness: 6mm (1/4")
- Size: 30cm × 30cm square
- Cost: $3-5 at hardware store
- Cut to 25cm diameter (or leave square)

**Option C: 3D Printed (If you have printer)**
- Material: PLA or PETG
- Thickness: 5mm
- Cost: ~$2 in filament
- Files: See `cad/base_platform.stl`

---

### Mounting Hardware

| Part | Qty | Price | Notes |
|------|-----|-------|-------|
| **Hot glue sticks** | 10 | $3 | For mounting buzzers |
| **Double-sided foam tape** | 1 roll | $4 | Alternative to hot glue |
| **Zip ties** (small) | 10 | $2 | Cable management |

---

### Reflector Plate

| Part | Specs | Qty | Price |
|------|-------|-----|-------|
| **Aluminum foil** | Kitchen grade | 1 sheet | Free |
| **Cardboard disk** | 8cm diameter | 1 | Free |

**Purpose:** Reflects acoustic waves, mounted to test object

**Assembly:** Glue foil smoothly to cardboard disk

---

### Test Objects

| Object | Weight | Where to Get | Cost |
|--------|--------|--------------|------|
| **Ping pong ball** | 2.7g | Dollar store, Amazon | $1 |
| **Foam ball** (50mm) | 5-10g | Craft store | $1 |
| **Styrofoam sphere** | 3-8g | Craft store | $2 |

**Prepare test object:**
1. Attach reflector plate to bottom with glue
2. Ensure flat, smooth surface facing down
3. Keep assembly light (<15g total for first tests)

---

## Tools Required

### Essential (Must Have)

| Tool | Purpose | Cost if Buying |
|------|---------|----------------|
| **Soldering iron** | Wire connections | $15-30 |
| **Solder** (60/40 or lead-free) | Electrical connections | $5 |
| **Wire strippers** | Stripping wire | $8 |
| **Scissors or knife** | Cutting materials | $5 |
| **Ruler or calipers** | Measuring positions | $3-15 |
| **Hot glue gun** | Mounting components | $8 |

**Total tool cost if buying all:** ~$50

**But:** Most people have some of these, borrow the rest

---

### Nice to Have (Optional)

| Tool | Purpose | Cost |
|------|---------|------|
| **Multimeter** | Testing voltage/continuity | $15 |
| **Oscilloscope** | Verifying 40kHz signal | $50+ |
| **Helping hands** | Holding parts while soldering | $10 |
| **Drill + bits** | Clean mounting holes (if using wood) | $30 |

---

## Consumables

| Item | Qty | Price |
|------|-----|-------|
| **Electrical tape** | 1 roll | $2 |
| **Heat shrink tubing** | Small pack | $5 |
| **Flux pen** | 1 | $3 |
| **Desoldering wick** | 1 | $3 |
| **Isopropyl alcohol** | For cleaning | $3 |
| **Paper towels** | Cleaning | $1 |

---

## Complete Shopping Lists

### AliExpress Shopping Cart (~$60 + shipping)
```
[ ] Arduino Nano clone (1×) - $3
[ ] 40kHz buzzers 10-pack - $8
[ ] PAM8403 amplifier 5-pack - $5
[ ] Jumper wires 120pcs - $3
[ ] 22AWG wire 10m - $4
[ ] Breadboard - $2
[ ] DC barrel jacks 5-pack - $2
[ ] Hot glue sticks 20pcs - $2
[ ] Zip ties 100pcs - $2

Subtotal: $31
Shipping: $15-20
Total: ~$46-51

Add if needed:
[ ] Soldering iron kit - $15
[ ] Wire strippers - $5
[ ] Multimeter - $10
```

**Shipping time:** 20-40 days (be patient!)

---

### Amazon Shopping Cart (~$90, 2-day shipping)
```
[ ] Elegoo Nano V3 (3-pack) - $18 ($6 each, extras for future projects)
[ ] 40kHz ultrasonic sensors (10-pack) - $12
[ ] PAM8403 amplifier (5-pack) - $10
[ ] Dupont jumper wires (120pcs) - $7
[ ] 22AWG hookup wire kit - $10
[ ] Breadboard (3-pack) - $8
[ ] 12V 2A power supply - $9
[ ] Hot glue gun with 30 sticks - $10
[ ] Zip tie assortment - $6

Subtotal: $90

Optional adds:
[ ] Soldering iron kit (Tabiger 60W) - $22
[ ] AstroAI Multimeter - $16
[ ] Wire stripper/cutter - $10
```

**Shipping:** Free with Prime, arrives in 2 days

---

### DigiKey Shopping Cart (~$120, next-day)

**For those who want quality and have budget:**
```
[ ] Arduino Nano (A000005) - $25
[ ] Murata MA40S4S (7×) - $21
[ ] MA40S4R receivers (2×) - $6 (optional)
[ ] Assorted 22AWG wire - $12
[ ] Breadboard - $5
[ ] Jumper wires - $8
[ ] Various connectors - $10

Subtotal: $87

Add power supply from Amazon - $9
Add mechanical parts from hardware store - $15

Total: ~$110-120
```

**Shipping:** $8 next-day, free over $100

---

## Budget Breakdown

| Category | Minimum | Recommended | Premium |
|----------|---------|-------------|---------|
| **Electronics** | $30 | $50 | $90 |
| **Mechanical** | $10 | $20 | $30 |
| **Tools** (if buying) | $25 | $50 | $100 |
| **Consumables** | $10 | $15 | $20 |
| **Shipping** | $0 | $10 | $10 |
| **TOTAL** | **$75** | **$145** | **$250** |

**Realistic for most people:** $90-120 (electronics + shipping, already have tools)

---

## Money-Saving Tips

1. **Check what you already have**
   - Old Arduino from past project?
   - Wall wart power supplies in drawer?
   - Soldering iron from electronics kit?

2. **Group buy with friends**
   - Split 10-pack of buzzers (only need 7)
   - Share amplifier 5-packs
   - One person orders, divide cost

3. **Scavenge parts**
   - Old computer speakers → amplifier
   - Cardboard from packages → base platform
   - Wire from old electronics

4. **Start with minimum**
   - Skip sensors for first build
   - Use cardboard instead of wood
   - Basic soldering iron works fine

5. **Buy tools once**
   - Soldering iron lasts years
   - Wire strippers useful for future projects
   - Consider it investment in hobby

---

## What to Buy First

**If budget is tight, buy in stages:**

**Stage 1 ($40):** Order electronics from AliExpress
- Arduino Nano
- Buzzers
- Amplifiers
- Wire

**Stage 2 (while waiting for shipping):** Get tools
- Borrow or buy soldering iron
- Scavenge cardboard/foil
- Get test objects (ping pong ball)

**Stage 3 ($10):** Power supply
- Buy 12V adapter locally once parts arrive
- Or use bench supply if you have one

---

## Receiving Your Parts

**When AliExpress package arrives:**

1. **Inventory check**
   - Count everything
   - Compare to order
   - Report missing items immediately

2. **Visual inspection**
   - Look for shipping damage
   - Check solder joints on modules
   - Verify buzzers look identical

3. **Basic testing**
   - Plug in Arduino, LED should light
   - Test amplifiers with audio input
   - Check power supply voltage with multimeter

4. **Organize**
   - Label bags: "Buzzers", "Amps", etc.
   - Keep in plastic storage bin
   - Don't lose tiny pieces!

---

## Questions?

- **Part substitutions:** Check troubleshooting guide
- **Can't find exact part:** Post in GitHub issues
- **Local sourcing:** Check electronics stores (RadioShack, Fry's, Micro Center)
- **International:** Adjust links for your country

---

**Ready to order? Proceed to [assembly-guide.md](assembly-guide.md) while you wait for parts!**

---

*Pro tip: Order parts NOW, read assembly guide while waiting. You'll hit the ground running when package arrives.*