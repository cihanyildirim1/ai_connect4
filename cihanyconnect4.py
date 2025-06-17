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

