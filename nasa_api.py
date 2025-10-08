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
# function to display a simple loading spinner
def loading_animation(message="Fetching data"):
    animation = "|/-\\"
    for i in range(20):
        time.sleep(0.1)
        sys.stdout.write(f"\r{message} " + animation[i % len(animation)])
        sys.stdout.flush()
    print("\r", end="")
