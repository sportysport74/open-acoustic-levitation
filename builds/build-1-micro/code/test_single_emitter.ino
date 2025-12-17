/*
 * TEST SINGLE EMITTER
 * 
 * Generates 40kHz square wave on one pin at a time
 * Use to verify each emitter is working
 */

const int EMITTER_PINS[7] = {3, 5, 6, 9, 10, 11, 13};
const char* EMITTER_NAMES[7] = {"E0 (center)", "E1 (0°)", "E2 (60°)", "E3 (120°)", "E4 (180°)", "E5 (240°)", "E6 (300°)"};

void setup() {
  Serial.begin(115200);
  Serial.println(F("EMITTER TEST PROGRAM"));
  Serial.println(F("Testing each emitter for 3 seconds"));
  Serial.println();
  
  for (int i = 0; i < 7; i++) {
    pinMode(EMITTER_PINS[i], OUTPUT);
    digitalWrite(EMITTER_PINS[i], LOW);
  }
}

void loop() {
  for (int emitter = 0; emitter < 7; emitter++) {
    Serial.print(F("Testing "));
    Serial.print(EMITTER_NAMES[emitter]);
    Serial.print(F(" on pin D"));
    Serial.println(EMITTER_PINS[emitter]);
    
    // Generate 40kHz for 3 seconds
    unsigned long startTime = millis();
    while (millis() - startTime < 3000) {
      digitalWrite(EMITTER_PINS[emitter], HIGH);
      delayMicroseconds(12);  // 12.5μs HIGH
      digitalWrite(EMITTER_PINS[emitter], LOW);
      delayMicroseconds(12);  // 12.5μs LOW
      // Total: 25μs = 40kHz
    }
    
    Serial.println(F("Done. Pausing 1 second..."));
    Serial.println();
    delay(1000);
  }
  
  Serial.println(F("All emitters tested. Restarting cycle..."));
  Serial.println();
  delay(2000);
}