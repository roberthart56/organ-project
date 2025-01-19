void setup() {
  Serial.begin(0);
  while (!Serial) {
    // Wait for USB Serial to connect
  }
  Serial.println("USB Serial initialized");
  
  Serial1.setTX(D6);   // TX on GPIO0
  Serial1.setRX(-D7);  // Disable RX functionality
  Serial1.begin(115200);  
  pinMode(D7, INPUT_PULLUP);  //button on pin that would normally be RX.
  pinMode(D9, INPUT_PULLUP);  //button two pins over.
  
}

void loop() {
  Serial.print(digitalRead(D7));
  Serial.print(", ");
  Serial.println(digitalRead(D9));
  delay(100);

}
