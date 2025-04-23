# pip install opencv-python numpy

import cv2
import numpy as np

# Load pre-trained colorization model
prototxt = "colorization_deploy_v2.prototxt"
model = "colorization_release_v2.caffemodel"
points = "pts_in_hull.npy"

net = cv2.dnn.readNetFromCaffe(prototxt, model)
pts = np.load(points)

# Add cluster centers to the model
class8 = net.getLayerId("class8_ab")
conv8 = net.getLayerId("conv8_313_rh")
pts = pts.transpose().reshape(2, 313, 1, 1)
net.getLayer(class8).blobs = [pts.astype(np.float32)]
net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

def colorize_image(img_path):
    bw = cv2.imread(img_path)
    normalized = bw.astype("float32") / 255.0
    lab = cv2.cvtColor(normalized, cv2.COLOR_BGR2LAB)

    resized = cv2.resize(lab, (224, 224))
    L = resized[:, :, 0]
    L -= 50

    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
    ab = cv2.resize(ab, (bw.shape[1], bw.shape[0]))

    L = lab[:, :, 0]
    colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
    colorized = np.clip(colorized, 0, 1)

    # Display
    cv2.imshow("Black & White", bw)
    cv2.imshow("Colorized", (colorized * 255).astype("uint8"))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
# Example
colorize_image("bw_photo.jpg")