# pip install opencv-python face-recognition numpy pandas
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pandas as pd

# Load known images
path = 'images'  # Folder with images of known faces
images = []
names = []

for filename in os.listdir(path):
    img = cv2.imread(f'{path}/{filename}')
    images.append(img)
    names.append(os.path.splitext(filename)[0])
def find_encodings(images):
    encode_list = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)
        if encode:
            encode_list.append(encode[0])
    return encode_list
def mark_attendance(name):
    now = datetime.now()
    date_string = now.strftime('%Y-%m-%d')
    time_string = now.strftime('%H:%M:%S')

    if not os.path.exists("attendance.csv"):
        df = pd.DataFrame(columns=["Name", "Date", "Time"])
        df.to_csv("attendance.csv", index=False)

    df = pd.read_csv("attendance.csv")

    if not ((df['Name'] == name) & (df['Date'] == date_string)).any():
        df = df.append({"Name": name, "Date": date_string, "Time": time_string}, ignore_index=True)
        df.to_csv("attendance.csv", index=False)
        print(f"✅ Attendance marked for {name} at {time_string}")

# Encode known faces