import cv2
import mediapipe as mp
import serial
import time
import numpy as np

# Connecting to the Arduino on COM9
try:
    arduino = serial.Serial('COM9', 9600, timeout=1)
    time.sleep(2)  # Give the Arduino some time to reset before sending/receiving data
except serial.SerialException as e:
    print(f"Error: {e}")
    exit()

# Setting up MediaPipe to track just the right hand
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.6)

# Using the webcam for input
cap = cv2.VideoCapture(0)

def calculate_servo_angles(hand_landmarks, image_shape):
    """
    Here I'm calculating the servo angles based on the hand's movements (right hand).
    Focusing on horizontal, vertical, and depth movements for Servo 1, 2, and 3.
    Added adjustments to give better movement range for Servo 1.
    """
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

    # Normalizing the wrist and index finger positions relative to the image dimensions
    wrist_x, wrist_y = int(wrist.x * image_shape[1]), int(wrist.y * image_shape[0])
    index_x, index_y = int(index_finger_tip.x * image_shape[1]), int(index_finger_tip.y * image_shape[0])
    wrist_z, index_z = wrist.z, index_finger_tip.z

    # These are the horizontal, vertical, and depth differences based on hand movement
    horizontal_distance = index_x - wrist_x
    vertical_distance = index_y - wrist_y
    depth_distance = abs(wrist_z - index_z)

    # Debugging to see the horizontal distance for testing purposes
    print(f"Horizontal Distance: {horizontal_distance}")

    # Adjusted the range for horizontal movement to map properly to Servo 1
    angle_servo1 = np.clip(int(np.interp(horizontal_distance, [-250, 250], [0, 180])), 0, 180)

    # Debugging to check the Servo 1 angle calculation
    print(f"Servo 1 Angle: {angle_servo1}")
    
    # Mapping vertical movement to Servo 2
    angle_servo2 = np.clip(int(np.interp(vertical_distance, [-300, 300], [0, 180])), 0, 180)
    
    # Depth-based control for Servo 3
    angle_servo3 = np.clip(int(np.interp(depth_distance, [0, 1], [0, 180])), 0, 180)

    return angle_servo1, angle_servo2, angle_servo3

def is_hand_open(hand_landmarks):
    """
    I added this function to determine if the hand is open based on fingertip positions relative to the wrist.
    This will be used for controlling Servo 4.
    """
    wrist_y = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y
    fingertips = [hand_landmarks.landmark[i].y for i in [
        mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]]
    
    # If all fingertips are above the wrist, we consider the hand open
    return all(tip < wrist_y for tip in fingertips)

def send_servo_angles_to_arduino(angles):
    """This function sends the calculated servo angles to the Arduino for motor control."""
    try:
        message = f"{','.join(map(str, angles))}\n"
        arduino.write(message.encode())
    except serial.SerialException as e:
        print(f"Error: {e}")

def visualize_hand_landmarks(image, hand_landmarks):
    """I'm using this to draw the hand landmarks on the image to visually track hand movement."""
    for landmark in hand_landmarks.landmark:
        cx = int(landmark.x * image.shape[1])
        cy = int(landmark.y * image.shape[0])
        cv2.circle(image, (cx, cy), 5, (0, 255, 0), -1)

def display_servo_angles(image, angles):
    """To help debug, this displays the current servo angles on the screen."""
    for i, angle in enumerate(angles, 1):
        cv2.putText(image, f'Servo {i} Angle: {angle}', (10, i * 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

try:
    while True:
        # Capture frame from webcam
        success, image = cap.read()
        if not success:
            print("Error: Could not read from webcam.")
            break

        # Convert image to RGB as MediaPipe works in that color space
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]

            # Calculating the angles for the servos based on hand movement
            angle_servo1, angle_servo2, angle_servo3 = calculate_servo_angles(hand_landmarks, image.shape)
            
            # Check if the hand is open or closed, and control Servo 4 accordingly
            angle_servo4 = 60 if is_hand_open(hand_landmarks) else 0

            # Combine all servo angles, and ensure Servo 4 stays within range
            angles = [angle_servo1, angle_servo2, angle_servo3, np.clip(angle_servo4, 0, 60)]

            # Send the calculated angles to the Arduino for motor control
            send_servo_angles_to_arduino(angles)

            # Visualize the hand landmarks and show the current servo angles
            visualize_hand_landmarks(image, hand_landmarks)
            display_servo_angles(image, angles)

        # Display the processed image in a window
        cv2.imshow('Right Hand Tracking', image)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Cleanup: Release the webcam and close any open windows
    cap.release()
    cv2.destroyAllWindows()
    arduino.close()
