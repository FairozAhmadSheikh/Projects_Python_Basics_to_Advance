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
# Save tasks to file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

class TodoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do List Manager")
        self.master.geometry("600x500")

        self.tasks = load_tasks()

        # Input field
        self.entry = tk.Entry(master, font=("Arial", 14), width=40)
        self.entry.pack(pady=10)

        # Buttons
        self.add_btn = tk.Button(master, text="Add Task", width=20, command=self.add_task)
        self.add_btn.pack(pady=5)

        self.delete_btn = tk.Button(master, text="Delete Selected Task", width=20, command=self.delete_task)
        self.delete_btn.pack(pady=5)

        self.clear_btn = tk.Button(master, text="Clear All Tasks", width=20, command=self.clear_tasks)
        self.clear_btn.pack(pady=5)

        self.complete_btn = tk.Button(master, text="Mark as Completed", width=20, command=self.complete_task)
        self.complete_btn.pack(pady=5)

        # Task listbox
        self.task_listbox = tk.Listbox(master, width=80, height=20, font=("Arial", 12))
        self.task_listbox.pack(pady=10)

        self.refresh_task_list()