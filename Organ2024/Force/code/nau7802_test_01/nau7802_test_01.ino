#include <Adafruit_NAU7802.h>
#include <math.h>

Adafruit_NAU7802 nau;
const int button = D8;
const int led = D7;

void setup() {
  pinMode(button, INPUT_PULLUP);
  pinMode(led, OUTPUT);
  Serial.begin(115200);
  delay(1000);
  Serial.println("NAU7802");
  if (! nau.begin()) {
    Serial.println("Failed to find NAU7802");
    while (1) delay(10);  // Don't proceed.
  }
  Serial.println("Found NAU7802");

  nau.setLDO(NAU7802_3V0);
  Serial.print("LDO voltage set to ");
  switch (nau.getLDO()) {
    case NAU7802_4V5:  Serial.println("4.5V"); break;
    case NAU7802_4V2:  Serial.println("4.2V"); break;
    case NAU7802_3V9:  Serial.println("3.9V"); break;
    case NAU7802_3V6:  Serial.println("3.6V"); break;
    case NAU7802_3V3:  Serial.println("3.3V"); break;
    case NAU7802_3V0:  Serial.println("3.0V"); break;
    case NAU7802_2V7:  Serial.println("2.7V"); break;
    case NAU7802_2V4:  Serial.println("2.4V"); break;
    case NAU7802_EXTERNAL:  Serial.println("External"); break;
  }

  nau.setGain(NAU7802_GAIN_128);
  Serial.print("Gain set to ");
  switch (nau.getGain()) {
    case NAU7802_GAIN_1:  Serial.println("1x"); break;
    case NAU7802_GAIN_2:  Serial.println("2x"); break;
    case NAU7802_GAIN_4:  Serial.println("4x"); break;
    case NAU7802_GAIN_8:  Serial.println("8x"); break;
    case NAU7802_GAIN_16:  Serial.println("16x"); break;
    case NAU7802_GAIN_32:  Serial.println("32x"); break;
    case NAU7802_GAIN_64:  Serial.println("64x"); break;
    case NAU7802_GAIN_128:  Serial.println("128x"); break;
  }

  nau.setRate(NAU7802_RATE_10SPS);
  Serial.print("Conversion rate set to ");
  switch (nau.getRate()) {
    case NAU7802_RATE_10SPS:  Serial.println("10 SPS"); break;
    case NAU7802_RATE_20SPS:  Serial.println("20 SPS"); break;
    case NAU7802_RATE_40SPS:  Serial.println("40 SPS"); break;
    case NAU7802_RATE_80SPS:  Serial.println("80 SPS"); break;
    case NAU7802_RATE_320SPS:  Serial.println("320 SPS"); break;
  }

  // Take 10 readings to flush out readings
  for (uint8_t i=0; i<10; i++) {
    while (! nau.available()) delay(1);
    nau.read();
  }

  while (! nau.calibrate(NAU7802_CALMOD_INTERNAL)) {
    Serial.println("Failed to calibrate internal offset, retrying!");
    delay(1000);
  }
  Serial.println("Calibrated internal offset");

  while (! nau.calibrate(NAU7802_CALMOD_OFFSET)) {
    Serial.println("Failed to calibrate system offset, retrying!");
    delay(1000);
  }
  Serial.println("Calibrated system offset");
delay(5000);
}



void read_nsmpl(int32_t arr[25]){     //pass array to function
  // Take 10 readings to flush out readings
  Serial.println("flushing"); 
  
  for (uint8_t i=0; i<10; i++) {
    while (! nau.available()) delay(1);
    nau.read();
  }
  
  Serial.println("taking data...");
  digitalWrite(led, HIGH);

  for (int i = 0; i < 25; i++){
      while (!nau.available()) delay(1);
      int32_t val = nau.read();
      arr[i] = val;
      Serial.print("sample"); 
      Serial.println(i);
    }

  digitalWrite(led, LOW);
}


int32_t* calc_stats(int32_t* input){    //pass pointer to array, return pointer to array
  static int32_t stats[2]; 
  stats[0] = 0;  //sum
  stats[1] = 0;  // st. dev.

  for (int i = 0; i < 25; i++){
      stats[0] += input[i];
  }
  
  stats[0] = stats[0]/25;  //calculate average.
  
  for (int i = 0; i < 25; i++){
      stats[1] += (input[i] - stats[0])*(input[i] - stats[0]);
  }
  float sdev = sqrt(stats[1]/25);
  stats[1] = round(sdev);
  return stats;  //return pointer
}


void loop() {
  //do nothing until button pressed.
  while (digitalRead(button)) {
    delay(1);
  }  
  
  int32_t results[25];
  read_nsmpl(results);   //array with all the samples.
  
  int32_t* sample_stats = calc_stats(results);

  Serial.print("ave = ");
  Serial.print(sample_stats[0]);
  Serial.print(",   sd = ");
  Serial.println(sample_stats[1]);
  //while (true);
}