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
    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✔" if task['completed'] else "✗"
            self.task_listbox.insert(tk.END, f"{status} {task['task']}")

    def add_task(self):
        task_text = self.entry.get()
        if not task_text:
            messagebox.showwarning("Warning", "Please enter a task.")
            return
        self.tasks.append({"id": str(uuid.uuid4()), "task": task_text, "completed": False})
        save_tasks(self.tasks)
        self.entry.delete(0, tk.END)
        self.refresh_task_list()

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if not selected:
            return
        index = selected[0]
        del self.tasks[index]
        save_tasks(self.tasks)
        self.refresh_task_list()

    def clear_tasks(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks?"):
            self.tasks = []
            save_tasks(self.tasks)
            self.refresh_task_list()

    def complete_task(self):
        selected = self.task_listbox.curselection()
        if not selected:
            return
        index = selected[0]
        self.tasks[index]['completed'] = True
        save_tasks(self.tasks)
        self.refresh_task_list()
