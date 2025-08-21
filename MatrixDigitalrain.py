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
