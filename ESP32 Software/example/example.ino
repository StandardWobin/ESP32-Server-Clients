// declare constant pin values for LEDS or Sensors
// accessible on I/O Pin 5 and I/O Pin 26
// I/O stand for Input output
const int LED_PIN = 5;
const int LED_2_PIN = 26;

// declare pin for input toch sensor
const int touch_pin = 14;


////////////////////////////////////////
// will be run once at start (after ESP gains power it imidiate runs this function ONCE)
void setup()
{
  // declare I/O pins as output
  pinMode (LED_PIN, OUTPUT);
  pinMode (LED_2_PIN, OUTPUT);


  // touch sensor does not need to be set to INPUT!!
  
  // prints text to serial output (USB Cable)
  // can be see in Arduino programm -> tools -> Serial Monitor. Do not forget to change BAUT rate to ESP32 specific value 115200
  Serial.println("setup function finished");

}


// repeats forever
void loop()
{
  // gives maximum voltage (3,3 V for ESP32)
  digitalWrite (LED_2_PIN, HIGH);
  digitalWrite (LED_PIN, HIGH);

  // waits 500 ms
  delay(500);
  
  // stops voltage
  digitalWrite (LED_PIN, LOW);
  delay(500);

  // Prints in one line ( only println makes new line) the capacity value of pin 14
  Serial.print("Input (Pin 14) Input value (touch): ");
  Serial.print(touchRead(touch_pin));
  Serial.println("");


}
