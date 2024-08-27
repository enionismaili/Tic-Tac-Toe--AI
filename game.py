import tkinter as tk
from tkinter import messagebox, simpledialog
import random
from player import SmartComputerPlayer, RandomComputerPlayer

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Tic Tac Toe")
        self.root.configure(bg="#333")

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.human_player = None
        self.ai_player = None
        self.current_player = None
        self.ai_strategy = None
        self.board = [' ' for _ in range(9)]
        self.current_winner = None
        self.human_score = 0
        self.ai_score = 0
        self.ties = 0

        self.choose_letter_and_strategy()

    def choose_letter_and_strategy(self):
        while True:
            choice = simpledialog.askstring("Choose Letter", "Do you want to be X or O?", parent=self.root)
            if choice is None:
                self.root.quit()  # Exit if the user closes the dialog
                return
            choice = choice.upper()
            if choice == 'X':
                self.human_player = "X"
                self.ai_player = "O"
                break
            elif choice == 'O':
                self.human_player = "O"
                self.ai_player = "X"
                break
            else:
                messagebox.showerror("Invalid Choice", "Please choose either 'X' or 'O'.")

        while True:
            strategy_choice = simpledialog.askstring("Choose AI Strategy", "Do you want to play against a (1) Smart AI or (2) Random AI?", parent=self.root)
            if strategy_choice is None:
                self.root.quit()  # Exit if the user closes the dialog
                return
            if strategy_choice == '1':
                self.ai_strategy = SmartComputerPlayer(self.ai_player)
                break
            elif strategy_choice == '2':
                self.ai_strategy = RandomComputerPlayer(self.ai_player)
                break
            else:
                messagebox.showerror("Invalid Choice", "Please choose either '1' or '2'.")

        self.current_player = random.choice([self.human_player, self.ai_player])
        self.create_widgets()
        self.create_menu()

        if self.current_player == self.ai_player:
            self.info_label.config(text="AI's Turn")
            self.root.after(500, self.ai_move)
        else:
            self.info_label.config(text="Your Turn")

    def create_widgets(self):
        self.info_label = tk.Label(self.root, text=f"{self.current_player}'s Turn!", font="Arial 16 bold", bg="#333", fg="white")
        self.info_label.grid(row=0, column=0, columnspan=3)

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.root, text=" ", font="Arial 24 bold", width=5, height=2,
                                               bg="#eee", fg="#333",
                                               command=lambda row=i, col=j: self.button_click(row, col))
                self.buttons[i][j].grid(row=i+1, column=j, padx=5, pady=5)

        self.score_label = tk.Label(self.root, text=f"Score - You: {self.human_score} AI: {self.ai_score} Ties: {self.ties}", 
                                    font="Arial 12", bg="#333", fg="white")
        self.score_label.grid(row=4, column=0, columnspan=3)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New Game", command=self.reset_board)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.quit)

    def button_click(self, row, col):
        if self.buttons[row][col]["text"] == " " and self.current_winner is None:
            self.make_move(row * 3 + col, self.human_player)
            self.buttons[row][col]["text"] = self.human_player
            self.buttons[row][col]["bg"] = "#4CAF50"

            if self.check_winner(self.human_player):
                self.human_score += 1
                self.end_game(f"You win!")
            elif not self.empty_squares():
                self.ties += 1
                self.end_game("It's a tie!")
            else:
                self.current_player = self.ai_player
                self.info_label.config(text="AI's Turn")
                self.root.after(500, self.ai_move)

    def ai_move(self):
        if self.current_winner is None and self.current_player == self.ai_player:
            move = self.ai_strategy.get_move(self)
        
            if self.make_move(move, self.ai_player):
                row, col = divmod(move, 3)
                self.buttons[row][col]["text"] = self.ai_player
                self.buttons[row][col]["bg"] = "#F44336"
                self.buttons[row][col].config(state="disabled")  

                if self.check_winner(self.ai_player):
                    self.ai_score += 1
                    self.end_game(f"AI wins!")
                elif not self.empty_squares():
                    self.ties += 1
                    self.endv_game("It's a tie!")
                else:
                    self.current_player = self.human_player
                    self.info_label.config(text="Your Turn!")



    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.check_winner(letter):
                self.current_winner = letter
            return True
        return False

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def check_winner(self, letter):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            if all([s == letter for s in row]):
                return True
        for col in [[self.board[i+j*3] for j in range(3)] for i in range(3)]:
            if all([s == letter for s in col]):
                return True
        if all([self.board[i] == letter for i in [0, 4, 8]]) or \
           all([self.board[i] == letter for i in [2, 4, 6]]):
            return True
        return False

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def reset_board(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["text"] = " "
                self.buttons[i][j]["bg"] = "#eee"
                self.buttons[i][j].config(state="normal")

        self.choose_letter_and_strategy()

        if self.current_player == self.ai_player:
            self.root.after(500, self.ai_move)

    def end_game(self, message):
        self.info_label.config(text=message)
        self.score_label.config(text=f"Score - You: {self.human_score} AI: {self.ai_score} Ties: {self.ties}")
        for row in self.buttons:
            for button in row:
                button.config(state="disabled")
        self.root.after(2000, self.reset_board)

if __name__ == '__main__':
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()
