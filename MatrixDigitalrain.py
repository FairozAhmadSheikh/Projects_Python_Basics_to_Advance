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
        # Move cursor to the start of the current column
        sys.stdout.write(f"\033[{1};{i + 1}H")

        # Print the lead character in green
        if columns[i] > 0:
            sys.stdout.write(f"\033[32m{random.choice(chars)}")
        # Print the rest of the trail in dark green
        for j in range(1, columns[i]):
            sys.stdout.write(f"\033[{j + 1};{i + 1}H\033[90m{random.choice(chars)}")
            
        # Move cursor and print a space to erase the last character in the trail
        if columns[i] > 0 and columns[i] < rows:
            sys.stdout.write(f"\033[{columns[i] + 1};{i + 1}H ")