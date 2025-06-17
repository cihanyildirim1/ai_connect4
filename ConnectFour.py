# Objective:
# The goal of Connect Four is to get four of your discs in a row, either horizontally, vertically, or diagonally, on a 7x6 grid.
#
# Rules:
# The game is played on a 7-column, 6-row grid.
# Players take turns dropping a colored disc (usually red and yellow) into one of the seven columns. The disc will fall to the lowest available space in that column.
# The first player to get four discs in a row, either horizontally, vertically, or diagonally, wins the game.
# If the grid is filled up and no player has won, the game is a draw.
# The game can be restarted after a win or draw.

import random

# Define constants for the board size
ROWS = 6
COLS = 7

# Initialize the board as a 2D list
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Display the board
def print_board(board):
    print(" 0   1   2   3   4   5   6 ")
    print("|---|---|---|---|---|---|---|")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("|---|---|---|---|---|---|---|")

# Drop a piece into the selected column
def drop_piece(board, col, piece):
    for row in range(ROWS - 1, -1, -1):  # Start from the bottom row
        if board[row][col] == ' ':
            board[row][col] = piece
            return row, col
    return -1, -1  # Column is full

# Check for a win (horizontal, vertical, or diagonal)
def check_win(board, row, col, piece):
    # Check horizontal
    for c in range(col - 3, col + 1):
        if 0 <= c <= 3 and all(board[row][c + i] == piece for i in range(4)):
            return True

    # Check vertical
    for r in range(row - 3, row + 1):
        if 0 <= r <= 2 and all(board[r + i][col] == piece for i in range(4)):
            return True

    # Check diagonal (down-right and up-right)
    for dr, dc in [(1, 1), (-1, 1)]:
        for i in range(-3, 1):
            # Make sure the indices are within bounds
            if 0 <= row + i * dr <= 5 and 0 <= col + i * dc <= 6:
                if all(0 <= row + (i + j) * dr <= 5 and 0 <= col + (i + j) * dc <= 6 and board[row + (i + j) * dr][col + (i + j) * dc] == piece for j in range(4)):
                    return True

    return False

# AI chooses a random column that is not full
def ai_move(board):
    import math
    EMPTY = " "
    PLAYER_PIECE = "O"
    AI_PIECE = "X"
    WINDOW_LENGTH = 4

    def is_valid_location(b, col):
        return b[0][col] == EMPTY  

    def get_next_open_row(b, col):
        for r in range(ROWS - 1, -1, -1):
            if b[r][col] == EMPTY:
                return r
        return None

    def evaluate_window(window, piece):
        score = 0
        opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE
        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 4
        return score

    def score_position(b, piece):
        score = 0
        # Score center column
        center_col = COLS // 2
        center_array = [b[r][center_col] for r in range(ROWS)]
        score += center_array.count(piece) * 3
        # Score Horizontal
        for r in range(ROWS):
            row_array = b[r]
            for c in range(COLS - WINDOW_LENGTH + 1):
                window = row_array[c:c + WINDOW_LENGTH]
                score += evaluate_window(window, piece)
        # Score Vertical
        for c in range(COLS):
            col_array = [b[r][c] for r in range(ROWS)]
            for r in range(ROWS - WINDOW_LENGTH + 1):
                window = col_array[r:r + WINDOW_LENGTH]
                score += evaluate_window(window, piece)

        # Score positive diagonal
        for r in range(ROWS - WINDOW_LENGTH + 1):
            for c in range(COLS - WINDOW_LENGTH + 1):
                window = [b[r + i][c + i] for i in range(WINDOW_LENGTH)]
                score += evaluate_window(window, piece)

        # Score negative diagonal
        for r in range(WINDOW_LENGTH - 1, ROWS):
            for c in range(COLS - WINDOW_LENGTH + 1):
                window = [b[r - i][c + i] for i in range(WINDOW_LENGTH)]
                score += evaluate_window(window, piece)

        return score

    def get_valid_locations(b):
        valid_locations = []
        for col in range(COLS):
            if is_valid_location(b, col):
                valid_locations.append(col)
        return valid_locations

    # Board-wide win check
    def winning_move(b, piece):
        for r in range(ROWS):
            for c in range(COLS):
                if b[r][c] == piece:
                    if check_win(b, r, c, piece):
                        return True
        return False

    def is_terminal_node(b):
        return (winning_move(b, PLAYER_PIECE) or 
                winning_move(b, AI_PIECE) or 
                len(get_valid_locations(b)) == 0)
    
    #minmax algorithm
    def minimax(b, depth, alpha, beta, maximizingPlayer):
        valid_locations = get_valid_locations(b)
        terminal = is_terminal_node(b)
        if depth == 0 or terminal:
            if terminal:
                if winning_move(b, AI_PIECE):
                    return (None, 100000000000000)
                elif winning_move(b, PLAYER_PIECE):
                    return (None, -10000000000000)
                else:
                    return (None, 0)
            else:
                return (None, score_position(b, AI_PIECE))
        if maximizingPlayer:
            value = -math.inf
            best_col = random.choice(valid_locations)
            for col in valid_locations:
                row = get_next_open_row(b, col)
                if row is None:
                    continue
                b_copy = [r[:] for r in b]  # Deep copy
                b_copy[row][col] = AI_PIECE
                new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    best_col = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return best_col, value
        else:
            value = math.inf
            best_col = random.choice(valid_locations)
            for col in valid_locations:
                row = get_next_open_row(b, col)
                if row is None:
                    continue
                b_copy = [r[:] for r in b]
                b_copy[row][col] = PLAYER_PIECE
                new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    best_col = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return best_col, value

    valid_locations = get_valid_locations(board)
    if not valid_locations:
        return None
    best_column, _ = minimax(board, 5, -math.inf, math.inf, True)
    return best_column



# Main function to play the game
def play_game():
    board = create_board()
    print_board(board)
    turn = 0  # Player 1 starts
    while True:
        if turn % 2 == 0:
            player_piece = 'O'  # Player 1 is 'O'
            print("Player 1, choose a column (0-6):")
            col = int(input())
        else:
            player_piece = 'X'  # Player 2 (AI) is 'X'
            print("Player 2 (AI) chooses a column.")
            col = ai_move(board)

        # Drop the piece in the selected column
        row, col = drop_piece(board, col, player_piece)

        if row == -1:
            print("Column is full, try again.")
            continue

        print_board(board)

        # Check for a win
        if check_win(board, row, col, player_piece):
            if turn % 2 == 0:
                print("Player 1 wins!")
            else:
                print("Player 2 wins!")
            break

        turn += 1

# Run the game
if __name__ == "__main__":
    play_game()