#include <Servo.h>

// Creating Servo objects for controlling the four motors
Servo servo1, servo2, servo3, servo4;

int angles[4] = {0, 0, 0, 0};  // This array will store the angles for the four servos
String inputString = "";  // I use this to hold incoming serial data as a string

void setup() {
  // Attaching the servos to their respective pins
  servo1.attach(9);
  servo2.attach(10);
  servo3.attach(11);
  servo4.attach(12);

  // Setting up the serial communication so we can send data from Python (9600 baud rate)
  Serial.begin(9600);

  // Setting all servos to 0 degrees at startup
  resetServos();
}

void loop() {
  // Checking if there's any data coming from the serial port
  if (Serial.available()) {
    char c = (char)Serial.read();  // Reading each character from the incoming data
    if (c == '\n') {
      // If newline detected, process the entire string and reset it
      processInputString();
      inputString = "";  // Clear the string after handling the data
    } else {
      inputString += c;  // Keep adding characters to the string until a newline is found
    }
  }
}

void processInputString() {
  // I'm parsing the string here to break it into four parts representing the servo angles
  int indices[3] = {
    inputString.indexOf(','),  // Finding first comma
    inputString.indexOf(',', inputString.indexOf(',') + 1),  // Second comma
    inputString.indexOf(',', inputString.indexOf(',', inputString.indexOf(',') + 1) + 1)  // Third comma
  };

  if (indices[2] > 0) {  // Only proceed if all three commas were found
    // Extracting the angles from the string and converting them to integers
    angles[0] = inputString.substring(0, indices[0]).toInt();
    angles[1] = inputString.substring(indices[0] + 1, indices[1]).toInt();
    angles[2] = inputString.substring(indices[1] + 1, indices[2]).toInt();
    angles[3] = inputString.substring(indices[2] + 1).toInt();

    // Move the servos based on these angles
    moveServos();
  }
}

void moveServos() {
  // Sending the calculated angles to each of the servos
  servo1.write(angles[0]);
  servo2.write(angles[1]);
  servo3.write(angles[2]);
  servo4.write(angles[3]);

  // Printing the angles to the serial monitor for debugging purposes
  Serial.print("Servo Angles: ");
  for (int i = 0; i < 4; i++) {
    Serial.print(angles[i]);
    if (i < 3) Serial.print(", ");  // Add commas between angles except for the last one
  }
  Serial.println();  // Move to the next line after printing all angles
}

void resetServos() {
  // Resets all servos to 0 degrees during initialization
  servo1.write(0);
  servo2.write(0);
  servo3.write(0);
  servo4.write(0);
}
