# Face Recognition Attendance System

This project is a real-time attendance system using a webcam and face recognition. It stores and matches face encodings in a MySQL database and automatically marks attendance. If a new face is detected, it prompts the user to register and log their attendance.

## Features

- Real-time face detection using webcam
- Automatic attendance marking
- MySQL database integration for storing face encodings
- New user registration on unrecognised faces
- Avoids duplicate attendance per session

## Technologies Used

- Python
- OpenCV
- face_recognition (dlib-based)
- NumPy
- MySQL (via `mysql-connector-python`)

## Database Schema

### `user_images` Table

| Column       | Type        | Description                    |
|--------------|-------------|--------------------------------|
| user_id      | INT         | Primary key (Auto Increment)   |
| user_name    | VARCHAR(255)| Name of the user               |
| image_encoding | LONGBLOB  | Face encoding data             |

### `attendance` Table

| Column         | Type        | Description                    |
|----------------|-------------|--------------------------------|
| attendance_id  | INT         | Primary key (Auto Increment)   |
| user_id        | INT         | Foreign key (user_images)      |
| timestamp      | DATETIME    | Attendance timestamp           |


