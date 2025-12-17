/*
 * OPEN ACOUSTIC LEVITATION PROJECT - BUILD 1
 * Basic Levitation System
 * 
 * Authors: Sportysport & Claude (Anthropic)
 * License: MIT
 * 
 * Hardware:
 * - Arduino Nano
 * - 7× 40kHz ultrasonic buzzers (MA40S4S or similar)
 * - 4× PAM8403 amplifiers
 * - 12V power supply
 * 
 * Generates 40kHz carrier frequency with 80kHz parametric modulation
 * Phase-shifted outputs for Flower of Life geometry
 * 
 * No sensors required - open-loop control
 */

// ============================================================================
// CONFIGURATION
// ============================================================================

// Emitter pins (must be PWM-capable)
const int EMITTER_PINS[7] = {3, 5, 6, 9, 10, 11, 13};

// Frequencies
const unsigned long CARRIER_FREQ = 40000;      // 40 kHz carrier
const unsigned long PARAM_FREQ = 80000;        // 80 kHz (2× carrier)

// Parametric modulation depth (0.0 to 0.3)
// Start conservative, increase if needed
const float EPSILON = 0.10;  // 10% modulation

// Phase offsets for Flower of Life geometry (radians)
// E0: center (0°), E1-E6: ring at 60° intervals
const float PHASE_OFFSETS[7] = {
  0.0,           // E0: center
  0.0,           // E1: 0° (reference)
  1.047,         // E2: 60° (π/3)
  2.094,         // E3: 120° (2π/3)
  3.142,         // E4: 180° (π)
  4.189,         // E5: 240° (4π/3)
  5.236          // E6: 300° (5π/3)
};

// ============================================================================
// GLOBALS
// ============================================================================

// Pre-calculated constants
const float TWO_PI = 6.283185307;
const float CARRIER_PERIOD_US = 1000000.0 / CARRIER_FREQ;  // 25 microseconds
const float PARAM_PERIOD_US = 1000000.0 / PARAM_FREQ;      // 12.5 microseconds

// ============================================================================
// SETUP
// ============================================================================

void setup() {
  // Initialize serial for debugging
  Serial.begin(115200);
  Serial.println(F("=================================="));
  Serial.println(F("ACOUSTIC LEVITATION - BUILD 1"));
  Serial.println(F("Open Source Hardware Project"));
  Serial.println(F("=================================="));
  Serial.println();
  
  // Print configuration
  Serial.print(F("Carrier frequency: "));
  Serial.print(CARRIER_FREQ);
  Serial.println(F(" Hz"));
  
  Serial.print(F("Parametric frequency: "));
  Serial.print(PARAM_FREQ);
  Serial.println(F(" Hz"));
  
  Serial.print(F("Modulation depth (epsilon): "));
  Serial.println(EPSILON);
  Serial.println();
  
  // Initialize all emitter pins as outputs
  for (int i = 0; i < 7; i++) {
    pinMode(EMITTER_PINS[i], OUTPUT);
    digitalWrite(EMITTER_PINS[i], LOW);
  }
  
  Serial.println(F("All emitters initialized"));
  Serial.println(F("Starting levitation in 3 seconds..."));
  delay(3000);
  
  Serial.println(F("LEVITATION ACTIVE"));
  Serial.println(F("Press Ctrl+C to stop"));
  Serial.println();
}

// ============================================================================
// MAIN LOOP
// ============================================================================

void loop() {
  // Get current time in microseconds
  unsigned long t = micros();
  
  // Calculate parametric envelope
  // envelope = 1 + ε*sin(2πf_param*t)
  float param_phase = TWO_PI * (t % (unsigned long)PARAM_PERIOD_US) / PARAM_PERIOD_US;
  float envelope = 1.0 + EPSILON * sin(param_phase);
  
  // Calculate carrier phase (time within one period)
  float carrier_phase = TWO_PI * (t % (unsigned long)CARRIER_PERIOD_US) / CARRIER_PERIOD_US;
  
  // Generate signals for all emitters
  for (int i = 0; i < 7; i++) {
    // Add emitter-specific phase offset
    float total_phase = carrier_phase + PHASE_OFFSETS[i];
    
    // Normalize phase to [0, 2π]
    while (total_phase > TWO_PI) total_phase -= TWO_PI;
    
    // Apply parametric modulation
    float signal = envelope * sin(total_phase);
    
    // Convert to digital output (square wave approximation)
    // Positive half of sine → HIGH, negative half → LOW
    digitalWrite(EMITTER_PINS[i], signal > 0 ? HIGH : LOW);
  }
  
  // Status update every 10 seconds
  static unsigned long lastStatus = 0;
  if (millis() - lastStatus > 10000) {
    Serial.print(F("Running... uptime: "));
    Serial.print(millis() / 1000);
    Serial.println(F(" seconds"));
    lastStatus = millis();
  }
}