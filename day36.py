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