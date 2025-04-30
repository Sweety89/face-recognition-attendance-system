import cv2
import face_recognition
import numpy as np
from database import get_connection

def mark_attendance(encoding, marked_users):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT user_id, user_name, image_encoding FROM user_images")
    users = cursor.fetchall()

    for user_id, name, enc in users:
        db_enc = np.frombuffer(enc, dtype=np.float64)
        if face_recognition.compare_faces([db_enc], encoding)[0]:
            if user_id in marked_users:
                return name  # Already marked, skip

            cursor.execute("INSERT INTO attendance (user_id) VALUES (%s)", (user_id,))
            conn.commit()
            print(f"Attendance marked for {name}")
            marked_users.add(user_id)
            conn.close()
            return name

    conn.close()
    return None

def register_new_user(encoding, frame):
    name = input("Enter name for new user: ")
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO user_images (user_name, image_encoding) VALUES (%s, %s)",
                   (name, encoding.tobytes()))
    user_id = cursor.lastrowid
    cursor.execute("INSERT INTO attendance (user_id) VALUES (%s)", (user_id,))
    conn.commit()
    print(f"New user {name} registered and marked present.")
    conn.close()

def run_attendance():
    cap = cv2.VideoCapture(0)
    marked_users = set()  # Keep track of already marked users

    print("Scanning for faces. Please look at the camera...")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame. Exiting.")
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb)
        face_encodings = face_recognition.face_encodings(rgb, face_locations)

        if not face_encodings:
            print("No faces detected. Exiting.")
            break

        all_processed = True  # Assume all are processed unless we find otherwise

        for encoding in face_encodings:
            name = mark_attendance(encoding, marked_users)
            if not name:
                register_new_user(encoding, frame)
                # We still count it as processed after registering
            else:
                continue  # Already marked

        # After processing all current face encodings, exit
        print("Attendance completed. Exiting...")
        break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_attendance()
