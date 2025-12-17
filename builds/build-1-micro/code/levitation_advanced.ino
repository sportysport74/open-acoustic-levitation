/*
 * ADVANCED LEVITATION SYSTEM
 * 
 * Adds features:
 * - Adjustable parameters via Serial commands
 * - Performance monitoring
 * - Automatic frequency optimization (if sensors added later)
 * 
 * Serial commands:
 * - 'f40000' - Set carrier frequency to 40000 Hz
 * - 'e0.10' - Set epsilon to 0.10
 * - 's' - Print status
 * - 'r' - Reset to defaults
 */

// ============================================================================
// CONFIGURATION
// ============================================================================

const int EMITTER_PINS[7] = {3, 5, 6, 9, 10, 11, 13};

// Default parameters (can be changed via serial)
unsigned long carrierFreq = 40000;
float epsilon = 0.10;

const float PHASE_OFFSETS[7] = {
  0.0, 0.0, 1.047, 2.094, 3.142, 4.189, 5.236
};

const float TWO_PI = 6.283185307;

// ============================================================================
// SETUP
// ============================================================================

void setup() {
  Serial.begin(115200);
  printHeader();
  
  for (int i = 0; i < 7; i++) {
    pinMode(EMITTER_PINS[i], OUTPUT);
    digitalWrite(EMITTER_PINS[i], LOW);
  }
  
  Serial.println(F("Ready. Type 's' for status, 'h' for help"));
  delay(2000);
  Serial.println(F("Levitation active"));
}

// ============================================================================
// MAIN LOOP
// ============================================================================

void loop() {
  // Handle serial commands
  if (Serial.available() > 0) {
    handleSerialCommand();
  }
  
  // Generate levitation signals
  generateSignals();
  
  // Status updates
  static unsigned long lastStatus = 0;
  if (millis() - lastStatus > 30000) {  // Every 30 seconds
    printQuickStatus();
    lastStatus = millis();
  }
}

// ============================================================================
// SIGNAL GENERATION
// ============================================================================

void generateSignals() {
  unsigned long t = micros();
  
  // Calculate periods
  float carrierPeriod = 1000000.0 / carrierFreq;
  float paramPeriod = 1000000.0 / (2 * carrierFreq);
  
  // Parametric envelope
  float paramPhase = TWO_PI * fmod(t, paramPeriod) / paramPeriod;
  float envelope = 1.0 + epsilon * sin(paramPhase);
  
  // Carrier phase
  float carrierPhase = TWO_PI * fmod(t, carrierPeriod) / carrierPeriod;
  
  // Generate for all emitters
  for (int i = 0; i < 7; i++) {
    float totalPhase = carrierPhase + PHASE_OFFSETS[i];
    while (totalPhase > TWO_PI) totalPhase -= TWO_PI;
    
    float signal = envelope * sin(totalPhase);
    digitalWrite(EMITTER_PINS[i], signal > 0 ? HIGH : LOW);
  }
}

// ============================================================================
// SERIAL COMMAND HANDLING
// ============================================================================

void handleSerialCommand() {
  String command = Serial.readStringUntil('\n');
  command.trim();
  command.toLowerCase();
  
  if (command.length() == 0) return;
  
  char cmd = command.charAt(0);
  
  switch(cmd) {
    case 'h':  // Help
      printHelp();
      break;
      
    case 's':  // Status
      printStatus();
      break;
      
    case 'f':  // Set frequency
      if (command.length() > 1) {
        unsigned long newFreq = command.substring(1).toInt();
        if (newFreq >= 20000 && newFreq <= 60000) {
          carrierFreq = newFreq;
          Serial.print(F("Carrier frequency set to: "));
          Serial.print(carrierFreq);
          Serial.println(F(" Hz"));
        } else {
          Serial.println(F("Error: Frequency must be 20000-60000 Hz"));
        }
      }
      break;
      
    case 'e':  // Set epsilon
      if (command.length() > 1) {
        float newEpsilon = command.substring(1).toFloat();
        if (newEpsilon >= 0.0 && newEpsilon <= 0.3) {
          epsilon = newEpsilon;
          Serial.print(F("Epsilon set to: "));
          Serial.println(epsilon, 3);
        } else {
          Serial.println(F("Error: Epsilon must be 0.0-0.3"));
        }
      }
      break;
      
    case 'r':  // Reset to defaults
      carrierFreq = 40000;
      epsilon = 0.10;
      Serial.println(F("Reset to defaults"));
      printStatus();
      break;
      
    default:
      Serial.print(F("Unknown command: "));
      Serial.println(command);
      Serial.println(F("Type 'h' for help"));
  }
}

// ============================================================================
// DISPLAY FUNCTIONS
// ============================================================================

void printHeader() {
  Serial.println(F("=================================="));
  Serial.println(F("ADVANCED LEVITATION SYSTEM"));
  Serial.println(F("Build 1 - Open Source Hardware"));
  Serial.println(F("=================================="));
  Serial.println();
}

void printHelp() {
  Serial.println();
  Serial.println(F("COMMANDS:"));
  Serial.println(F("  h        - Show this help"));
  Serial.println(F("  s        - Print detailed status"));
  Serial.println(F("  f<freq>  - Set carrier frequency (Hz)"));
  Serial.println(F("             Example: f40000"));
  Serial.println(F("  e<val>   - Set epsilon (modulation depth)"));
  Serial.println(F("             Example: e0.15"));
  Serial.println(F("  r        - Reset to default parameters"));
  Serial.println();
}

void printStatus() {
  Serial.println();
  Serial.println(F("=== CURRENT STATUS ==="));
  Serial.print(F("Carrier frequency: "));
  Serial.print(carrierFreq);
  Serial.println(F(" Hz"));
  
  Serial.print(F("Parametric frequency: "));
  Serial.print(carrierFreq * 2);
  Serial.println(F(" Hz"));
  
  Serial.print(F("Epsilon (modulation): "));
  Serial.println(epsilon, 3);
  
  Serial.print(F("Wavelength: "));
  Serial.print(343000.0 / carrierFreq, 2);
  Serial.println(F(" mm"));
  
  Serial.print(F("Uptime: "));
  Serial.print(millis() / 1000);
  Serial.println(F(" seconds"));
  
  Serial.println(F("====================="));
  Serial.println();
}

void printQuickStatus() {
  Serial.print(F("["));
  Serial.print(millis() / 1000);
  Serial.print(F("s] f="));
  Serial.print(carrierFreq);
  Serial.print(F("Hz, ε="));
  Serial.println(epsilon, 2);
}