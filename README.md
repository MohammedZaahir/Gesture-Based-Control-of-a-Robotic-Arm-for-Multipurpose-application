# Gesture-Based-Control-of-a-Robotic-Arm-for-Multipurpose-application


This project involves controlling a robotic arm using hand gestures tracked via a webcam and MediaPipe. The hand movements are captured using OpenCV and MediaPipe, and the corresponding servo angles are calculated and sent to an Arduino to control the robotic arm's servos.

## Features

- Control a robotic arm using real-time hand tracking.
- 4 servos for different degrees of freedom.
- Servo angles are calculated based on the horizontal, vertical, and depth movements of the hand.
- Hand open/closed detection is used to control an additional servo.
- Wireless communication with the robotic arm via Bluetooth (optional in future updates).

## Hardware Requirements

- Arduino Uno 
- 4 servos
- Webcam or laptop camera
- USB Cable to connect Arduino to the computer
- Jumper wires
- breadboard

## Software Requirements

- Python 
- Arduino IDE
- OpenCV
- MediaPipe*
- pySerial

## Project Setup

1. Clone the repository:

2. Arduino:

Upload the provided Arduino code to your Arduino using the Arduino IDE.
Make sure the servos are connected to the correct pins: 9, 10, 11, and 12.

3. Python:

Install the required Python dependencies by running the following command:

pip install -r requirements.txt

4. Run the Python script:

The script will capture your hand movements using a webcam and send servo angles to the Arduino.




## How It Works
1. Hand Tracking: The MediaPipe library is used to detect hand landmarks in real-time using a webcam.
2. Servo Angle Calculation: The positions of the wrist and index finger tip are used to compute the angles for controlling the servos.
3. Communication with Arduino: The calculated angles are sent to the Arduino through serial communication, where the Arduino moves the servos based on these angles.


## Future Enhancements
1. Add wireless control via the HC-05 Bluetooth module.
2. Support for controlling multiple robotic arms simultaneously using different webcams.
3. Improve hand gesture recognition for more intuitive control.
