/* Sweep
by BARRAGAN <http://barraganstudio.com>
This example code is in the public domain.

modified 8 Nov 2013
by Scott Fitzgerald
http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>

Servo myservo,myservo2;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position
char t;
void setup() {
myservo.attach(9);  // attaches the servo on pin 9 to the servo object
myservo2.attach(10);
Serial.begin(9600);
while(!Serial){
}
Serial.println("Connected");
}

void loop() {

  if (Serial.available()) {
  
    t = Serial.read();
    if(t=='i'){
      for (pos = 0; pos <= 90; pos += 1) { // goes from 180 degrees to 0 degrees
      myservo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(20);                       // waits 15ms for the servo to reach the position
      }
    }
    if(t=='j'){
      for (pos = 90; pos >= 0; pos -= 1) { // goes from 0 degrees to 180 degrees
      // in steps of 1 degree
      myservo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(20);                       // waits 15ms for the servo to reach the position
      }
    }
    if(t=='k'){
      for (pos = 0; pos <= 90; pos += 1) { // goes from 180 degrees to 0 degrees
      myservo2.write(pos);              // tell servo to go to position in variable 'pos'
      delay(20);                       // waits 15ms for the servo to reach the position
      }
    }
    if(t=='l'){
      for (pos = 90; pos >= 0; pos -= 1) { // goes from 0 degrees to 180 degrees
      // in steps of 1 degree
      myservo2.write(pos);              // tell servo to go to position in variable 'pos'
      delay(20);                       // waits 15ms for the servo to reach the position
      }
    }
  }
}
