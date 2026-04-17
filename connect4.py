# Connect 4 Game with Optimized AI

import time

# ============================================
# BOARD MANAGEMENT FUNCTIONS
# ============================================

def create_board():
    """Create a 6x7 empty board"""
    return [[' ' for _ in range(7)] for _ in range(6)]

def print_board(board):
    """Print the board in a clear, visually appealing format"""
    print("\n" + "="*31)
    print("  0   1   2   3   4   5   6")
    print("="*31)
    for row in board:
        print("| " + " | ".join(row) + " |")
    print("="*31)

def is_column_full(board, column):
    """Check if a column is full"""
    return board[0][column] != ' '

def is_board_full(board):
    """Check if the board is completely full"""
    return all(board[0][col] != ' ' for col in range(7))

def get_available_columns(board):
    """Get list of columns that are not full, ordered by strategic value"""
    # Center-first ordering for better alpha-beta pruning
    column_order = [3, 2, 4, 1, 5, 0, 6]
    return [col for col in column_order if not is_column_full(board, col)]

def drop_piece(board, column, piece):
    """Drop a piece in the specified column (modifies board in-place)"""
    for row in range(5, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = piece
            return row
    return -1

def remove_piece(board, column, row):
    """Remove a piece from the board (for undo in minimax)"""
    board[row][column] = ' '

# ============================================
# WIN DETECTION FUNCTIONS
# ============================================

def check_win(board, piece):
    """Check if the current piece has won"""
    # Check horizontal
    for row in range(6):
        for col in range(4):
            if all(board[row][col+i] == piece for i in range(4)):
                return True
    
    # Check vertical
    for row in range(3):
        for col in range(7):
            if all(board[row+i][col] == piece for i in range(4)):
                return True
    
    # Check diagonal (down-right)
    for row in range(3):
        for col in range(4):
            if all(board[row+i][col+i] == piece for i in range(4)):
                return True
    
    # Check diagonal (up-right)
    for row in range(3, 6):
        for col in range(4):
            if all(board[row-i][col+i] == piece for i in range(4)):
                return True
    
    return False

def is_winning_move(board, column, piece):
    """Check if dropping a piece in this column wins the game"""
    row = drop_piece(board, column, piece)
    if row == -1:
        return False
    wins = check_win(board, piece)
    remove_piece(board, column, row)
    return wins

# ============================================
# AI EVALUATION FUNCTIONS
# ============================================

def evaluate_window(window, piece):
    """Evaluate a window of 4 positions with improved scoring"""
    opponent = 'X' if piece == 'O' else 'O'
    
    piece_count = window.count(piece)
    empty_count = window.count(' ')
    opponent_count = window.count(opponent)
    
    # AI's opportunities
    if piece_count == 4:
        return 1000
    elif piece_count == 3 and empty_count == 1:
        return 50
    elif piece_count == 2 and empty_count == 2:
        return 10
    
    # Block opponent threats
    if opponent_count == 3 and empty_count == 1:
        return -80
    elif opponent_count == 2 and empty_count == 2:
        return -5
    
    return 0

def score_position(board, piece):
    """Evaluate the entire board position with strategic preferences"""
    score = 0
    
    # Strongly prefer center column
    center_array = [board[row][3] for row in range(6)]
    score += center_array.count(piece) * 6
    
    # Prefer columns near center
    for col in [2, 4]:
        col_array = [board[row][col] for row in range(6)]
        score += col_array.count(piece) * 2
    
    # Score all windows
    # Horizontal
    for row in range(6):
        for col in range(4):
            window = [board[row][col+i] for i in range(4)]
            score += evaluate_window(window, piece)
    
    # Vertical
    for col in range(7):
        for row in range(3):
            window = [board[row+i][col] for i in range(4)]
            score += evaluate_window(window, piece)
    
    # Diagonal (down-right)
    for row in range(3):
        for col in range(4):
            window = [board[row+i][col+i] for i in range(4)]
            score += evaluate_window(window, piece)
    
    # Diagonal (up-right)
    for row in range(3, 6):
        for col in range(4):
            window = [board[row-i][col+i] for i in range(4)]
            score += evaluate_window(window, piece)
    
    return score

# ============================================
# MINIMAX WITH ALPHA-BETA PRUNING
# ============================================

def minimax(board, depth, alpha, beta, maximizing_player):
    """
    Minimax algorithm with alpha-beta pruning
    - Uses in-place board modifications for efficiency
    - Prunes branches that can't affect the final decision
    - Evaluates center columns first for better pruning
    """
    available_cols = get_available_columns(board)
    
    # Terminal conditions
    if check_win(board, 'O'):
        return (None, 100000000)
    if check_win(board, 'X'):
        return (None, -100000000)
    if is_board_full(board):
        return (None, 0)
    if depth == 0:
        return (None, score_position(board, 'O'))
    
    if maximizing_player:
        value = float('-inf')
        best_column = available_cols[0]
        
        for col in available_cols:
            row = drop_piece(board, col, 'O')
            new_score = minimax(board, depth - 1, alpha, beta, False)[1]
            remove_piece(board, col, row)
            
            if new_score > value:
                value = new_score
                best_column = col
            
            alpha = max(alpha, value)
            if alpha >= beta:  # Beta cutoff
                break
        
        return best_column, value
    
    else:  # Minimizing player
        value = float('inf')
        best_column = available_cols[0]
        
        for col in available_cols:
            row = drop_piece(board, col, 'X')
            new_score = minimax(board, depth - 1, alpha, beta, True)[1]
            remove_piece(board, col, row)
            
            if new_score < value:
                value = new_score
                best_column = col
            
            beta = min(beta, value)
            if alpha >= beta:  # Alpha cutoff
                break
        
        return best_column, value

# ============================================
# AI MOVE SELECTION
# ============================================

def get_ai_move(board):
    """Get the best move for AI with optimized decision making"""
    available_cols = get_available_columns(board)
    
    # Priority 1: Take winning move immediately
    for col in available_cols:
        if is_winning_move(board, col, 'O'):
            print("🤖 AI is thinking...")
            time.sleep(0.3)
            print(f"✓ AI plays column {col} (Winning move!)\n")
            return col
    
    # Priority 2: Block opponent's winning move
    for col in available_cols:
        if is_winning_move(board, col, 'X'):
            print("🤖 AI is thinking...")
            time.sleep(0.3)
            print(f"✓ AI plays column {col} (Blocking your win!)\n")
            return col
    
    # Priority 3: Use minimax for strategic move
    print("🤖 AI is thinking...")
    time.sleep(0.5)
    column, score = minimax(board, 3, float('-inf'), float('inf'), True)
    print(f"✓ AI plays column {column}\n")
    return column

# ============================================
# PLAYER INPUT FUNCTIONS
# ============================================

def get_valid_column(board, player):
    """Get a valid column number from the player"""
    while True:
        try:
            user_input = input("Choose column (0-6): ").strip()
            
            if not user_input:
                print("❌ Please enter a column number!\n")
                continue
            
            column = int(user_input)
            
            if column < 0 or column > 6:
                print("❌ Invalid column! Please choose between 0 and 6.\n")
                continue
            
            if is_column_full(board, column):
                print("❌ Column is full! Please choose another column.\n")
                continue
            
            print(f"✓ You play column {column}\n")
            return column
            
        except ValueError:
            print("❌ Please enter a valid number (0-6)!\n")

# ============================================
# MAIN GAME LOOP
# ============================================

def play_game():
    """Main game loop"""
    board = create_board()
    current_player = 'X'
    
    # Welcome screen
    print("\n" + "="*40)
    print("       WELCOME TO CONNECT 4!".center(40))
    print("="*40)
    print("\n  You: X  |  AI: O")
    print("  Goal: Connect 4 pieces in a row!")
    print("  (Horizontal, Vertical, or Diagonal)")
    print("\n" + "="*40)
    
    while True:
        print_board(board)
        
        if current_player == 'X':
            # Human player's turn
            print("\n>>> YOUR TURN <<<")
            column = get_valid_column(board, current_player)
        else:
            # AI's turn
            print("\n>>> AI'S TURN <<<")
            column = get_ai_move(board)
        
        drop_piece(board, column, current_player)
        
        # Check for win
        if check_win(board, current_player):
            print_board(board)
            print("\n" + "="*40)
            if current_player == 'X':
                print("       🎉 YOU WIN! 🎉".center(40))
                print("     Congratulations!".center(40))
            else:
                print("       🤖 AI WINS! 🤖".center(40))
                print("     Better luck next time!".center(40))
            print("="*40 + "\n")
            break
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("\n" + "="*40)
            print("       IT'S A DRAW!".center(40))
            print("     Well played!".center(40))
            print("="*40 + "\n")
            break
        
        # Switch player
        current_player = 'O' if current_player == 'X' else 'X'

if __name__ == "__main__":
    play_game()
