/*
 * Flower of Life - 19-Emitter Mounting Plate (Build 2)
 * ======================================================
 * 
 * 3D-printable mounting plate for Build 2 (19-emitter lab array)
 * Multi-ring Flower of Life: 1 center + 6 inner + 12 outer
 * 
 * Specifications:
 * - Wavelength: 8.575mm @ 40kHz
 * - Inner ring: 2.5λ = 21.4mm radius
 * - Outer ring: 5.0λ = 42.9mm radius
 * - Emitter diameter: 16mm (HC-SR04 compatible)
 * - Plate thickness: 4mm (thicker for rigidity)
 * - Material: PETG or ABS recommended (PLA acceptable)
 * 
 * Print Settings:
 * - Layer height: 0.2mm
 * - Infill: 30% (higher for vibration damping)
 * - Supports: Not required
 * - Print time: ~3 hours
 * - Material: ~80g filament
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

// Array geometry - Multi-ring Flower of Life
inner_ring_radius = 2.5 * wavelength;  // 21.4mm (6 emitters)
outer_ring_radius = 5.0 * wavelength;  // 42.9mm (12 emitters)
n_inner_emitters = 6;
n_outer_emitters = 12;

// Emitter specifications
emitter_diameter = 16;  // mm (standard ultrasonic transducer)
emitter_hole_diameter = 16.2;  // mm (0.2mm tolerance)
mounting_screw_diameter = 2.5;  // mm (M2.5 screws for emitters)

// Plate dimensions
plate_radius = outer_ring_radius + emitter_diameter + 15;  // Extra margin
plate_thickness = 4;  // mm (thicker for 19 emitters)
base_height = 2;  // mm raised platform for emitters

// Structural reinforcement
reinforcement_thickness = 3;
reinforcement_width = 4;

// Corner mounting holes (for enclosure)
corner_hole_offset = plate_radius - 6;
corner_hole_diameter = 4;  // M4 screws

// Cable management
cable_channel_width = 3;
cable_channel_depth = 2;

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
    
    // Wire exit hole on bottom
    translate([0, 0, -0.1])
        cylinder(h=1.5, d=6, $fn=30);
}

module mounting_screw_hole() {
    /*
     * Creates M2.5 mounting hole for securing emitters
     */
    translate([0, 0, -0.1])
        cylinder(h=plate_thickness + 0.2, d=mounting_screw_diameter, $fn=30);
    
    // Countersink for screw head
    translate([0, 0, plate_thickness - 1.5])
        cylinder(h=1.6, d1=mounting_screw_diameter, d2=5.5, $fn=30);
}

module base_plate() {
    /*
     * Main circular base plate with structural ribs
     */
    difference() {
        union() {
            // Main disc
            cylinder(h=plate_thickness, r=plate_radius, $fn=180);
            
            // Structural ribs (radial from center to outer ring)
            for (angle = [0:30:330]) {
                rotate([0, 0, angle])
                    translate([0, -reinforcement_width/2, 0])
                        cube([outer_ring_radius + 10, reinforcement_width, 
                             plate_thickness + 1]);
            }
        }
        
        // Text label (debossed)
        translate([0, -plate_radius + 6, plate_thickness - 0.6])
            linear_extrude(height=0.7)
                text("FLOWER OF LIFE", size=4, halign="center", 
                     font="Liberation Sans:style=Bold");
        
        translate([0, -plate_radius + 11, plate_thickness - 0.6])
            linear_extrude(height=0.7)
                text("19-Emitter Array - Build 2", size=3, halign="center");
        
        translate([0, -plate_radius + 15.5, plate_thickness - 0.6])
            linear_extrude(height=0.7)
                text("40kHz Lab Grade", size=2.5, halign="center");
        
        // Ring labels
        translate([inner_ring_radius + 2, 0, plate_thickness - 0.5])
            rotate([0, 0, 0])
                linear_extrude(height=0.6)
                    text("R1", size=2, halign="center");
        
        translate([outer_ring_radius + 2, 0, plate_thickness - 0.5])
            rotate([0, 0, 0])
                linear_extrude(height=0.6)
                    text("R2", size=2, halign="center");
    }
}

module corner_mounting_holes() {
    /*
     * Corner holes for mounting plate to enclosure
     * 6 corners at 60° angles (hexagonal pattern)
     */
    for (angle = [0, 60, 120, 180, 240, 300]) {
        rotate([0, 0, angle])
            translate([corner_hole_offset, 0, -0.1])
                cylinder(h=plate_thickness + 0.2, d=corner_hole_diameter, $fn=40);
    }
}

module emitter_platform(x, y, label) {
    /*
     * Raised platform for each emitter
     * Provides better acoustic isolation and numbering
     */
    difference() {
        translate([x, y, plate_thickness])
            cylinder(h=base_height, d=emitter_diameter + 5, $fn=60);
        
        // Emitter number label
        translate([x, y, plate_thickness + base_height - 0.4])
            linear_extrude(height=0.5)
                text(str(label), size=2.5, halign="center", valign="center",
                     font="Liberation Sans:style=Bold");
    }
}

