#include <avr/io.h>



void setup() {
  Serial.begin(9600);
  // Configure ADC control register
  ADC0.CTRLA = ADC_ENABLE_bm;               // Enable ADC
  ADC0.CTRLB = ADC_SAMPNUM_ACC16_gc;        // Accumulate 16 samples for better resolution
  ADC0.CTRLC = ADC_REFSEL_1024MV_gc         // Use VDD as reference.  Mnemonic edited 1/2/25. 
              | ADC_PRESC_DIV16_gc;         // Prescaler: divide clock by 16

  // Configure MUX for differential input
  ADC0.MUXPOS = ADC_MUXPOS_AIN2_gc;         // Positive input: AIN2
  ADC0.MUXNEG = ADC_MUXNEG_AIN1_gc;         // Negative input: AIN1

  // Configure gain (e.g., 16x)
  ADC0.PGACTRL = ADC_GAIN_16X_gc;   // Programmable gain set to 16x

  // Start first conversion
  ADC0.COMMAND |= ADC_START_IMMEDIATE_gc;
}

void loop() {
  // Wait for ADC result ready
  while (!(ADC0.INTFLAGS & ADC_RESRDY_bm));
  
  // Read the result
  int16_t result = ADC0.RESULT;
  Serial.println(result);
  ADC0.COMMAND |= ADC_START_IMMEDIATE_gc;

  // Do something with the result
}
