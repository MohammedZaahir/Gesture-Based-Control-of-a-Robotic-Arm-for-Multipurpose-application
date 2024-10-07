#include <Servo.h>

// Create Servo objects for the four servos
Servo servo1, servo2, servo3, servo4;

int angles[4] = {0, 0, 0, 0};  // Array to hold angles for the four servos
String inputString = "";  // String to hold incoming data

void setup() {
  // Attach servos to respective pins
  servo1.attach(9);
  servo2.attach(10);
  servo3.attach(11);
  servo4.attach(12);

  // Begin serial communication at 9600 baud
  Serial.begin(9600);

  // Initialize all servos to 0 degrees
  resetServos();
}

void loop() {
  // Read incoming data
  if (Serial.available()) {
    char c = (char)Serial.read();
    if (c == '\n') {
      processInputString();  // Process the string when newline detected
      inputString = "";  // Clear the string after processing
    } else {
      inputString += c;  // Append the character to input string
    }
  }
}

void processInputString() {
  // Parse the input string into servo angles
  int indices[3] = {inputString.indexOf(','), inputString.indexOf(',', inputString.indexOf(',') + 1), inputString.indexOf(',', inputString.indexOf(',', inputString.indexOf(',') + 1) + 1)};

  if (indices[2] > 0) {
    angles[0] = inputString.substring(0, indices[0]).toInt();
    angles[1] = inputString.substring(indices[0] + 1, indices[1]).toInt();
    angles[2] = inputString.substring(indices[1] + 1, indices[2]).toInt();
    angles[3] = inputString.substring(indices[2] + 1).toInt();

    moveServos();
  }
}

void moveServos() {
  // Move the servos to the respective angles
  servo1.write(angles[0]);
  servo2.write(angles[1]);
  servo3.write(angles[2]);
  servo4.write(angles[3]);

  // Optional: Print angles for debugging
  Serial.print("Servo Angles: ");
  for (int i = 0; i < 4; i++) {
    Serial.print(angles[i]);
    if (i < 3) Serial.print(", ");
  }
  Serial.println();
}

void resetServos() {
  servo1.write(0);
  servo2.write(0);
  servo3.write(0);
  servo4.write(0);
}
