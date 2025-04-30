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