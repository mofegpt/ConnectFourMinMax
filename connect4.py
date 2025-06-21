import numpy as np


class ConnectFour:
    def __init__(self):
        self.rows = 6
        self.cols = 5
        # Creates board with empty spaces as .
        self.board = np.full((self.rows, self.cols), ".", dtype=str)  

     # Print the board for UI
    def print_board(self):
        print("\n".join([" ".join(row) for row in self.board[::-1]]))  # Print board top-down
        print("\n")

    # Drop a piece in the selected column
    def drop_piece(self, col, player):
        symbol = "X" if player == 1 else "O"  # Human = "X", AI = "O"
        for row in range(self.rows):
            if self.board[row][col] == ".":
                self.board[row][col] = symbol
                return True
        return False  # Column is full

    # Undo move to test another move
    def undo_move(self, col):
        for row in reversed(range(self.rows)):
            if self.board[row][col] != ".":
                self.board[row][col] = "."
                return

    # Checks if board is full
    def is_full(self):
        return all(self.board[5, :] != ".")

    # Checks winner of board
    def check_winner(self):
        directions = [(0,1), (1,0), (1,1), (1,-1)]  # Right, Down, Down Diagonal \, Up Diagonal /
        
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == ".":
                    continue
                player = self.board[row][col]
                for dr, dc in directions:
                    count = 1  # Current position counts
                    for i in range(1, 4):
                        r, c = row + dr * i, col + dc * i
                        if 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] == player:
                            count += 1
                        else:
                            break  # Stop if out of bounds or mismatch
                    
                    if count == 4:
                        return player  # Return "X" for Human, "O" for AI
        
        return "." 

    # Evaluates board at a current state
    def evaluate_board(self):
        ai_score = 0
        human_score = 0

        center_col = self.cols // 2  # Middle column index

        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.board[row][col]
                if cell == "O":  # AI piece
                    ai_score += self.count_winning_combinations(row, col)
                    if col == center_col:
                        ai_score += 3  # Bonus for occupying the center
                elif cell == "X":  # Human piece
                    human_score += self.count_winning_combinations(row, col)
                    if col == center_col:
                        human_score += 3 

        return ai_score - human_score

    # Counts potential winning paths at a position for SECOND ITERATION
    def count_winning_combinations(self, row, col):
        total = 0
        directions = [(0,1), (1,0), (1,1), (1,-1)]  # Horizontal, Vertical, Diagonal \, Diagonal /
        
        for dr, dc in directions:
            count = 1  # Include current piece
            for i in range(1, 4):  # Look 3 more steps ahead
                r, c = row + dr * i, col + dc * i
                if 0 <= r < self.rows and 0 <= c < self.cols:  # Stay in bounds
                    count += 1
                else:
                    break  # Stop if out of bounds

            # Gets here if its a combination of 4 connects
            if count >= 4:  
                total += 1

        return total

    # Simple board evaluation for FIRST ITERATION
    def count_patterns(self,symbol):
        score = 0
        directions = [(0,1), (1,0), (1,1), (1,-1)] 

        for row in range(self.rows):
            for col in range(self.cols):
                for dr, dc in directions:
                    pattern = []
                    for i in range(4):  # Check sequences of 4
                        r, c = row + dr*i, col + dc*i
                        if 0 <= r < self.rows and 0 <= c < self.cols:
                            pattern.append(self.board[r][c])
                        else:
                            break
                    if len(pattern) == 4:
                        if pattern.count(symbol) == 4:
                            score += 1000
                        elif pattern.count(symbol) == 3 and pattern.count(".") == 1:
                            score += 100
                        elif pattern.count(symbol) == 2 and pattern.count(".") == 2:
                            score += 10
        return score


# Regular minmax for FIRST ITERATION
def minimax(board, depth, maximizing_player):
    if depth == 0 or board.check_winner() or board.is_full():
        return board.evaluate_board()  # Returns a score

    if maximizing_player:  # AI’s turn
        max_eval = float('-inf')
        for col in range(5):
            if board.drop_piece(col, -1):  # AI plays (-1)
                score = minimax(board, depth - 1, False)
                board.undo_move(col)  # Undo move
                max_eval = max(max_eval, score)
        return max_eval
    else:  # Human’s turn
        min_eval = float('inf')
        for col in range(5):
            if board.drop_piece(col, 1):  # Player plays (1)
                score = minimax(board, depth - 1, True)
                board.undo_move(col)  # Undo move
                min_eval = min(min_eval, score)
        return min_eval
        
# alpha beta pruning for SECOND ITERATION
def minimax_alpha_beta(board, depth, alpha, beta, maximizing_player):
    winner = board.check_winner()
    if depth == 0 or winner != "." or board.is_full():
        return board.evaluate_board() if winner == "." else (1000 if winner == "O" else -1000)

    if maximizing_player:  # AI Turn
        max_eval = float('-inf')
        for col in range(5):
            if board.drop_piece(col, -1):  # AI places a piece
                score = minimax_alpha_beta(board, depth - 1, alpha, beta, False)
                board.undo_move(col)  # Undo move after checking
                max_eval = max(max_eval, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break  # Alpha-Beta Pruning
        return max_eval
    else:  # Human Turn
        min_eval = float('inf')
        for col in range(5):
            if board.drop_piece(col, 1):  # Human places a piece
                score = minimax_alpha_beta(board, depth - 1, alpha, beta, True)
                board.undo_move(col)
                min_eval = min(min_eval, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break  # Alpha-Beta Pruning
        return min_eval


def get_best_move(board, depth=4):
    best_score = float('-inf')
    best_move = -1
    # Center-out order. Changes order pieces are dropped from the middle out.
    col_order = [2, 1, 3, 0, 4]

    for col in col_order:
        if board.drop_piece(col, -1):
            score = minimax_alpha_beta(board, depth - 1, float('-inf'), float('inf'), False)
            board.undo_move(col)
            if score > best_score:
                best_score = score
                best_move = col

    return best_move


def play_game():
    game = ConnectFour()
    game.print_board()

    while not game.is_full():
        # Human Turn
        col = int(input("Enter column (0-4): "))  # Get player input
        while not (0 <= col < 5 and game.drop_piece(col, 1)):
            col = int(input("Invalid move! Try again (0-4): "))
        
        game.print_board()

        if game.check_winner() == "X":
            print("You Win! 🎉")
            return

        # AI Turn
        print("AI thinking...")
        ai_move = get_best_move(game)
        game.drop_piece(ai_move, -1)
        game.print_board()
        print(f"AI chose column {ai_move}")

        if game.check_winner() == "O":
            print("AI Wins! 🤖")
            return

    print("It's a Tie!")


# Run the game
play_game()
