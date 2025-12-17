/*
 * TEST ALL EMITTERS SIMULTANEOUSLY
 * 
 * Generates 40kHz on all pins at once
 * All in phase (no phase offsets)
 * Use to verify overall system before levitation
 */

const int EMITTER_PINS[7] = {3, 5, 6, 9, 10, 11, 13};

void setup() {
  Serial.begin(115200);
  Serial.println(F("ALL EMITTERS TEST"));
  Serial.println(F("Generating 40kHz on all 7 emitters"));
  Serial.println(F("All in phase (no offsets)"));
  Serial.println();
  
  for (int i = 0; i < 7; i++) {
    pinMode(EMITTER_PINS[i], OUTPUT);
    digitalWrite(EMITTER_PINS[i], LOW);
  }
  
  Serial.println(F("Starting in 2 seconds..."));
  delay(2000);
  Serial.println(F("ACTIVE - Press reset to stop"));
}

void loop() {
  // Set all HIGH
  for (int i = 0; i < 7; i++) {
    digitalWrite(EMITTER_PINS[i], HIGH);
  }
  delayMicroseconds(12);
  
  // Set all LOW
  for (int i = 0; i < 7; i++) {
    digitalWrite(EMITTER_PINS[i], LOW);
  }
  delayMicroseconds(12);
  
  // Status update every 10 seconds
  static unsigned long lastStatus = 0;
  if (millis() - lastStatus > 10000) {
    Serial.print(F("Running... "));
    Serial.print(millis() / 1000);
    Serial.println(F("s"));
    lastStatus = millis();
  }
}