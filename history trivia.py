import tkinter as tk
from tkinter import messagebox
import requests
import random
import html
from PIL import Image, ImageTk
import pygame

# ------------------------------
# HOVER COLORS 
# ------------------------------
BTN_BG = "#E6C79A"
BTN_HOVER = "#D4AF37"
BTN_FG = "#2B1B0E"

# -------------------------------
# QUIZ CLASS (OOP)
# -------------------------------
class TriviaQuiz:
    def __init__(self, root, category=23, num_questions=10):
        self.root = root
        self.root.title("History Trivia Quiz")
        self.root.geometry("720x480")
        self.root.resizable(False, False)

        self.category = category  # Open Trivia API category (History)
        self.num_questions = num_questions
        self.current_question = 0
        self.score = 0
        self.questions = []

        pygame.init()
        pygame.mixer.init()

        # Wrong or Correct sound effects
        self.correct_sound = pygame.mixer.Sound("correct.wav")
        self.wrong_sound = pygame.mixer.Sound("wrong.wav")

        self.correct_sound.set_volume(0.6)
        self.wrong_sound.set_volume(0.15)

        self.create_difficulty_selection()

    # hover effects
    def add_hover(self, button, hover_bg, normal_bg):
        button.bind("<Enter>", lambda e: button.config(bg=hover_bg))
        button.bind("<Leave>", lambda e: button.config(bg=normal_bg))

    # Main Menu Music
    def play_menu_music(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load("work_music.wav")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
    
    #Stops after main menu
    def stop_music(self):
        pygame.mixer.music.stop()

    # -------------------------------
    # DIFFICULTY SELECTION SCREEN
    # -------------------------------
    def create_difficulty_selection(self):
        self.stop_music()
        self.play_menu_music()
        self.clear_root()

        # Background Image
        bg_image = Image.open("wp2244210.jpg")
        bg_image = bg_image.resize((720, 480))
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title
        tk.Label(
            self.root,
            text="📜 History Trivia Quiz 🪶",
            font=("Old English Text MT", 30),
            fg="#755C00",
            bg="#E6C79A"
        ).pack(pady=20)

        # Select Difficulty buttons
        tk.Label(
            self.root,
            text="Select Difficulty:",
            font=("Arial", 15, "bold"),
            fg="#2B1B0E",
            bg="#E6C79A"
        ).pack(pady=30)

        for text, diff in [("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard")]:
            btn = tk.Button(
                self.root,
                text=text,
                width=20, 
                fg=BTN_FG, 
                bg=BTN_BG, 
                activebackground=BTN_HOVER, 
                command=lambda d=diff: self.start_quiz(d)
            )
            btn.pack(pady=5)
            self.add_hover(btn, BTN_HOVER, BTN_BG)
        
        # Exit button
        exit_btn = tk.Button(
            self.root,
            text="Exit",
            width=20,
            fg=BTN_FG,
            bg=BTN_BG,
            activebackground=BTN_HOVER,
            command=self.root.destroy
        )
        exit_btn.pack(pady=30)
        self.add_hover(exit_btn, BTN_HOVER, BTN_BG)

    # -------------------------------
    # FETCH QUESTIONS FROM API
    # -------------------------------
    def fetch_questions(self, difficulty):
        api_url = f"https://opentdb.com/api.php?amount=10&category={self.category}&type=multiple&difficulty={difficulty}"
        response = requests.get(api_url)3
        data = response.json()

        if data["response_code"] != 0:
            messagebox.showerror("Error", "Failed to fetch trivia questions")
            self.root.destroy()
            return []

        # Randomly select num_questions from API results
        return random.sample(data["results"], k=min(self.num_questions, len(data["results"])))

    # -------------------------------
    # START QUIZ
    # -------------------------------
    def start_quiz(self, difficulty):
        self.stop_music()
        self.questions = self.fetch_questions(difficulty)
        self.current_question = 0
        self.score = 0
        self.create_quiz_widgets()
        self.show_question()

    # -------------------------------
    # CREATE QUIZ GUI
    # -------------------------------
    def create_quiz_widgets(self):
        self.clear_root()
        
        #Background Image
        bg_image = Image.open("wp2244210.jpg")
        bg_image = bg_image.resize((720, 480))
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title
        self.title_label = tk.Label(
            self.root,
            text="📜 History Trivia Quiz 🪶",
            font=("Old English Text MT", 30),
            fg = "#755C00", 
            bg="#E6C79A"
        )
        self.title_label.pack(pady=10)

        # Display question
        self.question_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 15, "bold"),
            wraplength=550, 
            fg = "#2B1B0E", 
            bg="#E6C79A"
        )
        self.question_label.pack(pady=20)

        # Display choices buttons 
        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(
                self.root,
                text="",
                width=50,
                fg=BTN_FG,
                bg=BTN_BG,
                command=lambda idx=i: self.check_answer(idx),
            )
            btn.pack(pady=5)
            self.add_hover(btn, BTN_HOVER, BTN_BG)
            self.option_buttons.append(btn)

        # Display current score 
        self.score_label = tk.Label(self.root, fg = "#2B1B0E", bg="#E6C79A", text=f"Score: {self.score}")
        self.score_label.pack(pady=10)

    # -------------------------------
    # SHOW QUESTION
    # -------------------------------
    def show_question(self):
        if self.current_question < len(self.questions):
            q = self.questions[self.current_question]
            question_text = html.unescape(q["question"])
            self.question_label.config(
                text=f"Q{self.current_question + 1}: {question_text}"
            )

            options = q["incorrect_answers"] + [q["correct_answer"]]
            options = [html.unescape(opt) for opt in options]
            random.shuffle(options)

            for i in range(4):
                self.option_buttons[i].config(text=options[i])
        else:
            self.show_final_score()

    # -------------------------------
    # CHECK ANSWER
    # -------------------------------
    def check_answer(self, idx):
        q = self.questions[self.current_question]
        correct_answer = html.unescape(q["correct_answer"])
        selected = self.option_buttons[idx]["text"]

        if selected == correct_answer:
            self.score += 1
            self.correct_sound.play()
            self.show_feedback(True, correct_answer)
        else:
            self.wrong_sound.play()
            self.show_feedback(False, correct_answer)

        self.score_label.config(text=f"Score: {self.score}")

    # -------------------------------
    # DISPLAY CORRECT ANSWER 
    # -------------------------------
    def show_feedback(self, is_correct, correct_answer):
        self.clear_root()

        # Background image 
        bg_image = Image.open("wp2244210.jpg")
        bg_image = bg_image.resize((720, 480))
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title 
        self.title_label = tk.Label(
            self.root,
            text="📜 History Trivia Quiz 🪶",
            font=("Old English Text MT", 30),
            fg = "#755C00", 
            bg="#E6C79A"
        )
        self.title_label.pack(pady=10)

        if is_correct:
            text = "CORRECT!"
            color = "#2E7D32"
        else: 
            text = "WRONG!"
            color = "#8B0000"

        # Display Correct or Wrong text
        tk.Label(
            self.root,
            text=text,
            font=("Old English Text MT", 20),
            fg=color,
            bg="#E6C79A"
        ).pack(pady=30)

        # Display correct answer
        if not is_correct:
            tk.Label(
                self.root,
                text=f"Correct Answer: {correct_answer}",
                font=("Arial", 12, "bold"),
                fg="#2B1B0E",
                bg="#E6C79A"
            ).pack(pady=30)

        # Continue button 
        continue_btn = tk.Button(
            self.root, 
            text="OK",
            width=15, 
            font=("Arial", 10, "bold"),
            fg=BTN_FG,
            bg=BTN_BG,
            activebackground=BTN_HOVER,
            command=self.next_question
        )
        continue_btn.pack(pady=30)

        self.add_hover(continue_btn, BTN_HOVER, BTN_BG)

    # ----- Continue to quiz -----
    def next_question(self):
        self.current_question += 1
        self.create_quiz_widgets()
        self.show_question()

    # -------------------------------
    # FINAL SCORE
    # -------------------------------
    def show_final_score(self):
        self.clear_root()

        # Background Image
        bg_image = Image.open("wp2244210.jpg")
        bg_image = bg_image.resize((720, 480))
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title
        tk.Label(
            self.root,
            text="📜 History Trivia Quiz 🪶",
            font=("Old English Text MT", 30),
            fg="#755C00",
            bg="#E6C79A"
        ).pack(pady=10)

        # Display Total score
        tk.Label(
            self.root,
            text=f"Your Score:\n{self.score} / {len(self.questions)}",
            font=("Arial", 15, "bold"),
            fg="#2B1B0E",
            bg="#E6C79A"
        ).pack(pady=30)

        # Play again button
        play_again_btn = tk.Button(
            self.root,
            text="Play Again",
            width=20,
            fg=BTN_FG,
            bg=BTN_BG,
            activebackground=BTN_HOVER,
            command=self.create_difficulty_selection
        )
        play_again_btn.pack(pady=10)
        self.add_hover(play_again_btn, BTN_HOVER, BTN_BG)

        # Exit button
        exit_btn = tk.Button(
            self.root,
            text="Exit",
            width=20,
            fg=BTN_FG,
            bg=BTN_BG,
            activebackground=BTN_HOVER,
            command=self.root.destroy
        )
        exit_btn.pack(pady=10)
        self.add_hover(exit_btn, BTN_HOVER, BTN_BG)

    # -------------------------------
    # HELPER TO CLEAR ROOT
    # -------------------------------
    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# -------------------------------
# MAIN PROGRAM
# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TriviaQuiz(root, category=23, num_questions=10)
    root.mainloop()