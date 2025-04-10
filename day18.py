import tkinter as tk
import time
import threading

class PomodoroTimer:
    def __init__(self, master):
        self.master = master
        self.master.title("Pomodoro Timer")
        self.master.geometry("400x300")
        self.master.resizable(False, False)

        self.session_length = 25 * 60  # 25 minutes
        self.break_length = 5 * 60     # 5 minutes
        self.is_running = False
        self.is_break = False
        self.remaining = self.session_length

        self.label = tk.Label(master, text="Pomodoro Timer", font=("Arial", 20))
        self.label.pack(pady=10)

        self.timer_label = tk.Label(master, text=self.format_time(self.remaining), font=("Arial", 40))
        self.timer_label.pack(pady=10)

        self.start_btn = tk.Button(master, text="Start", width=15, command=self.start_timer)
        self.start_btn.pack(pady=5)

        self.reset_btn = tk.Button(master, text="Reset", width=15, command=self.reset_timer)
        self.reset_btn.pack(pady=5)

        self.session_label = tk.Label(master, text="Focus Session", font=("Arial", 16))
        self.session_label.pack(pady=10)

    