# Contributing to Open Acoustic Levitation

🌸 **Thank you for your interest in contributing!** This project thrives on community participation, and we welcome contributions from physicists, engineers, makers, and enthusiasts of all skill levels.

---

## 🎯 Ways to Contribute

### 🛠️ Build & Share Your Array

**The #1 most valuable contribution: Build your own levitator and share your results!**

**What we're looking for:**
- 📸 **Build photos** - Assembly process, finished array, creative enclosures
- 🎬 **Levitation videos** - Particles floating, multiple traps, dynamic manipulation
- 📊 **Experimental data** - Force measurements, particle trajectories, stability tests
- 💡 **Design improvements** - Modifications that work better for specific use cases
- 🐛 **Troubleshooting tips** - Solutions to common problems you encountered

**How to share:**
1. Post in [GitHub Discussions](https://github.com/sportysport74/open-acoustic-levitation/discussions) with photos/videos
2. Open an Issue tagged `build-showcase`
3. Submit a Pull Request adding your build to `/community/builds/`
4. Tag `#OpenAcousticLevitation` on social media

**Community Hall of Fame:** Outstanding builds will be featured in README!

---

### 🔬 Scientific Contributions

**Validate, extend, or challenge the simulations**

**Research areas:**
- Experimental validation of simulation predictions
- Alternative geometry comparisons
- Parametric pumping implementations
- Multi-particle dynamics
- Acoustic streaming effects
- Non-spherical particle levitation

**How to contribute:**
1. Run simulations with different parameters
2. Document your methodology
3. Share results with analysis
4. Open a Pull Request with new simulation scripts

**Publishing:** If your contribution is substantial, we'll collaborate on academic papers!

---

### 💻 Code Contributions

**Improve simulations, add features, fix bugs**

**High-impact areas:**
- Interactive web visualizations (WebGL, Three.js)
- Real-time control software (Python GUI, LabVIEW)
- Machine learning for trap optimization
- CAD model improvements (FreeCAD, Fusion 360)
- Hardware firmware enhancements
- Documentation improvements

**Process:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with clear commit messages
4. Test thoroughly
5. Submit a Pull Request with description of changes

---

### 📐 Hardware Design Contributions

**Expand the hardware ecosystem**

**What we need:**
- **Build 2 CAD models** (19-emitter mounting plate)
- **Build 3 CAD models** (37-emitter professional array)
- **Alternative enclosures** (acrylic, aluminum, wood)
- **PCB designs** (custom driver boards)
- **Power supply designs** (switching regulators, amplifiers)
- **Sensor integration** (microphones, cameras, force sensors)

**Formats accepted:**
- OpenSCAD (.scad)
- FreeCAD (.fcstd)
- Fusion 360 (.f3d)
- STL for 3D printing (.stl)
- DXF for laser cutting (.dxf)
- KiCAD for PCBs (.kicad_pro)

**Submit via Pull Request to `/builds/` with:**
- CAD source files
- Exported STL/DXF files
- Assembly instructions
- Bill of materials
- Photos of assembled hardware (if available)

---

### 📚 Documentation Contributions

**Make the project more accessible**

**Documentation needs:**
- Tutorials for beginners
- Troubleshooting guides
- Theory explanations (simplified for non-physicists)
- Video walkthroughs
- Translations to other languages
- FAQ expansions

**Style guide:**
- Use clear, concise language
- Include visual aids (diagrams, photos)
- Provide examples and real-world context
- Link to relevant theory documents

---

### 🐛 Bug Reports & Feature Requests

**Help us improve**

**Reporting bugs:**
1. Check if issue already exists
2. Use descriptive title
3. Include:
   - Operating system
   - Python version
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages (full traceback)
   - Screenshots if relevant

**Requesting features:**
1. Describe use case clearly
2. Explain why it's valuable
3. Suggest implementation approach (optional)
4. Link to relevant papers/resources

**Use issue templates:** We provide templates for bugs and features

---

## 🎨 Community Guidelines

### Be Respectful & Inclusive

- Welcome contributors of all backgrounds and skill levels
- Use inclusive language
- Provide constructive feedback
- Celebrate successes together
- Help newcomers get started

### Scientific Integrity

- Cite sources properly
- Be honest about limitations
- Share negative results (failed experiments teach us!)
- Acknowledge uncertainty
- Don't make claims beyond what data supports

### Open Source Spirit

- Share knowledge freely
- Give credit generously
- Help others succeed
- Document your work
- Pay it forward

---

## 🚀 Getting Started

### First-Time Contributors

**Easy starter tasks:**
1. Fix typos in documentation
2. Add comments to code
3. Improve README formatting
4. Test installation instructions
5. Share your build photos

**Look for issues tagged:** `good-first-issue` or `help-wanted`

### Development Setup

```bash
# Clone repository
git clone https://github.com/sportysport74/open-acoustic-levitation.git
cd open-acoustic-levitation

# Install dependencies
pip install -r requirements.txt

# Run tests (if available)
python -m pytest

# Run simulations
cd simulations
python gor_kov_simulation.py
```

### Code Style

**Python:**
- PEP 8 style guide
- Descriptive variable names
- Docstrings for functions
- Type hints encouraged
- Comments for complex logic

**OpenSCAD:**
- Parametric designs
- Clear module names
- Comments explaining geometry
- Print instructions included

---

## 📝 Pull Request Process

1. **Update documentation** - If you change functionality, update relevant docs
2. **Test thoroughly** - Ensure code runs without errors
3. **One feature per PR** - Keep changes focused
4. **Descriptive title** - Clearly state what the PR does
5. **Explain changes** - Provide context in PR description
6. **Reference issues** - Link related issues (Closes #123)
7. **Be patient** - Reviews may take a few days

### PR Checklist

- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Changes tested locally
- [ ] Commit messages are clear
- [ ] No merge conflicts
- [ ] Screenshots included (for visual changes)

---

## 🏆 Recognition

### Ways We Thank Contributors

**All contributors:**
- Listed in Contributors section
- Mentioned in release notes
- Acknowledged in academic papers (if substantial)

**Outstanding contributions:**
- Featured in README showcase
- Invited to co-author publications
- Promoted on social media
- Recognized in documentation

**Build showcase winners:**
- Featured photo on main README
- Detailed writeup in `/community/builds/`
- Social media spotlight
- Priority support for future projects

---

## 📧 Communication Channels

**GitHub Discussions** (primary)
- Q&A
- Build showcases
- Feature discussions
- Community meetups

**GitHub Issues**
- Bug reports
- Feature requests
- Technical problems

**Social Media**
- Twitter/X: `#OpenAcousticLevitation`
- Reddit: r/AcousticLevitation
- Discord: (coming soon!)

---

## 🔒 Safety First

**All contributions must prioritize safety:**
- Include safety warnings where appropriate
- Don't encourage unsafe modifications
- Document potential hazards
- Provide protective equipment recommendations

**See [SAFETY.md](docs/safety.md) for full guidelines**

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

This means:
- Anyone can use your contribution freely
- You retain copyright to your work
- No warranty is implied
- Credit is given where due

---

## 🎓 Academic Collaboration

**Interested in publishing together?**

We're preparing manuscripts for submission to:
- Applied Physics Letters
- Journal of the Acoustical Society of America
- Scientific Reports

**Major contributors may be invited as co-authors.** Criteria:
- Substantial intellectual contribution
- Original research or analysis
- Experimental validation
- Novel theoretical insights

**Contact via GitHub Issues with tag:** `academic-collaboration`

---

## 🌟 Special Thanks

To everyone who has contributed so far - this project wouldn't exist without you!

**Top contributors will be listed here as the project grows.**

---

## 🎯 Current Priority Needs

**Updated: December 2025**

**Most wanted contributions right now:**
1. 🎬 **First levitation video!** - Be the first to capture real levitation
2. 📐 **Build 2 CAD models** - 19-emitter mounting plate design
3. 🔬 **Experimental validation** - Measure actual forces vs predictions
4. 💡 **Arduino firmware improvements** - Real-time frequency tuning
5. 🌐 **Interactive web demo** - Browser-based simulation
6. 📹 **Tutorial videos** - Assembly walkthroughs
7. 🔊 **Acoustic pressure measurements** - Validate SPL predictions
8. 📊 **Parametric pumping** - Implement time-varying modulation

**See [current issues](https://github.com/sportysport74/open-acoustic-levitation/issues) for more**

---

## ❓ Questions?

**Not sure where to start?**
- Read the [README](README.md) for project overview
- Check [FAQ](docs/faq.md) for common questions
- Browse [existing discussions](https://github.com/sportysport74/open-acoustic-levitation/discussions)
- Open an issue asking for guidance - we're friendly!

---

**🌸 Thank you for helping democratize acoustic levitation technology! Together, we're making breakthrough science accessible to everyone. 🌸**

---

*Last updated: December 19, 2025*