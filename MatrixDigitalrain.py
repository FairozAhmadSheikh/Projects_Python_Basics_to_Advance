import os
import random
import time
import sys
# Get terminal dimensions
try:
    cols, rows = os.get_terminal_size()
except OSError:
    cols, rows = 80, 24 # Fallback for some environments

# The characters to use for the "rain"
chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;':\",./<>?`~"
columns = [0] * cols

while True:
    for i in range(cols):
        # If the column is at the top of the screen (i.e., inactive)
        if columns[i] == 0 and random.random() < 0.02:
            columns[i] = random.randint(10, rows - 5)