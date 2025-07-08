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
