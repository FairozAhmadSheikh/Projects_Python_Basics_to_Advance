import tkinter as tk
from tkinter import messagebox
import random
# Sample questions for the quiz
questions = [
    {
        "question": "What is the capital of France?",
        "options": ["Paris", "London", "Berlin", "Madrid"],
        "answer": "Paris"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Saturn"],
        "answer": "Mars"
    },
    {
        "question": "Who wrote 'To Kill a Mockingbird'?",
        "options": ["Harper Lee", "Mark Twain", "J.K. Rowling", "Jane Austen"],
        "answer": "Harper Lee"
    },
       {
        "question": "What is the largest ocean on Earth?",
        "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
        "answer": "Pacific"
    },
    {
        "question": "Which element has the chemical symbol 'O'?",
        "options": ["Oxygen", "Gold", "Osmium", "Oxide"],
        "answer": "Oxygen"
    }
]
class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Python Quiz Game")
        self.master.geometry("600x400")
        self.score = 0
        self.q_index = 0
        random.shuffle(questions)
        self.current_question = None

        self.question_label = tk.Label(master, text="", font=("Arial", 16), wraplength=500, justify="center")
        self.question_label.pack(pady=20)

        self.options = []
        for i in range(4):
            btn = tk.Button(master, text="", width=40, height=2, font=("Arial", 12), command=lambda i=i: self.check_answer(i))
            btn.pack(pady=5)
            self.options.append(btn)

        self.status_label = tk.Label(master, text=f"Score: {self.score}", font=("Arial", 14))
        self.status_label.pack(pady=20)

        self.next_question()
        def next_question(self):
        if self.q_index < len(questions):
            self.current_question = questions[self.q_index]
            self.question_label.config(text=self.current_question["question"])
            shuffled_options = self.current_question["options"][:]
            random.shuffle(shuffled_options)
            for i, option in enumerate(shuffled_options):
                self.options[i].config(text=option)
            self.q_index += 1
        else:
            messagebox.showinfo("Quiz Completed", f"Your final score is: {self.score}/{len(questions)}")
            self.master.quit()

        def check_answer(self, index):
        selected = self.options[index].cget("text")
        correct = self.current_question["answer"]
        if selected == correct:
            self.score += 1
            messagebox.showinfo("Correct!", "You got it right!")
        else:
            messagebox.showerror("Wrong!", f"The correct answer was: {correct}")
        self.status_label.config(text=f"Score: {self.score}")
        self.next_question()
if __name__ == '__main__':
    root = tk.Tk()
    app = QuizApp(root)
     root.mainloop()