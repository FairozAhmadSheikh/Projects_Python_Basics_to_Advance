import cv2
import tkinter as tk
from PIL import Image, ImageTk
import datetime
import os
# Create snapshots directory if not exists
os.makedirs("snapshots", exist_ok=True)
# Load Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
