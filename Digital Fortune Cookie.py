import os
import random
import time
import webbrowser

#  Each time you run it, it gives you a randomly generated digital "fortune",
# opens a calming website, and plays a unique ASCII animation.
fortunes = [
    "You will debug a bug no one else could.",
    "Today, your code compiles on the first try.",
    "A surprise pull request will brighten your day.",
    "Refactor now, profit later.",
    "Your logic is as sharp as Python’s syntax.",
]
ascii_frames = [
    r"""
     ( •_•)
    <)   )╯ Fortune loading...
     /   \
    """,
    r"""
     ( •_•)
    <)   )╯ Your fortune is ready!
     /   \
    """,
    r"""
     ( •_•)
    <)   )╯ Here it comes...
     /   \
    """,
]
# Display ASCII animation
for i in range(3):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(ascii_frames[i % len(ascii_frames)])
    time.sleep(1)
# Show the fortune
os.system('cls' if os.name == 'nt' else 'clear')
fortune = random.choice(fortunes)