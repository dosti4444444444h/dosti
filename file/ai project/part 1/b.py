import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import pandas as pd

# Initialize scores and round counter
player_one_score = 0
player_two_score = 0
round_count = 0

# Initialize win counts for overall games
player_one_wins = 0
player_two_wins = 0

# Excel file for logging
EXCEL_FILE = 'game_data.xlsx'

class Player:
    def __init__(self, name):
        self.name = name
        self.choices = []
        self.shield = False

    def make_choice(self, choice):
        self.choices.append(choice)
        return choice

class Computer(Player):
    def __init__(self, name):
        super().__init__(name)
    
    def make_choice(self):
        if len(player_one.choices) < 3:
            choice = random.choice(["rock", "paper", "scissors"])
        else:
            choice = self.predict_choice()
        self.choices.append(choice)
        return choice
    
    def predict_choice(self):
        percentages = calculate_percentages()
        highest = max(percentages, key=percentages.get)
        if highest == 'rock':
            return 'paper'
        elif highest == 'paper':
            return 'scissors'
        else:
            return 'rock'

def determine_winner(player_one_choice, player_two_choice):
    global player_one_score, player_two_score
    if player_one_choice == player_two_choice:
        return "It's a tie!"
    elif (player_one_choice == "rock" and player_two_choice == "scissors") or \
         (player_one_choice == "scissors" and player_two_choice == "paper") or \
         (player_one_choice == "paper" and player_two_choice == "rock"):
        player_one_score += 1
        return "Player One"
    else:
        player_two_score += 1
        return "Player Two"

def play_with_image(player_one_choice):
    global player_one_score, player_two_score, round_count
    round_count += 1
    player_one.make_choice(player_one_choice)
    player_two_choice = player_two.make_choice()
    winner = determine_winner(player_one_choice, player_two_choice)
    
    result_text = f"Player Two chose: {player_two_choice}\n{winner} wins!"
    
    result_label.config(text=result_text)
    score_label.config(text=f"Player One Score: {player_one_score} | Player Two Score: {player_two_score}")
    
    log_to_excel(round_count, player_one_choice, player_two_choice, winner)

    if round_count == 5:
        # Update overall wins
        global player_one_wins, player_two_wins
        if player_one_score > player_two_score:
            player_one_wins += 1
            final_result = "Player One is the overall winner!"
        elif player_two_score > player_one_score:
            player_two_wins += 1
            final_result = "Player Two is the overall winner!"
        else:
            final_result = "It's a tie overall!"
        
        messagebox.showinfo("Game Over", final_result)
        show_overall_wins()
        reset_game()

def show_overall_wins():
    overall_wins_text = f"Overall Wins:\nPlayer One: {player_one_wins}\nPlayer Two: {player_two_wins}"
    messagebox.showinfo("Overall Wins", overall_wins_text)

def reset_game():
    global player_one_score, player_two_score, round_count
    player_one_score = 0
    player_two_score = 0
    round_count = 0
    player_one.choices.clear()
    player_two.choices.clear()
    player_one.shield = False
    player_two.shield = False
    result_label.config(text="")
    score_label.config(text=f"Player One Score: {player_one_score} | Player Two Score: {player_two_score}")

def log_to_excel(round_num, user_choice, computer_choice, result):
    try:
        df = pd.read_excel(EXCEL_FILE, engine='openpyxl')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Round', 'UserChoice', 'ComputerChoice', 'Result'])
    
    new_data = {
        'Round': round_num,
        'UserChoice': user_choice,
        'ComputerChoice': computer_choice,
        'Result': result
    }
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')

def calculate_percentages():
    try:
        df = pd.read_excel(EXCEL_FILE, engine='openpyxl')
    except FileNotFoundError:
        return {'rock': 0, 'paper': 0, 'scissors': 0}
    
    if df.empty:
        return {'rock': 0, 'paper': 0, 'scissors': 0}
    
    total = len(df)
    percentages = {
        'rock': len(df[df['UserChoice'] == 'rock']) / total * 100,
        'paper': len(df[df['UserChoice'] == 'paper']) / total * 100,
        'scissors': len(df[df['UserChoice'] == 'scissors']) / total * 100
    }
    return percentages

# Create the main window
root = tk.Tk()
root.title("Rock, Paper, Scissors")

# Load hand images
rock_img = Image.open("rock.png").resize((100, 100), Image.LANCZOS)
paper_img = Image.open("paper.png").resize((100, 100), Image.LANCZOS)
scissors_img = Image.open("scissors.png").resize((100, 100), Image.LANCZOS)

# Convert images to Tkinter-compatible objects
rock_icon = ImageTk.PhotoImage(rock_img)
paper_icon = ImageTk.PhotoImage(paper_img)
scissors_icon = ImageTk.PhotoImage(scissors_img)

# Create and place the image buttons using a grid layout
buttons_frame = tk.Frame(root, padx=10, pady=10)
buttons_frame.pack()

rock_button = tk.Button(buttons_frame, image=rock_icon, command=lambda: play_with_image("rock"))
rock_button.grid(row=0, column=0, padx=10, pady=10)

paper_button = tk.Button(buttons_frame, image=paper_icon, command=lambda: play_with_image("paper"))
paper_button.grid(row=0, column=1, padx=10, pady=10)

scissors_button = tk.Button(buttons_frame, image=scissors_icon, command=lambda: play_with_image("scissors"))
scissors_button.grid(row=0, column=2, padx=10, pady=10)

# Create and place the result label
result_label = tk.Label(root, text="", height=4, width=30)
result_label.pack()

# Create and place the score label
score_label = tk.Label(root, text=f"Player One Score: {player_one_score} | Player Two Score: {player_two_score}", font=("Helvetica", 12))
score_label.pack()

# Initialize players
player_one = Player("Player One")
player_two = Computer("Player Two")

# Start the GUI event loop
root.mainloop()

