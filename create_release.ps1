# Release Package Builder
# Creates v0.1 release with all simulation outputs for non-Python users

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 68) -ForegroundColor Cyan
Write-Host "RELEASE PACKAGE BUILDER v0.1" -ForegroundColor Yellow
Write-Host ("=" * 70) -ForegroundColor Cyan
Write-Host ""

$releaseDir = "release-v0.1"
$timestamp = Get-Date -Format "yyyy-MM-dd"

# Create release directory
New-Item -ItemType Directory -Path $releaseDir -Force | Out-Null
Write-Host "[✓] Created release directory: $releaseDir" -ForegroundColor Green

# Create subdirectories
$dirs = @(
    "$releaseDir/simulations",
    "$releaseDir/simulations/static-images",
    "$releaseDir/simulations/animations",
    "$releaseDir/hardware",
    "$releaseDir/documentation"
)

foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
}
Write-Host "[✓] Created subdirectories" -ForegroundColor Green

# Copy simulation results
Write-Host "`nCopying simulation outputs..." -ForegroundColor Yellow

# Static PNGs
$pngFiles = Get-ChildItem -Path "simulations/results" -Filter "*.png" -ErrorAction SilentlyContinue
foreach ($file in $pngFiles) {
    Copy-Item $file.FullName -Destination "$releaseDir/simulations/static-images/" -Force
    Write-Host "  [✓] $($file.Name)" -ForegroundColor Green
}

# Animated GIFs
$gifFiles = Get-ChildItem -Path "simulations/results" -Filter "*.gif" -ErrorAction SilentlyContinue
foreach ($file in $gifFiles) {
    Copy-Item $file.FullName -Destination "$releaseDir/simulations/animations/" -Force
    Write-Host "  [✓] $($file.Name)" -ForegroundColor Green
}

# Copy hardware BOMs
Write-Host "`nCopying hardware files..." -ForegroundColor Yellow
Copy-Item "builds/build-1-micro/BOM.csv" -Destination "$releaseDir/hardware/" -Force -ErrorAction SilentlyContinue
Copy-Item "builds/build-1-micro/BOM.md" -Destination "$releaseDir/hardware/" -Force -ErrorAction SilentlyContinue
Write-Host "  [✓] Bill of Materials" -ForegroundColor Green

# Copy documentation
Write-Host "`nCopying documentation..." -ForegroundColor Yellow
Copy-Item "README.md" -Destination "$releaseDir/documentation/" -Force
Copy-Item "docs/safety.md" -Destination "$releaseDir/documentation/" -Force -ErrorAction SilentlyContinue
Copy-Item "docs/faq.md" -Destination "$releaseDir/documentation/" -Force -ErrorAction SilentlyContinue
Copy-Item "LICENSE" -Destination "$releaseDir/" -Force
Write-Host "  [✓] Documentation files" -ForegroundColor Green

# Create README for release package
$releaseReadme = @"
# Open Acoustic Levitation - Release v0.1
**Release Date:** $timestamp

## 📦 What's Included

This release package contains all simulation outputs and documentation for the Open Acoustic Levitation project. **No Python installation required** to view the results!

### 📊 Simulation Results

**Static Images** (simulations/static-images/)
- gor_kov_comparison.png - Force field comparison
- line_profiles.png - 1D potential profiles
- potential_heatmaps.png - 2D heatmaps
- fol_detailed_analysis.png - 4-panel comprehensive analysis
- heatmap_enhanced_with_forces.png - Force vector overlays
- force_magnitude_comparison.png - Force field strength
- particle_trajectories_3d.png - 3D particle paths
- particle_trajectories_topview.png - Top-down trajectory view
- trajectory_convergence_analysis.png - Convergence over time
- 19_emitter_comparison.png - Multi-ring array comparison
- scaling_analysis.png - Scaling efficiency charts
- multiple_trap_points.png - 18 simultaneous traps mapped

**Animations** (simulations/animations/)
- fol_animation_solo.gif - Single Flower of Life animation
- particle_animation_comparison.gif - Side-by-side comparison

### 🛠️ Hardware

**Bills of Materials** (hardware/)
- BOM.csv - Spreadsheet with 3 sourcing options
- BOM.md - Markdown formatted BOM

### 📚 Documentation

