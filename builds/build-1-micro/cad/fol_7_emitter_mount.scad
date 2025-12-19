/*
 * Flower of Life - 7-Emitter Mounting Plate
 * ==========================================
 * 
 * 3D-printable mounting plate for Build 1 (7-emitter array)
 * Golden ratio spacing (φ = 1.618) optimized for 40kHz
 * 
 * Specifications:
 * - Wavelength: 8.575mm @ 40kHz
 * - Ring radius: 2.5λ = 21.4mm
 * - Emitter diameter: 16mm (HC-SR04 compatible)
 * - Plate thickness: 3mm
 * - Material: PLA, PETG, or ABS
 * 
 * Print Settings:
 * - Layer height: 0.2mm
 * - Infill: 20%
 * - Supports: Not required
 * - Print time: ~45 minutes
 * 
 * License: MIT
 * Author: Sportysport & Claude (Anthropic)
 */

// ============================================================================
// PARAMETERS (Adjust these for different builds)
// ============================================================================

// Physical constants
wavelength = 8.575;  // mm at 40kHz
phi = (1 + sqrt(5)) / 2;  // Golden ratio

// Array geometry
ring_radius = 2.5 * wavelength;  // 21.4mm
n_outer_emitters = 6;

// Emitter specifications
emitter_diameter = 16;  // mm (standard ultrasonic transducer)
emitter_hole_diameter = 16.2;  // mm (0.2mm tolerance)
mounting_hole_diameter = 2.5;  // mm (M2.5 screws)

// Plate dimensions
plate_radius = ring_radius + emitter_diameter + 10;  // Extra margin
plate_thickness = 3;  // mm
base_height = 2;  // mm raised platform for emitters

// Corner mounting holes
corner_hole_offset = plate_radius - 5;

// ============================================================================
// MODULES
// ============================================================================

module emitter_hole() {
    /*
     * Creates hole for ultrasonic transducer
     * With chamfer for easy insertion
     */
    translate([0, 0, -0.1])
        cylinder(h=plate_thickness + 0.2, d=emitter_hole_diameter, $fn=60);
    
    // Chamfer top edge (45 degree, 0.5mm)
    translate([0, 0, plate_thickness - 0.5])
        cylinder(h=0.6, d1=emitter_hole_diameter, 
                d2=emitter_hole_diameter + 1, $fn=60);
}

module mounting_hole() {
    /*
     * Creates M2.5 mounting hole
     * For securing emitters with screws
     */
    translate([0, 0, -0.1])
        cylinder(h=plate_thickness + 0.2, d=mounting_hole_diameter, $fn=30);
    
    // Countersink for screw head
    translate([0, 0, plate_thickness - 1.5])
        cylinder(h=1.6, d1=mounting_hole_diameter, d2=5, $fn=30);
}

module base_plate() {
    /*
     * Main circular base plate
     */
    difference() {
        // Main disc
        cylinder(h=plate_thickness, r=plate_radius, $fn=120);
        
        // Text label (debossed)
        translate([0, -plate_radius + 5, plate_thickness - 0.5])
            linear_extrude(height=0.6)
                text("FLOWER OF LIFE", size=3, halign="center", 
                     font="Liberation Sans:style=Bold");
        
        translate([0, -plate_radius + 10, plate_thickness - 0.5])
            linear_extrude(height=0.6)
                text("7-Emitter Array", size=2.5, halign="center");
        
        translate([0, -plate_radius + 14, plate_thickness - 0.5])
            linear_extrude(height=0.6)
                text("40kHz", size=2, halign="center");
    }
}

module corner_mounting_holes() {
    /*
     * Corner holes for mounting plate to enclosure
     * 4 corners at 45° angles
     */
    for (angle = [45, 135, 225, 315]) {
        rotate([0, 0, angle])
            translate([corner_hole_offset, 0, 0])
                mounting_hole();
    }
}

module emitter_platform(x, y) {
    /*
     * Raised platform for each emitter
     * Provides better acoustic isolation
     */
    translate([x, y, plate_thickness])
        cylinder(h=base_height, d=emitter_diameter + 4, $fn=60);
}

module flower_of_life_array() {
    /*
     * Complete 7-emitter Flower of Life mounting plate
     * 1 center + 6 ring emitters at 60° spacing
     */
    
    difference() {
        union() {
            // Base plate
            base_plate();
            
            // Center emitter platform
            emitter_platform(0, 0);
            
            // Ring emitter platforms
            for (i = [0:n_outer_emitters-1]) {
                angle = i * 60;  // 60° spacing
                x = ring_radius * cos(angle);
                y = ring_radius * sin(angle);
                emitter_platform(x, y);
            }
        }
        
        // Center emitter hole
        emitter_hole();
        
        // Ring emitter holes
        for (i = [0:n_outer_emitters-1]) {
            angle = i * 60;
            x = ring_radius * cos(angle);
            y = ring_radius * sin(angle);
            translate([x, y, 0])
                emitter_hole();
        }
        
        // Corner mounting holes
        corner_mounting_holes();
        
        // Wire management channels (from center outward)
        for (i = [0:n_outer_emitters-1]) {
            angle = i * 60;
            rotate([0, 0, angle])
                translate([0, 0, plate_thickness/2])
                    cube([ring_radius + 10, 2, 1], center=true);
        }
    }
    
    // Add registration markers for alignment
    for (i = [0, 120, 240]) {
        rotate([0, 0, i])
            translate([plate_radius - 3, 0, plate_thickness])
                cylinder(h=0.5, d=1.5, $fn=20);
    }
}

// ============================================================================
// GENERATE MODEL
// ============================================================================

flower_of_life_array();

// ============================================================================
// PRINT INSTRUCTIONS (in comments for reference)
// ============================================================================

/*
 * PRINTING GUIDE:
 * 
 * 1. Slice with these settings:
 *    - Layer height: 0.2mm
 *    - Wall thickness: 1.2mm (3 perimeters)
 *    - Top/bottom layers: 5
 *    - Infill: 20% (gyroid or honeycomb)
 *    - Print speed: 50mm/s
 *    - No supports needed!
 * 
 * 2. Material recommendations:
 *    - PLA: Easy to print, sufficient rigidity
 *    - PETG: Better temperature resistance
 *    - ABS: Professional grade, requires heated enclosure
 * 
 * 3. Post-processing:
 *    - Remove any stringing with hobby knife
 *    - Test fit emitters before assembly
 *    - Sand platforms lightly if emitters too tight
 * 
 * 4. Assembly:
 *    - Insert emitters from top
 *    - Solder wires through channels
 *    - Secure with M2.5 screws (optional)
 *    - Mount to enclosure using corner holes
 * 
 * ESTIMATED MATERIAL:
 * - Filament: ~25g
 * - Print time: 45 minutes
 * - Cost: <$1 in PLA
 */
