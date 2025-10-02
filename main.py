# main.py

import tkinter as tk
from tkinter import messagebox
from quiz_data import quizzes
import random

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App")
        self.root.geometry("500x400")
        self.quiz_data = {}
        self.current_question = 0
        self.score = 0
        self.selected_quiz = None
        self.user_answers = []

        self.create_home_screen()

    def create_home_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Welcome to the Quiz App", font=("Arial", 18)).pack(pady=20)

        for quiz_name in quizzes.keys():
            tk.Button(self.root, text=quiz_name, font=("Arial", 14),
                      command=lambda q=quiz_name: self.start_quiz(q)).pack(pady=5)

        tk.Button(self.root, text="Start Random Quiz", font=("Arial", 14),
                  command=self.start_random_quiz).pack(pady=10)

    def start_quiz(self, quiz_name):
        self.selected_quiz = quiz_name
        self.quiz_data = quizzes[quiz_name]
        self.current_question = 0
        self.score = 0
        self.user_answers = []
        self.show_question()

    def start_random_quiz(self):
        quiz_name = random.choice(list(quizzes.keys()))
        self.start_quiz(quiz_name)

    def show_question(self):
        self.clear_screen()

        question_data = self.quiz_data[self.current_question]
        question_text = question_data["question"]
        options = question_data["options"]

        tk.Label(self.root, text=f"Q{self.current_question + 1}: {question_text}",
                 font=("Arial", 14), wraplength=450).pack(pady=20)

        self.var = tk.StringVar()

        for option in options:
            tk.Radiobutton(self.root, text=option, variable=self.var, value=option,
                           font=("Arial", 12)).pack(anchor="w", padx=50)

        tk.Button(self.root, text="Submit Answer", font=("Arial", 12),
                  command=self.submit_answer).pack(pady=20)

    def submit_answer(self):
        selected = self.var.get()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an answer!")
            return

        correct_answer = self.quiz_data[self.current_question]["answer"]
        is_correct = selected == correct_answer
        self.user_answers.append((self.quiz_data[self.current_question]["question"], selected, correct_answer))

        if is_correct:
            self.score += 1
            messagebox.showinfo("Correct!", "🎉 Correct Answer!")
        else:
            messagebox.showerror("Wrong!", f"❌ Wrong Answer!\nCorrect: {correct_answer}")

        self.current_question += 1

        if self.current_question < len(self.quiz_data):
            self.show_question()
        else:
            self.show_result()

    def show_result(self):
        self.clear_screen()

        tk.Label(self.root, text="Quiz Completed!", font=("Arial", 18)).pack(pady=20)
        tk.Label(self.root, text=f"Your Score: {self.score} / {len(self.quiz_data)}",
                 font=("Arial", 14)).pack(pady=10)

        for idx, (q, user_ans, correct_ans) in enumerate(self.user_answers, start=1):
            color = "green" if user_ans == correct_ans else "red"
            result_text = f"{idx}. {q}\nYour Answer: {user_ans} | Correct: {correct_ans}"
            tk.Label(self.root, text=result_text, font=("Arial", 10), fg=color, wraplength=450, justify="left").pack(pady=2)

        tk.Button(self.root, text="Back to Home", font=("Arial", 12), command=self.create_home_screen).pack(pady=20)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()