**Guides** (documentation/)
- README.md - Complete project overview
- safety.md - Safety guidelines
- faq.md - Frequently asked questions
- LICENSE - MIT License

## 🔬 Key Results

**7-Emitter Array (Build 1):**
- 35% stronger peak forces vs alternatives
- Single primary trap point
- Cost: \$66-\$222

**19-Emitter Array (Build 2):**
- 18 simultaneous trap points
- 29% more traps than square grid
- Cost: \$180-\$520

**Performance Metrics:**
- Convergence time: 300ms (FoL) vs 500ms+ (random)
- Capture rate: 75% (FoL) vs 25% (random)
- Force advantage: 3755 μN/mm (FoL) vs 2780 (square)

## 🚀 Next Steps

### To View Results
1. Open any PNG file in image viewer
2. Open GIF files to see animations
3. Read documentation/ for full details

### To Run Simulations Yourself
1. Visit: https://github.com/sportysport74/open-acoustic-levitation
2. Clone repository
3. Install Python + dependencies
4. Run simulation scripts

### To Build Hardware
1. Review hardware/BOM files
2. Read documentation/safety.md (IMPORTANT!)
3. Order components
4. Follow assembly guides in GitHub repository

## 📄 License

MIT License - Free to use, modify, and share

## 🙏 Credits

**Theory & Simulation:** Sportysport & Claude (Anthropic)
**Community:** All contributors and supporters

## 📞 Support

- **GitHub:** https://github.com/sportysport74/open-acoustic-levitation
- **Issues:** Report bugs via GitHub Issues
- **Discussions:** Ask questions in GitHub Discussions

---

**⭐ If you find this useful, star the repository on GitHub!**

Made with ❤️ for open science and democratized technology
"@

Set-Content -Path "$releaseDir/README.txt" -Value $releaseReadme
Write-Host "`n[✓] Created release README" -ForegroundColor Green

# Create file manifest
$manifest = @"
# Release v0.1 File Manifest
Generated: $timestamp

## Directory Structure
"@

Get-ChildItem -Path $releaseDir -Recurse | ForEach-Object {
    $relativePath = $_.FullName.Replace((Get-Location).Path + "\$releaseDir\", "")
    $manifest += "`n  $relativePath"
}

Set-Content -Path "$releaseDir/MANIFEST.txt" -Value $manifest
Write-Host "[✓] Created file manifest" -ForegroundColor Green

# Compress to ZIP
Write-Host "`nCreating release archive..." -ForegroundColor Yellow
$zipFile = "open-acoustic-levitation-v0.1-$timestamp.zip"

if (Test-Path $zipFile) {
    Remove-Item $zipFile -Force
}

Compress-Archive -Path "$releaseDir/*" -DestinationPath $zipFile -CompressionLevel Optimal
Write-Host "[✓] Created: $zipFile" -ForegroundColor Green

# Get file size
$zipSize = (Get-Item $zipFile).Length / 1MB
Write-Host "  Size: $($zipSize.ToString('F2')) MB" -ForegroundColor Cyan

# Summary
Write-Host "`n" -NoNewline
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 68) -ForegroundColor Cyan
Write-Host "RELEASE PACKAGE COMPLETE!" -ForegroundColor Green
Write-Host ("=" * 70) -ForegroundColor Cyan
Write-Host "`nCreated files:" -ForegroundColor Yellow
Write-Host "  1. $zipFile (upload to GitHub Releases)" -ForegroundColor White
Write-Host "  2. $releaseDir/ (temporary staging directory)" -ForegroundColor White
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "  1. Go to: https://github.com/sportysport74/open-acoustic-levitation/releases" -ForegroundColor White
Write-Host "  2. Click 'Draft a new release'" -ForegroundColor White
Write-Host "  3. Tag: v0.1" -ForegroundColor White
Write-Host "  4. Title: 'v0.1 - First Public Release'" -ForegroundColor White
Write-Host "  5. Upload: $zipFile" -ForegroundColor White
Write-Host "  6. Publish release" -ForegroundColor White
Write-Host "`nCleanup:" -ForegroundColor Yellow
Write-Host "  Remove-Item -Recurse -Force $releaseDir" -ForegroundColor Gray
Write-Host ("=" * 70) -ForegroundColor Cyan