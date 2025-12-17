/*
 * FREQUENCY SWEEP
 * 
 * Sweeps carrier frequency from 38kHz to 42kHz
 * Hold test object at levitation height and find resonance
 * Optimal frequency is where levitation is strongest/most stable
 */

const int EMITTER_PINS[7] = {3, 5, 6, 9, 10, 11, 13};

// Sweep parameters
const unsigned long FREQ_START = 38000;   // 38 kHz
const unsigned long FREQ_END = 42000;     // 42 kHz
const unsigned long FREQ_STEP = 500;      // 500 Hz steps
const unsigned long DWELL_TIME = 5000;    // 5 seconds per frequency

unsigned long currentFreq = FREQ_START;

void setup() {
  Serial.begin(115200);
  Serial.println(F("FREQUENCY SWEEP CALIBRATION"));
  Serial.println(F("Sweeping 38kHz to 42kHz in 500Hz steps"));
  Serial.println(F("Hold test object at ~5mm height"));
  Serial.println(F("Note which frequency gives best levitation"));
  Serial.println();
  
  for (int i = 0; i < 7; i++) {
    pinMode(EMITTER_PINS[i], OUTPUT);
    digitalWrite(EMITTER_PINS[i], LOW);
  }
  
  delay(3000);
  Serial.println(F("Starting sweep..."));
  Serial.println();
}

void loop() {
  Serial.print(F("Testing frequency: "));
  Serial.print(currentFreq);
  Serial.print(F(" Hz ("));
  Serial.print((currentFreq - FREQ_START) * 100 / (FREQ_END - FREQ_START));
  Serial.println(F("% complete)"));
  
  // Generate this frequency for DWELL_TIME
  unsigned long startTime = millis();
  float halfPeriod = 500000.0 / currentFreq;  // microseconds
  
  while (millis() - startTime < DWELL_TIME) {
    // Set all HIGH
    for (int i = 0; i < 7; i++) {
      digitalWrite(EMITTER_PINS[i], HIGH);
    }
    delayMicroseconds((int)halfPeriod);
    
    // Set all LOW
    for (int i = 0; i < 7; i++) {
      digitalWrite(EMITTER_PINS[i], LOW);
    }
    delayMicroseconds((int)halfPeriod);
  }
  
  // Next frequency
  currentFreq += FREQ_STEP;
  
  if (currentFreq > FREQ_END) {
    Serial.println();
    Serial.println(F("Sweep complete!"));
    Serial.println(F("Restarting from beginning..."));
    Serial.println();
    currentFreq = FREQ_START;
    delay(3000);
  }
}