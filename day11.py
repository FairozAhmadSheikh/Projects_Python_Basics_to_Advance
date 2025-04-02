import numpy as np
import cv2
import random
import time

def generate_maze(size=20):
    """Generates a random maze using recursive division."""
    maze = np.ones((size, size), dtype=np.uint8) * 255