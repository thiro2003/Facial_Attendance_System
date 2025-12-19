# Face Recognition Attendance System

A Flask-based attendance system that uses face recognition to mark daily attendance. Users can register with their face image, and the system automatically marks attendance for recognized faces. It also auto-marks users as absent if not detected for the day.

## Features
- User Registration: Upload your face image, name, email, and password.
- Face Recognition Attendance: Marks attendance automatically using a webcam.
- Auto Absent Marking: Users not present are automatically marked absent for the day.
- Secure Login: Passwords are hashed using Werkzeug.
- Attendance Tracking: View attendance history on the home page.
- Flash Messages: Provides feedback for login, registration, and attendance.

## Tech Stack
- Backend: Flask, Python
- Database: SQLite
- Face Recognition: face_recognition library
- Image Processing: OpenCV, PIL, NumPy
- Frontend: HTML templates with Jinja2
- ORM: SQLAlchemy

## Installation and Setup
1. Clone the repository:
2. Create a virtual environment and activate it:
- For Linux/macOS:
- python -m venv venv
- source venv/bin/activate
- For Windows:
- python -m venv venv
- venv\Scripts\activate
- 3. Install dependencies:
- pip install -r requirements.txt
- 4. Run the app:
- python app.py
- 5. Open your browser and go to `http://127.0.0.1:5000` to access the app.

## Project Structure
Face_Recognition_Attendance/
│
├── templates/
│ ├── login.html
│ ├── register.html
│ └── home.html
├── app.py # Main Flask app
├── requirements.txt # Python dependencies
└── README.md

## Usage
1. Register a new user with a face image.
2. Login using full name and password.
3. Go to Mark Attendance page: The system will use your webcam to recognize your face and mark attendance if recognized.
4. Home Page shows your attendance history.
5. Users not recognized will be automatically marked as absent for the day.

## Requirements
- Python 3.9+
- Flask
- Flask-SQLAlchemy
- OpenCV
- face_recognition
- NumPy
- PIL (Pillow)
- Werkzeug

## Notes
- Ensure your webcam is connected and accessible.
- For better recognition, use clear face images during registration.
- Tolerance for face matching is set to 0.5. Adjust in app.py if needed.

## License
This project is open-source and available under the MIT License.

 

