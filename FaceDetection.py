import cv2
import tkinter as tk
from PIL import Image, ImageTk
import datetime
import os
# Create snapshots directory if not exists
os.makedirs("snapshots", exist_ok=True)
# Load Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
class FaceDetectionApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Real-Time Face Detection")

        self.video_capture = cv2.VideoCapture(0)

        self.label = tk.Label(window)
        self.label.pack()

        self.snapshot_btn = tk.Button(window, text="📷 Take Snapshot", command=self.take_snapshot, bg='blue', fg='white', font=('Arial', 12, 'bold'))
        self.snapshot_btn.pack(pady=10)

        self.update_frame()
    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            # Convert to grayscale for detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Detect faces
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            # Draw rectangles
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # Convert BGR to RGB for Tkinter
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb_frame)
            imgtk = ImageTk.PhotoImage(image=img)

            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

        self.window.after(10, self.update_frame)
    def take_snapshot(self):
        ret, frame = self.video_capture.read()
        if ret:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"snapshots/face_snapshot_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            print(f"✅ Snapshot saved: {filename}")
    def __del__(self):
        self.video_capture.release()
