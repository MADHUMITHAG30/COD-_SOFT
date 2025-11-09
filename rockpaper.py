
import tkinter as tk
from tkinter import ttk, messagebox
import random

class RockPaperScissorsGame:
    def __init__(self, root):  # ✅ fixed double underscores
        self.root = root
        self.root.title("Rock Paper Scissors")
        self.root.geometry("600x600")
        self.root.configure(bg='#2c3e50')
        
        # Game variables
        self.user_score = 0
        self.computer_score = 0
        self.choices = ["Rock", "Paper", "Scissors"]
        
        # Custom styles
        self.style = ttk.Style()
        self.style.configure('Game.TButton', font=('Arial', 14), padding=15)
        
        # Create UI
        self.create_widgets()
    
    def create_widgets(self):
        # Header frame
        header_frame = tk.Frame(self.root, bg='#e74c3c', height=100)
        header_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(header_frame, text="Rock Paper Scissors", 
                 font=('Arial', 24, 'bold'), bg='#e74c3c', fg='white').pack(pady=20)
        
        # Score display
        score_frame = tk.Frame(self.root, bg='#2c3e50')
        score_frame.pack(pady=10)
        
        tk.Label(score_frame, text="Your Score:", font=('Arial', 14), 
                 bg='#2c3e50', fg='#ecf0f1').grid(row=0, column=0, padx=10)
        self.user_score_label = tk.Label(score_frame, text="0", font=('Arial', 16, 'bold'), 
                                         bg='#2c3e50', fg='#2ecc71')
        self.user_score_label.grid(row=0, column=1, padx=10)
        
        tk.Label(score_frame, text="Computer Score:", font=('Arial', 14), 
                 bg='#2c3e50', fg='#ecf0f1').grid(row=0, column=2, padx=10)
        self.computer_score_label = tk.Label(score_frame, text="0", font=('Arial', 16, 'bold'), 
                                             bg='#2c3e50', fg='#e74c3c')
        self.computer_score_label.grid(row=0, column=3, padx=10)
        
        # Game buttons
        button_frame = tk.Frame(self.root, bg='#2c3e50')
        button_frame.pack(pady=20)
        
        button_colors = {
            "Rock": "#3498db",
            "Paper": "#f39c12",
            "Scissors": "#9b59b6"
        }
        
        for i, choice in enumerate(self.choices):
            btn = ttk.Button(button_frame, text=choice, style='Game.TButton',
                             command=lambda c=choice: self.play_round(c))
            btn.grid(row=0, column=i, padx=10)
            self.style.configure(f'{choice}.TButton', background=button_colors[choice])
            btn['style'] = f'{choice}.TButton'
        
        # Result display
        result_frame = tk.Frame(self.root, bg='#34495e', bd=2, relief='groove')
        result_frame.pack(pady=20, padx=30, fill='both', expand=True)
        
        tk.Label(result_frame, text="Your Choice:", font=('Arial', 12), 
                 bg='#34495e', fg='#bdc3c7').pack(pady=(10, 0))
        self.user_choice_label = tk.Label(result_frame, text="", font=('Arial', 14, 'bold'), 
                                          bg='#34495e', fg='#2ecc71')
        self.user_choice_label.pack()
        
        tk.Label(result_frame, text="Computer's Choice:", font=('Arial', 12), 
                 bg='#34495e', fg='#bdc3c7').pack(pady=(10, 0))
        self.computer_choice_label = tk.Label(result_frame, text="", font=('Arial', 14, 'bold'), 
                                              bg='#34495e', fg='#e74c3c')
        self.computer_choice_label.pack()
        
        self.result_label = tk.Label(result_frame, text="", font=('Arial', 18, 'bold'), 
                                     bg='#34495e', fg='#f1c40f')
        self.result_label.pack(pady=20)
        
        # Reset button
        reset_btn = ttk.Button(self.root, text="Reset Game", command=self.reset_game)
        reset_btn.pack(pady=10)
    
    def play_round(self, user_choice):
        computer_choice = random.choice(self.choices)
        
        # Update display
        self.user_choice_label.config(text=user_choice)
        self.computer_choice_label.config(text=computer_choice)
        
        # Determine winner
        if user_choice == computer_choice:
            result = "It's a Tie!"
            color = '#f1c40f'
        elif (user_choice == "Rock" and computer_choice == "Scissors") or \
             (user_choice == "Paper" and computer_choice == "Rock") or \
             (user_choice == "Scissors" and computer_choice == "Paper"):
            result = "You Win!"
            color = '#2ecc71'
            self.user_score += 1
        else:
            result = "Computer Wins!"
            color = '#e74c3c'
            self.computer_score += 1
        
        # Update UI
        self.result_label.config(text=result, fg=color)
        self.user_score_label.config(text=str(self.user_score))
        self.computer_score_label.config(text=str(self.computer_score))
    
    def reset_game(self):
        self.user_score = 0
        self.computer_score = 0
        self.user_score_label.config(text="0")
        self.computer_score_label.config(text="0")
        self.user_choice_label.config(text="")
        self.computer_choice_label.config(text="")
        self.result_label.config(text="")

def main():
    root = tk.Tk()
    game = RockPaperScissorsGame(root)
    root.mainloop()

if __name__ == "__main__":  # ✅ fixed double underscores
    main()
