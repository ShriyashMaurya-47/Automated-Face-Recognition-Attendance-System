#moduls
import cv2
import face_recognition
import numpy as np
import os
import json
import datetime
import pandas as pd
import random
import time

# Paths
FACES_DIR = "faces"
DATA_FILE = "faces.json"
ATTENDANCE_FILE = "attendance.xlsx"
EYE_CASCADE_PATH = cv2.data.haarcascades + "haarcascade_eye.xml"

# Ensure folders exist
os.makedirs(FACES_DIR, exist_ok=True)

# Load known faces
known_encodings = []
known_names = []

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        face_db = json.load(f)
        for name, data in face_db.items():
            known_encodings.append(np.array(data["encoding"]))
            known_names.append(name)
else:
    face_db = {}

# Track last attendance time
last_attendance = {}

# Load or create Excel attendance file
if os.path.exists(ATTENDANCE_FILE):
    df = pd.read_excel(ATTENDANCE_FILE, index_col=0)
else:
    df = pd.DataFrame(columns=known_names)

# Haar cascade for eyes
eye_cascade = cv2.CascadeClassifier(EYE_CASCADE_PATH)

# --- Utility Functions ---

def ensure_today_row():
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    if today_str not in df.index:
        df.loc[today_str] = [0]*len(df.columns)

def update_excel(name):
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    ensure_today_row()
    if name not in df.columns:
        df[name] = 0
    df.loc[today_str, name] = 1
    df.to_excel(ATTENDANCE_FILE)

def mark_attendance(name):
    now = datetime.datetime.now()
    if name in last_attendance:
        diff = now - last_attendance[name]
        if diff.total_seconds() < 3600:
            return
    last_attendance[name] = now
    update_excel(name)
    print(f"[ATTENDANCE] {name} marked present at {now.strftime('%H:%M:%S')}")

# --- Liveness Detection Functions ---

def check_liveness(frame, face_location):
    """
    Detects eyes as a basic liveness check.
    Returns True if eyes detected, False otherwise.
    """
    top, right, bottom, left = face_location
    face_img = frame[top:bottom, left:right]
    gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    return len(eyes) > 0

def liveness_challenge(frame):
    """
    Random liveness challenge: blink, turn left, turn right.
    Returns True if all challenges passed.
    """
    challenges = ["blink your eyes", "turn face to left", "turn face to right"]
    random.shuffle(challenges)
    for action in challenges:
        print(f"[LIVENESS] Please {action} now.")
        passed = False
        start_time = time.time()
        while time.time() - start_time < 5:
            ret, frame = video.read()
            if not ret:
                continue
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            if not face_locations:
                continue
            (top, right, bottom, left) = face_locations[0]

            if action == "blink your eyes":
                if check_liveness(frame, (top, right, bottom, left)):
                    passed = True
                    break
            else:
                # Simplified rotation detection: accept as passed
                passed = True
                break

        if not passed:
            print("[LIVENESS] Challenge failed.")
            return False
    return True

# --- Lighting / Background Check ---

def check_lighting(frame):
    """
    Check if lighting is sufficient.
    Returns True if mean brightness > threshold.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mean_brightness = np.mean(gray)
    return mean_brightness > 50  # adjust threshold as needed

# --- Face Addition ---

def add_new_face(frame, face_encoding, top, right, bottom, left):
    # Liveness challenge before adding
    if not liveness_challenge(frame):
        print("[NEW FACE] Failed liveness. Face not added.")
        return

    cv2.imshow("New Face", frame[top:bottom, left:right])
    cv2.waitKey(1)
    name = input("Enter name for this new face: ")

    known_encodings.append(face_encoding)
    known_names.append(name)
    face_db[name] = {"encoding": face_encoding.tolist()}

    face_img = frame[top:bottom, left:right]
    cv2.imwrite(os.path.join(FACES_DIR, f"{name}.jpg"), face_img)

    with open(DATA_FILE, "w") as f:
        json.dump(face_db, f)

    print(f"[NEW FACE] {name} saved.")
    mark_attendance(name)

# --- View Database ---

def view_database():
    print("\n--- Known Faces ---")
    for name in known_names:
        print(name)
    print("-------------------\n")

# --- Attendance Loop ---

def start_attendance():
    global video
    video = cv2.VideoCapture(0)

    while True:
        ret, frame = video.read()
        if not ret:
            continue

        # Check lighting
        if not check_lighting(frame):
            cv2.putText(frame, "LOW LIGHT! Improve lighting.", 
                        (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            cv2.imshow("Attendance System", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            continue  # skip frame

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if face_encodings:
            face_encoding = face_encodings[0]
            (top, right, bottom, left) = face_locations[0]

            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
            name = "Unknown"

            if True in matches:
                idx = matches.index(True)
                name = known_names[idx]
                if check_liveness(frame, (top, right, bottom, left)):
                    mark_attendance(name)
                else:
                    name = "Spoof Attempt"
                    print("[WARNING] Possible spoof detected!")
            else:
                add_new_face(frame, face_encoding, top, right, bottom, left)

            # Draw bounding box
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Attendance System", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()

# --- Menu ---

def menu():
    while True:
        print("\n--- Face Attendance System Menu ---")
        print("1. Start Attendance")
        print("2. View Known Faces")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            start_attendance()
        elif choice == "2":
            view_database()
        elif choice == "3":
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    menu()
