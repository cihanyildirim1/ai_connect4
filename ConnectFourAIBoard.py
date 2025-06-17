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
    available_cols = [col for col in range(COLS) if board[0][col] == ' ']
    return random.choice(available_cols)
def ai_player(board):
    available_cols = [col for col in range(COLS) if board[0][col] == ' ']
    return random.choice(available_cols)
# Main function to play the game


def play_game():
    board = create_board()
    print_board(board)
    turn = 0  # Player 1 starts
    while True:
        if turn % 2 == 0:
            player_piece = 'O'  # Player 1 is 'O'
            print("Player 1, choose a column (0-6):")
            col = ai_player(board)
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