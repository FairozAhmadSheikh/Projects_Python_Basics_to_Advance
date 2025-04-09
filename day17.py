import tkinter as tk
from tkinter import messagebox
import json
import os
import uuid

# Path to the task storage file
TASKS_FILE = "tasks.json"

# Load tasks from file
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)