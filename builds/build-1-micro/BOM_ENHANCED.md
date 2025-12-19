# Build 1 - Enhanced Bill of Materials (BOM)

**Last Updated:** December 19, 2025  
**Array Type:** 7-Emitter Flower of Life (Micro Array)  
**Budget:** $66 (Budget) | $144 (Standard) | $222 (Premium)

---

## 🛒 Quick Purchase Links

**ONE-CLICK SHOPPING:**

### Budget Build ($66 Total)
- [AliExpress Complete Kit](https://www.aliexpress.com/wholesale?SearchText=HC-SR04+ultrasonic+40khz) - All transducers
- [Amazon Arduino Starter Kit](https://www.amazon.com/s?k=arduino+nano+clone) - Includes Arduino + wires + breadboard

### Standard Build ($144 Total)
- [DigiKey Transducers](https://www.digikey.com/en/products/filter/ultrasonic-receivers-transmitters/158) - Quality components
- [Arduino Official Store](https://store.arduino.cc/products/arduino-nano) - Genuine Arduino

### Premium Build ($222 Total)
- [Mouser Professional Components](https://www.mouser.com/c/sensors/audio-sound-speakers-transducers/) - Industrial grade
- Custom PCB from [JLCPCB](https://jlcpcb.com/) or [PCBWay](https://www.pcbway.com/)

---

## 📋 Detailed Component List

### Core Components

| # | Part | Qty | Budget | Standard | Premium | Links |
|---|------|-----|--------|----------|---------|-------|
| 1 | **Ultrasonic Transducers** (40kHz, 16mm) | 7 | $14 | $35 | $70 | [AliExpress](https://www.aliexpress.com/wholesale?SearchText=40khz+ultrasonic+transducer+16mm) \| [DigiKey](https://www.digikey.com/en/products/detail/murata-electronics/MA40S4S/4358146) \| [Mouser](https://www.mouser.com/ProductDetail/Murata/MA40S4S) |
| 2 | **Microcontroller** (Arduino Nano compatible) | 1 | $3 | $25 | $25 | [AliExpress](https://www.aliexpress.com/wholesale?SearchText=arduino+nano+ch340) \| [Arduino Official](https://store.arduino.cc/products/arduino-nano) \| [Arduino Official](https://store.arduino.cc/products/arduino-nano) |
| 3 | **N-Channel MOSFETs** (IRLZ44N or similar) | 7 | $7 | $14 | $21 | [AliExpress](https://www.aliexpress.com/wholesale?SearchText=IRLZ44N) \| [DigiKey IRLZ44N](https://www.digikey.com/en/products/detail/infineon-technologies/IRLZ44NPBF/811756) \| [Mouser IRLB8721](https://www.mouser.com/ProductDetail/Infineon/IRLB8721PBF) |
| 4 | **Pull-down Resistors** (10kΩ, 1/4W) | 7 | $1 | $2 | $3 | [AliExpress](https://www.aliexpress.com/wholesale?SearchText=10k+resistor+pack) \| [DigiKey](https://www.digikey.com/en/products/detail/yageo/CFR-25JB-52-10K/338) \| [Mouser](https://www.mouser.com/ProductDetail/Vishay-Dale/CMF5510K000FHEB) |
| 5 | **Power Supply** (12V 2A DC) | 1 | $8 | $15 | $25 | [AliExpress](https://www.aliexpress.com/wholesale?SearchText=12v+2a+power+supply) \| [Amazon](https://www.amazon.com/s?k=12v+2a+power+adapter) \| [DigiKey](https://www.digikey.com/en/products/filter/ac-dc-desktop-wall-adapters/133) |

**Subtotal (Core):** $33 | $91 | $144

---

### Supporting Components

| # | Part | Qty | Budget | Standard | Premium | Links |
|---|------|-----|--------|----------|---------|-------|
| 6 | **Breadboard** (830 tie points) | 1 | $3 | $5 | N/A | [AliExpress](https://www.aliexpress.com/wholesale?SearchText=breadboard+830) \| [Amazon](https://www.amazon.com/s?k=solderless+breadboard) \| PCB instead |
| 7 | **Jumper Wires** (M-M, 22 AWG) | 1 pack | $2 | $4 | N/A | [AliExpress](https://www.aliexpress.com/wholesale?SearchText=dupont+jumper+wire) \| [Amazon](https://www.amazon.com/s?k=breadboard+jumper+wires) | PCB instead |
| 8 | **USB Cable** (Mini-B for Arduino) | 1 | $2 | $3 | $5 | [AliExpress](https://www.aliexpress.com/wholesale?SearchText=usb+mini+b+cable) \| [Amazon](https://www.amazon.com/s?k=mini+usb+cable) \| [Anker Quality](https://www.amazon.com/s?k=anker+mini+usb) |
| 9 | **DC Barrel Jack** (5.5mm × 2.1mm) | 1 | $1 | $2 | $3 | [AliExpress](https://www.aliexpress.com/wholesale?SearchText=dc+barrel+jack+screw) \| [DigiKey](https://www.digikey.com/en/products/filter/barrel-power-connectors/435) \| [Mouser](https://www.mouser.com/c/connectors/barrel-power-connectors/) |
| 10 | **Fuse Holder** + 2A Fuse | 1 | $2 | $3 | $5 | [AliExpress](https://www.aliexpress.com/wholesale?SearchText=inline+fuse+holder) \| [Amazon](https://www.amazon.com/s?k=inline+fuse+holder+2a) \| [DigiKey](https://www.digikey.com/en/products/filter/fuse-holders/157) |

**Subtotal (Supporting):** $10 | $17 | $13

---

### Optional Enhancements

| # | Part | Qty | Budget | Standard | Premium | Purpose |
|---|------|-----|--------|----------|---------|---------|
| 11 | **Heatsinks** (TO-220 package) | 7 | $3 | $5 | $10 | MOSFET cooling | [AliExpress](https://www.aliexpress.com/wholesale?SearchText=TO220+heatsink) \| [Amazon](https://www.amazon.com/s?k=to220+heatsink) \| [DigiKey](https://www.digikey.com/en/products/filter/thermal-heat-sinks/219) |
| 12 | **Cooling Fan** (40mm, 12V) | 1 | $3 | $5 | $8 | Active cooling | [AliExpress](https://www.aliexpress.com/wholesale?SearchText=40mm+12v+fan) \| [Amazon](https://www.amazon.com/s?k=40mm+12v+fan) \| [Noctua](https://www.amazon.com/s?k=noctua+40mm) |
| 13 | **Oscilloscope** (USB logic analyzer) | 1 | $8 | $25 | $150 | Phase verification | [AliExpress](https://www.aliexpress.com/wholesale?SearchText=24mhz+logic+analyzer) \| [Amazon Saleae Clone](https://www.amazon.com/s?k=8ch+logic+analyzer) \| [Saleae Official](https://www.saleae.com/) |
| 14 | **3D Printed Mounting Plate** | 1 | $2 | $5 | $15 | From CAD files | Local makerspace | Print service | Professional service |
| 15 | **Acrylic Safety Shield** | 1 | $5 | $10 | $20 | Protective enclosure | [Local hardware store](https://www.homedepot.com/s/acrylic%20sheet) | [TAP Plastics](https://www.tapplastics.com/) | Laser-cut service |
| 16 | **Snubber Diodes** (1N4007) | 7 | $1 | $2 | $3 | EMI suppression | [AliExpress](https://www.aliexpress.com/wholesale?SearchText=1N4007+diode) \| [DigiKey](https://www.digikey.com/en/products/detail/onsemi/1N4007/458603) \| [Mouser](https://www.mouser.com/ProductDetail/onsemi/1N4007G) |
| 17 | **Capacitors** (0.1μF ceramic) | 7 | $1 | $2 | $3 | Noise filtering | [AliExpress](https://www.aliexpress.com/wholesale?SearchText=0.1uf+ceramic+capacitor) \| [DigiKey](https://www.digikey.com/en/products/filter/ceramic-capacitors/60) \| [Mouser](https://www.mouser.com/c/passive-components/capacitors/ceramic-capacitors/) |

**Subtotal (Optional):** $23 | $54 | $209

---

## 💰 Total Cost Summary

| Build Level | Core | Supporting | Optional | **TOTAL** |
|-------------|------|------------|----------|-----------|
| **Budget** | $33 | $10 | $23 | **$66** |
| **Standard** | $91 | $17 | $36 | **$144** |
| **Premium** | $144 | $13 | $65 | **$222** |

---

## 🔧 Tools Required (Not Included in BOM)

### Minimal Toolset ($20-$50)
- Soldering iron + solder
- Wire strippers
- Small Phillips screwdriver
- Multimeter (basic)
- USB cable (Mini-B for Arduino)

**Links:**
- [Budget Soldering Kit](https://www.amazon.com/s?k=soldering+iron+kit+beginners) - $15-20
- [Basic Multimeter](https://www.amazon.com/s?k=digital+multimeter) - $10-15

### Recommended Toolset ($100-$200)
- Temperature-controlled soldering station
- Helping hands/PCB holder
- Wire strippers (precision)
- Digital multimeter (autoranging)
- Logic analyzer or oscilloscope

**Links:**
- [Hakko FX888D](https://www.amazon.com/s?k=hakko+fx888d) - $100 (best value)
- [Fluke Multimeter](https://www.amazon.com/s?k=fluke+117) - $150

---

## 📦 Recommended Suppliers by Region

### North America
- **Fast shipping:** [Amazon](https://www.amazon.com/) (2-day Prime)
- **Quality components:** [DigiKey](https://www.digikey.com/), [Mouser](https://www.mouser.com/)
- **Budget friendly:** [AliExpress](https://www.aliexpress.com/) (2-4 weeks)

### Europe
- **Fast shipping:** [RS Components](https://uk.rs-online.com/), [Farnell](https://www.farnell.com/)
- **Quality components:** [DigiKey EU](https://www.digikey.com/)
- **Budget friendly:** [AliExpress](https://www.aliexpress.com/)

### Asia-Pacific
- **Fast shipping:** [Taobao](https://www.taobao.com/) (China), [RS Components](https://sg.rs-online.com/)
- **Quality components:** [DigiKey](https://www.digikey.com/), local distributors
- **Budget friendly:** Local electronics markets

---

## 🎯 What to Buy First (Shopping List Priority)

### Phase 1: Get Started ($50)
1. Arduino Nano (or clone)
2. 7× Ultrasonic transducers (40kHz)
3. Breadboard + jumper wires
4. 12V 2A power supply
5. USB cable

**You can start coding and testing individual emitters!**

### Phase 2: Complete Array ($20)
1. 7× MOSFETs (IRLZ44N)
2. 7× 10kΩ resistors
3. DC barrel jack
4. Fuse holder + fuse

**Now you can drive all 7 emitters and attempt levitation!**

### Phase 3: Professional Finish ($30-150)
1. 3D printed mounting plate
2. Heatsinks for MOSFETs
3. Snubber diodes + capacitors
4. Safety shield
5. (Optional) Oscilloscope for phase verification

**Polished, safe, reliable system!**

---

## 🛡️ Safety Equipment (REQUIRED)

| Item | Cost | Link | Why Needed |
|------|------|------|------------|
| Safety glasses | $5-10 | [Amazon](https://www.amazon.com/s?k=safety+glasses+ansi) | Particle ejection protection |
| Hearing protection | $10-20 | [Amazon](https://www.amazon.com/s?k=ear+protection) | Ultrasonic exposure limits |
| Multimeter | $10-50 | [Amazon](https://www.amazon.com/s?k=multimeter) | Voltage/continuity verification |

**DO NOT skip safety equipment!**

---

## 📝 Shopping Checklist

Print this and check off as you order:

**Core Components:**
- [ ] 7× Ultrasonic transducers (40kHz, 16mm)
- [ ] 1× Arduino Nano (or compatible)
- [ ] 7× N-Channel MOSFETs (IRLZ44N)
- [ ] 7× 10kΩ resistors (1/4W)
- [ ] 1× Power supply (12V 2A)

**Supporting:**
- [ ] Breadboard (830 tie points)
- [ ] Jumper wire pack
- [ ] USB cable (Mini-B)
- [ ] DC barrel jack
- [ ] Fuse holder + 2A fuse

**Optional Enhancements:**
- [ ] 7× Heatsinks (TO-220)
- [ ] 1× Cooling fan (40mm, 12V)
- [ ] 1× Logic analyzer / oscilloscope
- [ ] 3D printed mounting plate
- [ ] Acrylic safety shield
- [ ] 7× Snubber diodes (1N4007)
- [ ] 7× Ceramic capacitors (0.1μF)

**Tools & Safety:**
- [ ] Soldering iron + solder
- [ ] Wire strippers
- [ ] Screwdriver set
- [ ] Multimeter
- [ ] Safety glasses
- [ ] Hearing protection

---

## 💡 Pro Tips

**Save Money:**
- Buy transducers in bulk (10-pack cheaper per unit)
- Use breadboard first, only make PCB if satisfied
- Check local makerspaces for 3D printing
- Group orders with friends to share shipping

**Avoid Common Mistakes:**
- Don't mix 5V/12V power rails
- Don't skip the fuse (fire hazard!)
- Don't use AC adapters (DC only!)
- Don't forget pull-down resistors on MOSFETs

**Quality Matters Most For:**
- Transducers (cheap ones have inconsistent frequency)
- Power supply (ripple affects performance)
- Arduino (clones sometimes have USB issues)

**Can Cheap Out On:**
- Wire (as long as 22 AWG or thicker)
- Resistors (tolerance doesn't matter much here)
- Breadboard (all work the same)

---

## 🔗 Related Files

- **Wiring Diagram:** `/builds/build-1-micro/WIRING_DIAGRAM.md`
- **CAD Files:** `/builds/build-1-micro/cad/`
- **Firmware:** `/builds/build-1-micro/code/`
- **Assembly Guide:** `/builds/build-1-micro/assembly-guide.md`

---

**Questions about component selection?** Open an issue on GitHub!

---

*Last updated: December 19, 2025*  
*Prices are estimates and may vary by region/supplier*
