import numpy as np
import cv2
import random
import time

def generate_maze(size=20):
    """Generates a random maze using recursive division."""
    maze = np.ones((size, size), dtype=np.uint8) * 255
    def divide(x, y, width, height):
        if width < 3 or height < 3:
            return
        
        horizontal = width < height
        if horizontal:
            wx = x
            wy = y + random.randint(1, height - 2)
            px = wx + random.randint(0, width - 1)
            for i in range(x, x + width):
                if i != px:
                    maze[wy, i] = 0
            divide(x, y, width, wy - y)
            divide(x, wy + 1, width, y + height - wy - 1)
        else:
            wx = x + random.randint(1, width - 2)
            wy = y
            py = wy + random.randint(0, height - 1)
            for i in range(y, y + height):
                if i != py:
                    maze[i, wx] = 0
            divide(x, y, wx - x, height)
            divide(wx + 1, y, x + width - wx - 1, height)