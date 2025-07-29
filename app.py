import streamlit as st
from auth import login_page
from profile import profile_page
import cv2
import mediapipe as mp
import numpy as np

# Global counters
counter = 0
wrong_counter = 0
stage = None
feedback = ""

def calculate_angle(a, b, c):

    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return 360 - angle if angle > 180 else angle


def pose_detection():
    global counter, wrong_counter, stage, feedback

    st.subheader("🏋️‍♀️ Real-Time Pose Detection")
    run = st.checkbox("✅ Start Camera")
    FRAME_WINDOW = st.image([])

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    while run:
        ret, frame = cap.read()
        if not ret:
            st.warning("❗ Failed to grab frame")
            break

        frame = cv2.flip(frame, 1)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

            knee_angle = calculate_angle(hip, knee, ankle)
            back_angle = calculate_angle(shoulder, hip, knee)

            if knee_angle < 90:
                if stage == 'up':
                    if 160 < back_angle < 195:
                        counter += 1
                        feedback = "✅ Good Squat"
                    else:
                        wrong_counter += 1
                        feedback = "❌ Keep Your Back Straight"
                    stage = 'down'
            elif knee_angle > 160:
                stage = 'up'
                feedback = "⬇️ Go Down"

            cv2.putText(image, f'Correct: {counter}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(image, f'Incorrect: {wrong_counter}', (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(image, feedback, (10, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        FRAME_WINDOW.image(image, channels="BGR")

    cap.release()


def main():
    if 'user' not in st.session_state:
        login_page()
    else:
        st.title("🏋️‍♂️ Welcome to AI Fitness Coach")
        st.write("Logged in as:", st.session_state['user']['email'])

        # Logout button
        if st.button("Logout"):
            del st.session_state['user']
            st.experimental_rerun()

        # Sidebar page selection
        page = st.sidebar.selectbox("📋 Choose Page", ["🏠 Profile", "💪 Workout"])

        # Route pages
        if page == "🏠 Profile":
            profile_page(st.session_state['user'])  # Pass logged-in user
        elif page == "💪 Workout":
            pose_detection()


if __name__ == "__main__":
    main()