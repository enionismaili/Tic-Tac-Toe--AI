import tkinter as tk #here the Tkinter library is imported to create the graphical user interface (GUI)
from tkinter import messagebox, simpledialog #here specific modules from Tkinter are imported for message and input dialogs
import random #here the random module is imported to allow for random choice selections
from player import SmartComputerPlayer, RandomComputerPlayer #here the AI player classes are imported from player.py

#this class defines the main Tic Tac Toe game with a graphical interface
class TicTacToeGUI:
    def __init__(self, root):
        #here the main window title is set, and the background color is configured
        self.root = root
        self.root.title("Advanced Tic Tac Toe")
        self.root.configure(bg="#333") #sets a dark background color

        #here a 3x3 grid of buttons is created to represent the Tic Tac Toe board; initially, all buttons are set to None
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.human_player = None #here the variable for the human player's letter ('X' or 'O') is initialized as None
        self.ai_player = None #here the variable for the AI player's letter ('X' or 'O') is initialized as None
        self.current_player = None #here the variable that tracks whose turn it is is initialized as None
        self.ai_strategy = None #here the variable for the AI strategy (smart or random) is initialized as None
        self.board = [' ' for _ in range(9)] #here a list representing the game board is created, initially empty spaces
        self.current_winner = None #here the variable to track the current winner is initialized as None
        self.human_score = 0 #here the score counter for the human player is initialized to 0
        self.ai_score = 0 #here the score counter for the AI player is initialized to 0
        self.ties = 0 #here the counter for the number of ties in the game is initialized to 0

        #this method is called to ask the player to choose their letter and select the AI strategy
        self.choose_letter_and_strategy()

    def choose_letter_and_strategy(self):
        #this loop prompts the player to choose their letter ('X' or 'O') until a valid choice is made
        while True:
            choice = simpledialog.askstring("Choose Letter", "Do you want to be X or O?", parent=self.root)
            if choice is None:
                self.root.quit() #exit the game if the player closes the dialog without making a choice
                return
            choice = choice.upper() #convert the choice to uppercase to standardize the input
            if choice == 'X':
                self.human_player = "X" #assign the human player as 'X'
                self.ai_player = "O" #assign the AI player as 'O'
                break #exit the loop once a valid choice is made
            elif choice == 'O':
                self.human_player = "O" #assign the human player as 'O'
                self.ai_player = "X" #assign the AI player as 'X'
                break #exit the loop once a valid choice is made
            else:
                #show an error message if the input is invalid (not 'X' or 'O')
                messagebox.showerror("Invalid Choice", "Please choose either 'X' or 'O'.")

        #thisloop prompts the player to choose the AI strategy (Smart AI or Random AI) until a valid choice is made
        while True:
            strategy_choice = simpledialog.askstring("Choose AI Strategy", "Do you want to play against a (1) Smart AI or (2) Random AI?", parent=self.root)
            if strategy_choice is None:
                self.root.quit() #exit the game if the player closes the dialog without choosing a strategy
                return
            if strategy_choice == '1':
                self.ai_strategy = SmartComputerPlayer(self.ai_player) #assign the AI to use the smart strategy
                break #exit the loop once a valid strategy is chosen
            elif strategy_choice == '2':
                self.ai_strategy = RandomComputerPlayer(self.ai_player) #assign the AI to use the random strategy
                break #exit the loop once a valid strategy is chosen
            else:
                #2show an error message if the input is invalid (not '1' or '2')
                messagebox.showerror("Invalid Choice", "Please choose either '1' or '2'.")

        # here a random selection is made to determine who goes first, the human player or the AI
        self.current_player = random.choice([self.human_player, self.ai_player])
        self.create_widgets() #this method sets up the game board UI elements (buttons and labels)
        self.create_menu() #this method sets up the game menu with options like starting a new game or exiting

        #if the AI is selected to go first, the AI's move is triggered after a short delay
        if self.current_player == self.ai_player:
            self.info_label.config(text="AI's Turn") #update the label to inform the player it's the AI's turn
            self.root.after(500, self.ai_move) #wait 500 milliseconds before the AI makes a move
        else:
            self.info_label.config(text="Your Turn") #update the label to inform the player it's their turn

    def create_widgets(self):
        #this method creates and configures the main label that displays whose turn it is
        self.info_label = tk.Label(self.root, text=f"{self.current_player}'s Turn!", font="Arial 16 bold", bg="#333", fg="white")
        self.info_label.grid(row=0, column=0, columnspan=3) #position the label at the top, spanning across three columns

        #this loop creates a 3x3 grid of buttons that represent the Tic Tac Toe board, which players will click to make moves
        for i in range(3):
            for j in range(3):
                #create each button with a default empty text, configure the style, and assign the click event handler
                self.buttons[i][j] = tk.Button(self.root, text=" ", font="Arial 24 bold", width=5, height=2,
                                               bg="#eee", fg="#333",
                                               command=lambda row=i, col=j: self.button_click(row, col))
                self.buttons[i][j].grid(row=i+1, column=j, padx=5, pady=5) #position each button in the grid

        #this label is created to display the scores (human player, AI, and ties) and is positioned below the board
        self.score_label = tk.Label(self.root, text=f"Score - You: {self.human_score} AI: {self.ai_score} Ties: {self.ties}", 
                                    font="Arial 12", bg="#333", fg="white")
        self.score_label.grid(row=4, column=0, columnspan=3) #position the score label below the grid, spanning three columns

    def create_menu(self):
        #this method creates the menu bar that appears at the top of the window with options for the game
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar) #set the menu bar to the root window

        #here the 'Game' menu is created with options for starting a new game or exiting the game
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New Game", command=self.reset_board) #add an option to start a new game
        game_menu.add_separator() #add a separator line in the menu
        game_menu.add_command(label="Exit", command=self.root.quit) #add an option to exit the game

    def button_click(self, row, col):
        #this method is called when a player clicks a button (makes a move)
        if self.buttons[row][col]["text"] == " " and self.current_winner is None: #check if the button is empty and the game is not yet won
            self.make_move(row * 3 + col, self.human_player) #update the board with the human player's move
            self.buttons[row][col]["text"] = self.human_player #update the button's text to show the player's move
            self.buttons[row][col]["bg"] = "#4CAF50" #change the button's background color to indicate it's taken

            if self.check_winner(self.human_player): #check if the human player has won the game
                self.human_score += 1 #increment the human player's score
                self.end_game(f"You win!") #call the method to handle the end of the game with a winning message
            elif not self.empty_squares(): #check if the board is full, indicating a tie
                self.ties += 1 #increment the tie count
                self.end_game("It's a tie!") #call the method to handle the end of the game with a tie message
            else:
                #if the game is still ongoing, switch to the AI's turn
                self.current_player = self.ai_player
                self.info_label.config(text="AI's Turn") #update the label to inform the player it's the AI's turn
                self.root.after(500, self.ai_move) #trigger the AI's move after a short delay of 500 milliseconds

    def ai_move(self):
        #this method handles the AI's move
        if self.current_winner is None and self.current_player == self.ai_player: #ensure the game is not yet won and it's the AI's turn
            move = self.ai_strategy.get_move(self) #get the AI's move using the selected strategy (smart or random)
        
            if self.make_move(move, self.ai_player): #update the board with the AI's move
                row, col = divmod(move, 3) #convert the move index to row and column
                self.buttons[row][col]["text"] = self.ai_player #update the button's text to show the AI's move
                self.buttons[row][col]["bg"] = "#F44336" #change the button's background color to indicate it's taken by AI
                self.buttons[row][col].config(state="disabled") #disable the button to prevent further clicks

                if self.check_winner(self.ai_player): #check if the AI has won the game
                    self.ai_score += 1 #increment the AI's score
                    self.end_game(f"AI wins!") #call the method to handle the end of the game with a winning message
                elif not self.empty_squares(): #check if the board is full, indicating a tie
                    self.ties += 1 #increment the tie count
                    self.end_game("It's a tie!") #call the method to handle the end of the game with a tie message
                else:
                    #if the game is still ongoing, switch back to the human player's turn
                    self.current_player = self.human_player
                    self.info_label.config(text="Your Turn!") #update the label to inform the player it's their turn

    def make_move(self, square, letter):
        #this method updates the board with the player's or AI's move
        if self.board[square] == ' ':
            self.board[square] = letter #place the player's letter ('X' or 'O') on the board at the specified square
            if self.check_winner(letter): #check if this move results in a win
                self.current_winner = letter #set the current winner to the player who made the move
            return True #return True indicating the move was successful
        return False #return False if the move was invalid (e.g., the square was already taken)

    def available_moves(self):
        #this method returns a list of available moves (empty squares) on the board
        return [i for i, spot in enumerate(self.board) if spot == ' ']  # return the indices of empty spots

    def check_winner(self, letter):
        #this method checks all possible winning combinations on the board
        #check all rows to see if any of them have the same letter (i.e., all 'X' or all 'O')
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            if all([s == letter for s in row]):
                return True
        #check all columns to see if any of them have the same letter
        for col in [[self.board[i+j*3] for j in range(3)] for i in range(3)]:
            if all([s == letter for s in col]):
                return True
            
        #check the main diagonal (positions 0, 4, 8) to see if all three positions have the same letter
        check_main_diagonal = all([self.board[i] == letter for i in [0, 4, 8]])
        #check the anti-diagonal (positions 2, 4, 6) to see if all three positions have the same letter
        check_anti_diagonal = all([self.board[i] == letter for i in [2, 4, 6]])
        #if either diagonal check is True, return True indicating a win on a diagonal
        if check_main_diagonal or check_anti_diagonal:
            return True
        #return False if there is no winner on any diagonal
        return False


    def empty_squares(self):
        #this method checks if there are any empty squares left on the board
        return ' ' in self.board #return True if there is at least one empty square, otherwise False

    def num_empty_squares(self):
        #this method returns the number of empty squares remaining on the board
        return self.board.count(' ') #count and return the number of empty spaces

    def reset_board(self):
        #this method resets the board to start a new game
        self.board = [' ' for _ in range(9)] #clear the board by resetting all squares to empty
        self.current_winner = None #reset the current winner to None
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["text"] = " " #clear the text on each button
                self.buttons[i][j]["bg"] = "#eee" #reset the button background color to the default
                self.buttons[i][j].config(state="normal") #enable all buttons for the new game

        self.choose_letter_and_strategy() #prompt the player to choose a letter and AI strategy again

        if self.current_player == self.ai_player:
            self.root.after(500, self.ai_move) #if the AI is selected to start, trigger its move after a short delay

    def end_game(self, message):
        # this method handles the end of the game
        self.info_label.config(text=message) #display the result of the game (win, loss, or tie)
        #update the score label to reflect the latest scores and ties
        self.score_label.config(text=f"Score - You: {self.human_score} AI: {self.ai_score} Ties: {self.ties}")
        #disable all buttons on the board to prevent further moves after the game ends
        for row in self.buttons:
            for button in row:
                button.config(state="disabled")
        #reset the board after a delay of 2 seconds to allow the player to see the result
        self.root.after(2000, self.reset_board)

#this is the main code to start the game
if __name__ == '__main__':
    root = tk.Tk() #here the main window is created using Tkinter
    game = TicTacToeGUI(root) #here an instance of the TicTacToeGUI class is created, passing the main window
    root.mainloop() #here the Tkinter event loop is started, which keeps the window open and responsive
