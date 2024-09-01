import random #here is imported the random module to allow the AI to make random choices

#this class defines a general player in the game
class Player:
    def __init__(self, letter):
        #here is initialized the player's letter, which can be either 'X' or 'O'
        self.letter = letter

    def get_move(self, game):
        #this method is a placeholder to be implemented by subclasses.
        #it represents how the player will choose their move during the game.
        pass

#this class defines a computer player that makes random moves on the board
class RandomComputerPlayer(Player):
    def __init__(self, letter):
        #here is called the constructor of the parent Player class to initialize the letter ('X' or 'O')
        super().__init__(letter)

    def get_move(self, game):
        #this method selects a move randomly from the available moves on the game board
        #game.available_moves() returns a list of all empty spots on the board
        square = random.choice(game.available_moves()) #here is selected one random move
        return square #here is returned the chosen move

#this class defines a smart computer player that uses the minimax algorithm to make optimal moves
class SmartComputerPlayer(Player):
    def __init__(self, letter):
        #here is called the constructor of the parent Player class to initialize the letter ('X' or 'O')
        super().__init__(letter)

    def get_move(self, game):
        #this method decides on the best move using the minimax algorithm, except for the first move
        if len(game.available_moves()) == 9:
            #if it's the first move of the game, choose a random square because all squares are equally good
            square = random.choice(game.available_moves())
        else:
            #otherwise, use the minimax algorithm to calculate the best possible move
            square = self.minimax(game, self.letter)['position']
        return square #here is returned the chosen move

    def minimax(self, state, player):
        #here is initialized the player that is trying to maximize the score, which is the smart computer itself
        max_player = self.letter
        #here is determined the opponent player, which is the player who isn't making the current move
        other_player = 'O' if player == 'X' else 'X'

        #this block of code checks if the previous move resulted in a win for the opponent
        if state.current_winner == other_player:
            #if the opponent has won, calculate the score based on how many empty squares are left
            #the fewer squares left, the better the win for the opponent (or worse for the AI)
            #the score is positive if the opponent wins and it's their turn; it's negative if it's the AI's turn
            return {
                'position': None, #no specific position is relevant since the game is over
                'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)
            }
        #this checks if the board is full and there is a tie
        elif not state.empty_squares():
            return {'position': None, 'score': 0} #a tie has a neutral score of 0

        #this block of code sets up variables to track the best possible move
        if player == max_player:
            #if the AI (maximizing player) is making the move, start with the lowest possible score
            best = {'position': None, 'score': -float('inf')}
        else:
            #if the opponent (minimizing player) is making the move, start with the highest possible score
            best = {'position': None, 'score': float('inf')}

        #this loop iterates over all possible moves the current player can make
        for possible_move in state.available_moves():
            #here is simulated the move by placing the player's letter in the chosen square
            state.make_move(possible_move, player)
            #here is called the minimax recursively to simulate the opponent's response to this move
            sim_score = self.minimax(state, other_player)

            #after simulating, reset the board to its original state (undo the move)
            state.board[possible_move] = ' '
            state.current_winner = None #clear the winner, since the move was undone
            sim_score['position'] = possible_move #record the position that was just tried

            #this block of code updates the best score based on whether the current player is maximizing or minimizing
            if player == max_player:
                #if the current player is the AI (maximizing player), choose the move with the highest score
                if sim_score['score'] > best['score']:
                    best = sim_score #update the best score to the higher score
            else:
                #if the current player is the opponent (minimizing player), choose the move with the lowest score
                if sim_score['score'] < best['score']:
                    best = sim_score #update the best score to the lower score
        #here is returned the best move found after considering all possibilities
        return best
