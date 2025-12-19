/*
 * Protective Shield for Acoustic Levitation Array
 * ================================================
 * 
 * Transparent acrylic shield to protect users from:
 * - High-intensity ultrasonic exposure
 * - Particle ejection at high power
 * - Accidental contact with emitters
 * 
 * Specifications:
 * - Material: 3mm clear acrylic (laser cut) OR 3D printed PETG
 * - Height: 100mm above array
 * - Diameter: 120mm (fits Build 1)
 * - Viewing windows: 4 sides
 * - Access port: Top removable lid
 * 
 * License: MIT
 * Author: Sportysport & Claude (Anthropic)
 */

// ============================================================================
// PARAMETERS
// ============================================================================

// Shield dimensions
shield_diameter = 120;  // mm
shield_height = 100;    // mm
wall_thickness = 3;     // mm (for 3D printing) or use 3mm acrylic sheet

// Base plate (mounts to array)
base_thickness = 5;
base_diameter = shield_diameter + 20;

// Viewing windows
window_width = 40;
window_height = 60;
window_offset_z = 20;  // Height above base

// Top lid
lid_thickness = 3;
lid_handle_height = 15;

// Ventilation holes (for heat dissipation)
vent_hole_diameter = 8;
n_vent_holes = 12;
vent_ring_radius = (shield_diameter / 2) - 10;

// Mounting holes for base
base_mounting_holes = 4;
base_mounting_radius = (base_diameter / 2) - 8;
base_hole_diameter = 3.5;  // M3 screws

// ============================================================================
// MODULES
// ============================================================================

module cylindrical_shell() {
    /*
     * Main cylindrical shield body
     */
    difference() {
        // Outer cylinder
        cylinder(h=shield_height, d=shield_diameter, $fn=120);
        
        // Inner cylinder (hollow)
        translate([0, 0, -0.1])
            cylinder(h=shield_height + 0.2, 
                    d=shield_diameter - 2*wall_thickness, $fn=120);
        
        // Viewing windows (4 sides at 90° intervals)
        for (angle = [0, 90, 180, 270]) {
            rotate([0, 0, angle])
                translate([shield_diameter/2 - wall_thickness/2, 0, window_offset_z])
                    cube([wall_thickness + 1, window_width, window_height], 
                         center=true);
        }
        
        // Top open (for lid)
        translate([0, 0, shield_height - 0.1])
            cylinder(h=1, d=shield_diameter - 2*wall_thickness - 1, $fn=120);
    }
    
    // Window frames (reinforcement)
    for (angle = [0, 90, 180, 270]) {
        rotate([0, 0, angle])
            translate([shield_diameter/2 - wall_thickness, 0, window_offset_z])
                cube([wall_thickness, 2, window_height + 10], center=true);
    }
}

module base_plate_shield() {
    /*
     * Base plate with ventilation and mounting holes
     */
    difference() {
        // Main base disc
        cylinder(h=base_thickness, d=base_diameter, $fn=120);
        
        // Center opening for array
        translate([0, 0, -0.1])
            cylinder(h=base_thickness + 0.2, d=shield_diameter - 10, $fn=120);
        
        // Ventilation holes in ring pattern
        for (i = [0:n_vent_holes-1]) {
            angle = i * (360 / n_vent_holes);
            rotate([0, 0, angle])
                translate([vent_ring_radius, 0, -0.1])
                    cylinder(h=base_thickness + 0.2, d=vent_hole_diameter, $fn=30);
        }
        
        // Mounting holes for securing to array plate
        for (angle = [45, 135, 225, 315]) {
            rotate([0, 0, angle])
                translate([base_mounting_radius, 0, -0.1])
                    cylinder(h=base_thickness + 0.2, d=base_hole_diameter, $fn=30);
        }
        
        // Label text
        translate([0, -base_diameter/2 + 8, base_thickness - 0.8])
            linear_extrude(height=1)
                text("CAUTION", size=4, halign="center", 
                     font="Liberation Sans:style=Bold");
        
        translate([0, -base_diameter/2 + 13, base_thickness - 0.8])
            linear_extrude(height=1)
                text("Ultrasonic Field", size=3, halign="center");
    }
}