module cable_channels() {
    /*
     * Cable management channels running from emitters to edge
     * Inner ring channels
     */
    for (i = [0:n_inner_emitters-1]) {
        angle = i * 60;
        rotate([0, 0, angle]) {
            translate([0, 0, plate_thickness - cable_channel_depth])
                linear_extrude(height=cable_channel_depth + 0.1)
                    polygon([
                        [0, -cable_channel_width/2],
                        [0, cable_channel_width/2],
                        [plate_radius, cable_channel_width/2],
                        [plate_radius, -cable_channel_width/2]
                    ]);
        }
    }
    
    // Outer ring channels (offset 30° from inner)
    for (i = [0:n_outer_emitters-1]) {
        angle = i * 30;
        rotate([0, 0, angle]) {
            translate([0, 0, plate_thickness - cable_channel_depth])
                linear_extrude(height=cable_channel_depth + 0.1)
                    polygon([
                        [0, -cable_channel_width/2],
                        [0, cable_channel_width/2],
                        [plate_radius, cable_channel_width/2],
                        [plate_radius, -cable_channel_width/2]
                    ]);
        }
    }
}

module registration_marks() {
    /*
     * Alignment marks for assembly verification
     * Shows correct 0°, 60°, 120° orientations
     */
    for (angle = [0, 60, 120]) {
        rotate([0, 0, angle])
            translate([plate_radius - 4, 0, plate_thickness])
                cylinder(h=1, d=2, $fn=20);
    }
}

module flower_of_life_19_emitter() {
    /*
     * Complete 19-emitter Flower of Life mounting plate
     * 1 center + 6 inner ring + 12 outer ring
     */
    
    difference() {
        union() {
            // Base plate with ribs
            base_plate();
            
            // Center emitter platform
            emitter_platform(0, 0, "C");
            
            // Inner ring emitter platforms (6 at 60° intervals)
            for (i = [0:n_inner_emitters-1]) {
                angle = i * 60;
                x = inner_ring_radius * cos(angle);
                y = inner_ring_radius * sin(angle);
                emitter_platform(x, y, str(i+1));
            }
            
            // Outer ring emitter platforms (12 at 30° intervals)
            for (i = [0:n_outer_emitters-1]) {
                angle = i * 30;
                x = outer_ring_radius * cos(angle);
                y = outer_ring_radius * sin(angle);
                emitter_platform(x, y, str(i+7));
            }
        }
        
        // Center emitter hole
        emitter_hole();
        
        // Inner ring emitter holes
        for (i = [0:n_inner_emitters-1]) {
            angle = i * 60;
            x = inner_ring_radius * cos(angle);
            y = inner_ring_radius * sin(angle);
            translate([x, y, 0])
                emitter_hole();
        }
        
        // Outer ring emitter holes
        for (i = [0:n_outer_emitters-1]) {
            angle = i * 30;
            x = outer_ring_radius * cos(angle);
            y = outer_ring_radius * sin(angle);
            translate([x, y, 0])
                emitter_hole();
        }
        
        // Corner mounting holes
        corner_mounting_holes();
        
        // Cable management channels
        cable_channels();
    }
    
    // Registration marks
    registration_marks();
}

// ============================================================================
// GENERATE MODEL
// ============================================================================

flower_of_life_19_emitter();

// ============================================================================
// ASSEMBLY NOTES
// ============================================================================

/*
 * PRINT INSTRUCTIONS:
 * 
 * Slicer Settings:
 * - Layer height: 0.2mm
 * - Wall thickness: 1.6mm (4 perimeters)
 * - Top/bottom layers: 6
 * - Infill: 30% (gyroid for vibration damping)
 * - Print speed: 40mm/s (slower for accuracy)
 * - Enable "Detect thin walls"
 * - Brim: 8mm (prevents warping)
 * 
 * Material Selection:
 * - PETG: Best choice (temp resistant, strong)
 * - ABS: Professional grade (requires enclosure)
 * - PLA: Acceptable but may warp under heat
 * 
 * Print Time: ~3 hours
 * Material: ~80g filament (~$2 in PETG)
 * 
 * POST-PROCESSING:
 * - Remove brim carefully
 * - Test-fit one emitter before installing all
 * - Sand platforms lightly if emitters too tight
 * - Clean out cable channels with pick/brush
 * 
 * ASSEMBLY SEQUENCE:
 * 1. Mount plate to enclosure using M4 corner screws
 * 2. Install center emitter first (labeled "C")
 * 3. Install inner ring (labeled 1-6) at 60° intervals
 * 4. Install outer ring (labeled 7-18) at 30° intervals
 * 5. Route wires through channels to edge
 * 6. Connect to driver board (see wiring diagram)
 * 7. Verify phase alignment with oscilloscope
 * 
 * EMITTER NUMBERING:
 * - C: Center (0°)
 * - 1-6: Inner ring (0°, 60°, 120°, 180°, 240°, 300°)
 * - 7-18: Outer ring (0°, 30°, 60°, ... 330°)
 * 
 * VERIFICATION:
 * - All emitters should be flush with platforms
 * - Registration marks should align at 0°, 60°, 120°
 * - Cable channels should allow wires to lay flat
 * - No wobble when mounted to enclosure
 * 
 * TROUBLESHOOTING:
 * - Emitters too tight: Sand platforms with 220 grit
 * - Emitters too loose: Use 0.1mm shim or adhesive
 * - Warped plate: Increase bed adhesion, reduce speed
 * - Cracked ribs: Increase wall thickness to 2mm
 */
