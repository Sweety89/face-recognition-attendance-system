import face_recognition
import numpy as np
from database import get_connection

def insert_face(user_name, image_path):
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)

    if not encodings:
        print("No face found.")
        return

    new_encoding = encodings[0]
    new_encoding_bytes = new_encoding.tobytes()

    # Retrieve all existing encodings from DB
    cursor.execute("SELECT user_id, user_name, image_encoding FROM user_images")
    all_users = cursor.fetchall()

    for user_id, existing_name, existing_encoding_bytes in all_users:
        existing_encoding = np.frombuffer(existing_encoding_bytes, dtype=np.float64)
        match = face_recognition.compare_faces([existing_encoding], new_encoding)[0]

        if match:
            print(f"A face match was found for existing user: {existing_name}")
            choice = input(f"Do you want to replace the name '{existing_name}' with '{user_name}'? (y/n): ").strip().lower()
            if choice == 'y':
                cursor.execute("UPDATE user_images SET user_name = %s WHERE user_id = %s", (user_name, user_id))
                connection.commit()
                print(f"Name updated to '{user_name}'.")
            else:
                print("No changes made.")
            connection.close()
            return

    # If no match found, insert as new user
    cursor.execute("INSERT INTO user_images (user_name, image_encoding) VALUES (%s, %s)",
                   (user_name, new_encoding_bytes))
    connection.commit()
    print(f"Inserted encoding for new user: {user_name}.")
    connection.close()