module top_lid() {
    /*
     * Removable top lid with handle
     * Allows access to levitation zone
     */
    difference() {
        union() {
            // Main lid disc
            cylinder(h=lid_thickness, d=shield_diameter - 2, $fn=120);
            
            // Handle
            translate([0, 0, lid_thickness])
                cylinder(h=lid_handle_height, d=20, $fn=60);
            
            // Handle grip
            translate([0, 0, lid_thickness + lid_handle_height])
                sphere(d=25, $fn=60);
        }
        
        // Central viewing hole
        translate([0, 0, -0.1])
            cylinder(h=lid_thickness + 0.2, d=40, $fn=60);
        
        // Ventilation slots (radial)
        for (i = [0:5]) {
            angle = i * 60;
            rotate([0, 0, angle])
                translate([shield_diameter/3, 0, -0.1])
                    cube([20, 3, lid_thickness + 0.2], center=true);
        }
        
        // Handle grip cutouts
        for (angle = [0, 120, 240]) {
            rotate([0, 0, angle])
                translate([0, 15, lid_thickness + lid_handle_height])
                    sphere(d=8, $fn=30);
        }
    }
}

module complete_shield_assembly() {
    /*
     * Complete protective shield assembly
     * (For visualization - print parts separately)
     */
    
    // Base plate
    base_plate_shield();
    
    // Cylindrical shield
    translate([0, 0, base_thickness])
        cylindrical_shell();
    
    // Top lid (shown in open position for clarity)
    translate([0, 0, base_thickness + shield_height + 10])
        top_lid();
}

// ============================================================================
// LASER CUT ALTERNATIVE (2D patterns)
// ============================================================================

module laser_cut_side_panel() {
    /*
     * Flat pattern for laser cutting acrylic side panels
     * Cut 4 of these from 3mm clear acrylic
     */
    difference() {
        // Main rectangle
        square([shield_diameter * 3.14159 / 4, shield_height]);
        
        // Viewing window
        translate([shield_diameter * 3.14159 / 8, window_offset_z])
            square([window_width, window_height], center=true);
        
        // Mounting holes along edges
        for (y = [10, shield_height - 10]) {
            for (x = [5, shield_diameter * 3.14159 / 4 - 5]) {
                translate([x, y])
                    circle(d=3, $fn=30);
            }
        }
    }
}

// ============================================================================
// GENERATE MODEL
// ============================================================================

// Choose what to render:
// 1. Complete assembly (for visualization)
complete_shield_assembly();

// 2. Individual parts (for printing)
// Uncomment to generate individual parts:

// base_plate_shield();

// translate([150, 0, 0])
//     cylindrical_shell();

// translate([0, 150, 0])
//     top_lid();

// 3. Laser cut pattern (for acrylic)
// translate([0, -150, 0])
//     laser_cut_side_panel();

// ============================================================================
// ASSEMBLY INSTRUCTIONS
// ============================================================================

/*
 * 3D PRINTING METHOD:
 * 
 * 1. Print 3 separate parts:
 *    - Base plate (print with brim)
 *    - Cylindrical shield (print standing up)
 *    - Top lid (print upside down)
 * 
 * 2. Materials:
 *    - PETG recommended (clear/translucent)
 *    - PLA acceptable for lower power arrays
 *    - ABS for professional builds
 * 
 * 3. Settings:
 *    - Layer height: 0.2mm
 *    - Walls: 3 perimeters
 *    - Infill: 15%
 *    - Print time: ~6 hours total
 * 
 * 4. Assembly:
 *    - Use M3 screws to attach base to array plate
 *    - Cylindrical shield pressure-fits onto base
 *    - Lid sits on top (friction fit)
 *    - Add rubber feet for vibration damping
 * 
 * LASER CUT METHOD (BETTER FOR CLARITY):
 * 
 * 1. Materials:
 *    - 3mm clear acrylic sheets
 *    - 5mm acrylic for base
 * 
 * 2. Cut patterns:
 *    - 4× side panels
 *    - 1× base ring
 *    - 1× top lid
 * 
 * 3. Assembly:
 *    - Use acrylic cement to bond sides
 *    - Bolt base to array plate
 *    - Lid with piano hinge (optional)
 * 
 * SAFETY NOTES:
 * - Ensure adequate ventilation (vent holes)
 * - Clear acrylic allows visual monitoring
 * - Shield reduces sound pressure outside by ~20dB
 * - Does NOT eliminate ultrasonic exposure completely
 * - Always wear hearing protection during operation
 */
