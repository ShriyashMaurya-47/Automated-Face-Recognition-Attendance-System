# Face Recognition Attendance System

A **Python-based real-time face recognition attendance system** using OpenCV, Face Recognition, and Excel for attendance tracking. This system supports **liveness detection** to prevent spoofing and ensures accurate attendance marking in low-light conditions.

---

## Features

* Real-time face recognition with webcam.
* Liveness detection to prevent spoofing:

  * Eye detection (blink detection)
  * Simple face rotation challenges
* Automatic attendance marking in an Excel file (`attendance.xlsx`).
* Add new faces with verification and store them in a JSON database (`faces.json`) and images folder (`faces/`).
* Lighting check for low-light conditions.
* Easy-to-use menu interface:

  * Start attendance
  * View known faces
  * Exit

---

## Requirements

* Python 3.8+
* Libraries:

  ```
  pip install opencv-python face_recognition numpy pandas
  ```
* OpenCV Haar Cascade (already included with OpenCV):

  * `haarcascade_eye.xml` for eye detection

---

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/ShriyashMaurya-47/Automated-Face-Recognition-Attendance-System.git
   cd Face-Attendance-System
   ```

2. Install required Python packages:

   ```
   pip install -r requirements.txt
   ```

3. Make sure you have a webcam connected for real-time attendance.

---

## Usage

1. Run the system:

   ```
   python attendance_system.py
   ```

2. Select options from the menu:

   * `1` → Start Attendance
   * `2` → View Known Faces
   * `3` → Exit

3. For new faces:

   * The system will ask you to perform liveness challenges.
   * Enter the name of the person to save their face.

4. Attendance is automatically updated in `attendance.xlsx` with the current date.

---

## File Structure

```
Face-Attendance-System/
│
├── faces/                 # Folder storing captured face images
├── attendance.xlsx        # Excel file for attendance tracking
├── faces.json             # JSON database of face encodings
├── attendance_system.py   # Main Python script
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## How It Works

1. **Face Recognition**
   Uses `face_recognition` library to identify faces in real-time.

2. **Liveness Detection**

   * Eye detection using OpenCV Haar Cascade (`haarcascade_eye.xml`)
   * Optional face movement challenges (turn left/right)

3. **Attendance Logging**

   * Attendance is stored in an Excel file.
   * Each row represents a date, and columns represent students.

4. **Adding New Faces**

   * When an unknown face is detected, the system performs liveness check.
   * After verification, face is saved in `faces/` and encoding in `faces.json`.

---

## Tips

* Ensure good lighting for better recognition accuracy.
* Sit or stand still while capturing new faces.
* Maintain a clean background if possible.

---

## License

This project is licensed under the MIT License.

---

## Author

**Shriyash Kumar Maurya**

* BCA Student | Developer
* GitHub: https://github.com/ShriyashMaurya-47
* Email: shriyashmaurya1@gmail.com

