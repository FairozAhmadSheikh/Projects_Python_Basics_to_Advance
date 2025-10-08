import requests  # for making HTTP requests
import time      # for simulating loading delays
import sys       # for terminal animations
import textwrap  # for wrapping long text


# function to create a typing animation
def slow_print(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()