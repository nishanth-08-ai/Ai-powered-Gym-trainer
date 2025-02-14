import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from tkinter import simpledialog, messagebox


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle


def ask_reps():
    root = tk.Tk()
    root.withdraw()
    user_input = simpledialog.askinteger("Input", "How many reps would you like to do?")
    root.destroy()
    return user_input


# Get desired reps from user
desired_reps = ask_reps()
if desired_reps is None:
    print("No input provided. Exiting...")
    exit()

# Rep tracking variables
left_counter = 0
right_counter = 0
left_stage = None
right_stage = None
counter = 0
current_hand = 'left'

cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Get frame dimensions
        frame_height, frame_width, _ = frame.shape

        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = pose.process(image)

        # Convert back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark

            # Extract landmarks and scale to frame dimensions
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * frame_width,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * frame_height]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * frame_width,
                          landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * frame_height]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x * frame_width,
                          landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y * frame_height]

            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * frame_width,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * frame_height]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x * frame_width,
                           landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y * frame_height]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x * frame_width,
                           landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y * frame_height]

            # Calculate angles
            left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
            right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

            # Angle percentage
            left_angle_percentage = np.interp(left_angle, (30, 160), (100, 0))
            right_angle_percentage = np.interp(right_angle, (30, 160), (100, 0))

            # Form detection
            left_form = "Good Form" if 30 < left_angle < 160 else "Bad Form"
            right_form = "Good Form" if 30 < right_angle < 160 else "Bad Form"

            left_color = (0, 255, 0) if left_form == "Good Form" else (0, 0, 255)
            right_color = (0, 255, 0) if right_form == "Good Form" else (0, 0, 255)

            # Display angles & form feedback
            cv2.putText(image, f'{int(left_angle)}°', (int(left_elbow[0] - 30), int(left_elbow[1] - 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, left_color, 2)
            cv2.putText(image, left_form, (int(left_elbow[0] - 50), int(left_elbow[1] - 50)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, left_color, 2)

            cv2.putText(image, f'{int(right_angle)}°', (int(right_elbow[0] - 30), int(right_elbow[1] - 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, right_color, 2)
            cv2.putText(image, right_form, (int(right_elbow[0] - 50), int(right_elbow[1] - 50)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, right_color, 2)

            # Curl logic for left arm
            if current_hand == 'left':
                if left_angle > 160:
                    left_stage = "down"
                if left_angle < 30 and left_stage == 'down':
                    left_stage = "up"
                    left_counter += 1
                    current_hand = 'right'

            # Curl logic for right arm
            if current_hand == 'right':
                if right_angle > 160:
                    right_stage = "down"
                if right_angle < 30 and right_stage == 'down':
                    right_stage = "up"
                    right_counter += 1
                    counter += 1
                    current_hand = 'left'

        except:
            pass

        # Display rep counter
        cv2.rectangle(image, (0, 0), (350, 140), (245, 117, 16), -1)
        cv2.putText(image, 'Reps', (15, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)
        cv2.putText(image, f'Left: {left_counter}', (15, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
        cv2.putText(image, f'Right: {right_counter}', (15, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        # Render pose landmarks
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

        cv2.imshow('Mediapipe Feed', image)

        if counter >= desired_reps:
            messagebox.showinfo("Info", "Exercise complete! Great job!")
            break

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()