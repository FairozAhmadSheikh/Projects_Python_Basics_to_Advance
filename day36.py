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
encode_list_known = find_encodings(images)
print("🔍 Face encodings loaded.")

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    img_small = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)

    faces_cur_frame = face_recognition.face_locations(img_small)
    encodes_cur_frame = face_recognition.face_encodings(img_small, faces_cur_frame)

    for encode_face, face_loc in zip(encodes_cur_frame, faces_cur_frame):
        matches = face_recognition.compare_faces(encode_list_known, encode_face)
        face_dist = face_recognition.face_distance(encode_list_known, encode_face)

        match_index = np.argmin(face_dist)

        if matches[match_index]:
            name = names[match_index].upper()
            y1, x2, y2, x1 = [v * 4 for v in face_loc]  # Resize to original size
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            mark_attendance(name)
            cv2.imshow('📷 Face Recognition Attendance', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()