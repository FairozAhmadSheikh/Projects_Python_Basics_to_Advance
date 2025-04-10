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
    def format_time(self, seconds):
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02}:{secs:02}"

    def update_timer(self):
        while self.is_running and self.remaining > 0:
            time.sleep(1)
            self.remaining -= 1
            self.timer_label.config(text=self.format_time(self.remaining))
        if self.remaining == 0 and self.is_running:
            self.is_break = not self.is_break
            self.remaining = self.break_length if self.is_break else self.session_length
            session_type = "Break Time!" if self.is_break else "Focus Session"
            self.session_label.config(text=session_type)
            self.start_timer()
        def start_timer(self):
            if not self.is_running:
                self.is_running = True
                thread = threading.Thread(target=self.update_timer)
                thread.daemon = True
                thread.start()
        def reset_timer(self):
            self.is_running = False
            self.is_break = False
            self.remaining = self.session_length
            self.timer_label.config(text=self.format_time(self.remaining))
            self.session_label.config(text="Focus Session")
