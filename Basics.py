import pygame
import sys
import random # For AI tie-breaking
import math # For infinity

WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE_SQUARE_COLOR = (245, 245, 220)
BLACK_SQUARE_COLOR = (139, 69, 19)
SELECTED_COLOR = (186, 202, 68)
HIGHLIGHT_COLOR = (0, 255, 0)
CHECK_TEXT_COLOR = (255, 0, 0)
PIECE_TEXT_COLOR = (0, 0, 0)
MESSAGE_BG_COLOR = (211, 211, 211, 180) # Light grey with some transparency

PIECES = {
    "r": "♜", "n": "♞", "b": "♝", "q": "♛", "k": "♚", "p": "♟",
    "R": "♖", "N": "♘", "B": "♗", "Q": "♕", "K": "♔", "P": "♙"
}

# --- Player Configuration ---
PLAYER_WHITE_IS_AI = True
PLAYER_BLACK_IS_AI = True

# --- AI Configuration ---
AI_DEPTH = 2  # Search depth for Minimax. Higher is stronger but much slower.
AI_THINKING_DURATION = 5000 # Milliseconds (5 seconds)

PIECE_VALUES = {
    "p": 10, "n": 30, "b": 30, "r": 50, "q": 90, "k": 900, 
    ".": 0
}


def create_board():
    # Standard chess starting position
    return [
        ["r","n","b","q","k","b","n","r"],
        ["p","p","p","p","p","p","p","p"],
        [".",".",".",".",".",".",".","."],
        [".",".",".",".",".",".",".","."],
        [".",".",".",".",".",".",".","."],
        [".",".",".",".",".",".",".","."],
        ["P","P","P","P","P","P","P","P"],
        ["R","N","B","Q","K","B","N","R"]
    ]

def get_square_under_mouse(mouse_pos):
    # Converts mouse coordinates to board row and column
    mouse_x, mouse_y = mouse_pos
    row = mouse_y // SQUARE_SIZE
    col = mouse_x // SQUARE_SIZE
    if 0 <= row < ROWS and 0 <= col < COLS:
        return row, col
    return None, None

def move_piece(board, start_pos, end_pos, promotion_piece='Q'):
    # Moves a piece on the board and handles pawn promotion
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    
    piece_to_move = board[start_row][start_col]
    board[start_row][start_col] = "."
    board[end_row][end_col] = piece_to_move

    # Pawn Promotion
    if piece_to_move.lower() == 'p':
        if piece_to_move == 'P' and end_row == 0: 
            board[end_row][end_col] = promotion_piece.upper()
        elif piece_to_move == 'p' and end_row == ROWS - 1:
            board[end_row][end_col] = promotion_piece.lower()
    return piece_to_move

def find_king(board, king_is_white):
    # Finds the position of the specified king
    king_char = "K" if king_is_white else "k"
    for r_idx in range(ROWS):
        for c_idx in range(COLS):
            if board[r_idx][c_idx] == king_char:
                return (r_idx, c_idx)
    return None

def is_square_attacked(board, square_pos_to_check, attacker_is_white):
    # Checks if a given square is attacked by the attacker's pieces
    attacker_turn_str = "White" if attacker_is_white else "Black"
    for r_idx in range(ROWS):
        for c_idx in range(COLS):
            piece = board[r_idx][c_idx]
            if piece == ".":
                continue
            
            piece_is_white_on_board = piece.isupper()
            if piece_is_white_on_board == attacker_is_white:
                moves = get_valid_moves(board, (r_idx, c_idx), attacker_turn_str, ignore_checks=True)
                if square_pos_to_check in moves:
                    return True
    return False

def get_valid_moves(board, piece_pos, current_player_turn_str, ignore_checks=False):
    # Calculates valid moves for a piece at piece_pos
    row, col = piece_pos
    piece_char = board[row][col]
    pseudo_moves = [] 

    if piece_char == ".":
        return [] 
    
    piece_is_white = piece_char.isupper()
    
    if not ((current_player_turn_str == "White" and piece_is_white) or \
            (current_player_turn_str == "Black" and not piece_is_white)):
        return []

    piece_type = piece_char.lower()

    if piece_type == "p":
        direction = -1 if piece_is_white else 1
        start_row_for_double_move = 6 if piece_is_white else 1
        if 0 <= row + direction < ROWS and board[row + direction][col] == ".":
            pseudo_moves.append((row + direction, col))
            if row == start_row_for_double_move and board[row + 2 * direction][col] == ".":
                pseudo_moves.append((row + 2 * direction, col))
        for capture_col_offset in [-1, 1]:
            nr, nc = row + direction, col + capture_col_offset
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                target_piece = board[nr][nc]
                if target_piece != "." and target_piece.isupper() != piece_is_white:
                    pseudo_moves.append((nr, nc))

    elif piece_type == "n":
        knight_move_offsets = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        for dr, dc in knight_move_offsets:
            nr, nc = row + dr, col + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                target_piece = board[nr][nc]
                if target_piece == "." or target_piece.isupper() != piece_is_white:
                    pseudo_moves.append((nr, nc))

    elif piece_type in ["r", "b", "q"]:
        directions = []
        if piece_type == "r": directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        elif piece_type == "b": directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        elif piece_type == "q": directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dr, dc in directions:
            nr, nc = row, col
            while True:
                nr += dr
                nc += dc
                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    target_piece = board[nr][nc]
                    if target_piece == ".": pseudo_moves.append((nr, nc))
                    elif target_piece.isupper() != piece_is_white:
                        pseudo_moves.append((nr, nc)); break
                    else: break
                else: break
    
    elif piece_type == "k":
        king_move_offsets = [
            (-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)
        ]
        for dr, dc in king_move_offsets:
            nr, nc = row + dr, col + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                target_piece = board[nr][nc]
                if target_piece == "." or target_piece.isupper() != piece_is_white:
                    pseudo_moves.append((nr, nc))

    if ignore_checks:
        return pseudo_moves
    else:
        legal_moves = []
        for move_end_pos in pseudo_moves:
            temp_board = [r.copy() for r in board]
            move_piece(temp_board, piece_pos, move_end_pos)
            king_owner_is_white = piece_is_white
            if not is_in_check(temp_board, king_owner_is_white):
                legal_moves.append(move_end_pos)
        return legal_moves

def is_in_check(board, current_player_king_is_white):
    king_pos = find_king(board, current_player_king_is_white)
    if not king_pos: return True 
    opponent_is_white = not current_player_king_is_white
    return is_square_attacked(board, king_pos, opponent_is_white)

def get_all_legal_moves_for_player(board, player_turn_str):
    all_moves = []
    player_is_white = (player_turn_str == "White")
    for r_idx in range(ROWS):
        for c_idx in range(COLS):
            piece_char = board[r_idx][c_idx]
            if piece_char != ".":
                piece_is_white_on_board = piece_char.isupper()
                if piece_is_white_on_board == player_is_white:
                    moves = get_valid_moves(board, (r_idx, c_idx), player_turn_str, ignore_checks=False)
                    for move in moves:
                        all_moves.append(((r_idx, c_idx), move))
    return all_moves

def has_any_legal_moves(board, player_turn_str):
    return bool(get_all_legal_moves_for_player(board, player_turn_str))

def draw_board(win, board, selected_piece_coords=None, valid_moves_for_selected=[], 
               check_flag=False, checkmate_flag=False, stalemate_flag=False, 
               thinking_flag=False, thinking_player_color_str=None): # Added thinking_player_color_str
    # Draws the entire game board, pieces, highlights, and messages
    try:
        piece_font = pygame.font.SysFont("Segoe UI Symbol", 48)
    except pygame.error:
        piece_font = pygame.font.SysFont("arial", 48)
    
    message_font = pygame.font.SysFont("arial", 30, bold=True)

    for r in range(ROWS):
        for c in range(COLS):
            square_color = WHITE_SQUARE_COLOR if (r + c) % 2 == 0 else BLACK_SQUARE_COLOR
            if selected_piece_coords == (r, c): # Only relevant for human player
                square_color = SELECTED_COLOR
            pygame.draw.rect(win, square_color, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            if (r, c) in valid_moves_for_selected: # Only relevant for human player
                highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                pygame.draw.circle(highlight_surface, (*HIGHLIGHT_COLOR, 100), 
                                   (SQUARE_SIZE // 2, SQUARE_SIZE // 2), SQUARE_SIZE // 5)
                win.blit(highlight_surface, (c * SQUARE_SIZE, r * SQUARE_SIZE))
            
            piece_char = board[r][c]
            if piece_char != ".":
                text_surface = piece_font.render(PIECES[piece_char], True, PIECE_TEXT_COLOR)
                text_rect = text_surface.get_rect(center=(c*SQUARE_SIZE + SQUARE_SIZE//2, 
                                                          r*SQUARE_SIZE + SQUARE_SIZE//2))
                win.blit(text_surface, text_rect)
    
    msg_str = ""
    if thinking_flag and thinking_player_color_str: # Use the passed color
        msg_str = f"{thinking_player_color_str} is thinking..."
    elif checkmate_flag:
        # Winner is the one NOT whose turn it is when checkmate occurs
        # This logic is handled in main() when setting the caption.
        # For the message, we can infer from who *was* checkmated.
        # If White was checkmated, Black wins. If Black was checkmated, White wins.
        # This needs the `current_player_turn` at the point of checkmate.
        # Let's assume `thinking_player_color_str` can be repurposed or we pass winner.
        # For simplicity, the main loop's caption is more accurate for winner.
        # The message here can be generic or rely on a winner string passed.
        # For now, let's keep it simple, the caption will have the winner.
        msg_str = "Checkmate!" 
    elif stalemate_flag:
        msg_str = "Stalemate! It's a draw."
    elif check_flag:
        msg_str = "Check!"
    
    if msg_str:
        text_surface = message_font.render(msg_str, True, CHECK_TEXT_COLOR)
        bg_width = text_surface.get_width() + 20
        bg_height = text_surface.get_height() + 10
        bg_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        bg_surface.fill(MESSAGE_BG_COLOR)
        bg_rect = bg_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        win.blit(bg_surface, bg_rect)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        win.blit(text_surface, text_rect)

# --- AI Functions ---
def evaluate_board(board):
    score = 0
    for r in range(ROWS):
        for c in range(COLS):
            piece_char = board[r][c]
            if piece_char != ".":
                value = PIECE_VALUES.get(piece_char.lower(), 0)
                if piece_char.isupper(): score += value
                else: score -= value
    return score

def minimax(board, depth, alpha, beta, maximizing_player_is_white, current_player_for_moves_str):
    if depth == 0:
        return evaluate_board(board)

    player_has_moves = has_any_legal_moves(board, current_player_for_moves_str)
    # The king to check for check/checkmate is the one whose turn it is currently in the simulation
    king_to_check_is_white = (current_player_for_moves_str == "White")
    king_is_in_check = is_in_check(board, king_to_check_is_white)

    if not player_has_moves:
        if king_is_in_check: # Checkmate
            # If it's White's turn (maximizer) and no moves in check = Black wins (-inf)
            # If it's Black's turn (minimizer) and no moves in check = White wins (+inf)
            return -math.inf if king_to_check_is_white else math.inf 
        else: # Stalemate
            return 0 

    possible_next_moves = get_all_legal_moves_for_player(board, current_player_for_moves_str)

    if maximizing_player_is_white: # Current node is for White (Maximizer)
        max_eval = -math.inf
        for start_pos, end_pos in possible_next_moves:
            temp_board = [r.copy() for r in board]
            move_piece(temp_board, start_pos, end_pos)
            # Next node will be Black's turn (Minimizer)
            eval_score = minimax(temp_board, depth - 1, alpha, beta, False, "Black")
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha: break
        return max_eval
    else: # Current node is for Black (Minimizer)
        min_eval = math.inf
        for start_pos, end_pos in possible_next_moves:
            temp_board = [r.copy() for r in board]
            move_piece(temp_board, start_pos, end_pos)
            # Next node will be White's turn (Maximizer)
            eval_score = minimax(temp_board, depth - 1, alpha, beta, True, "White")
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha: break
        return min_eval

def get_ai_move(board_state, search_depth, ai_turn_str):
    best_move = None
    possible_first_moves = get_all_legal_moves_for_player(board_state, ai_turn_str)
    random.shuffle(possible_first_moves) 

    ai_is_white = (ai_turn_str == "White")

    if ai_is_white: 
        max_eval_found = -math.inf
        for start_pos, end_pos in possible_first_moves:
            temp_board = [r.copy() for r in board_state]
            move_piece(temp_board, start_pos, end_pos)
            eval_score = minimax(temp_board, search_depth - 1, -math.inf, math.inf, False, "Black")
            if eval_score > max_eval_found:
                max_eval_found = eval_score
                best_move = (start_pos, end_pos)
    else: 
        min_eval_found = math.inf
        for start_pos, end_pos in possible_first_moves:
            temp_board = [r.copy() for r in board_state]
            move_piece(temp_board, start_pos, end_pos)
            eval_score = minimax(temp_board, search_depth - 1, -math.inf, math.inf, True, "White")
            if eval_score < min_eval_found:
                min_eval_found = eval_score
                best_move = (start_pos, end_pos)
    return best_move

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    
    main_board = create_board()
    selected_piece_coords = None 
    current_player_turn = "White"
    valid_moves_for_display = [] 
    
    is_check_active = False
    is_checkmate_active = False
    is_stalemate_active = False
    game_is_over = False
    
    ai_is_thinking = False # Flag to indicate AI is in its thinking period
    ai_thinking_start_time = 0 # Timestamp when AI started thinking

    running = True
    clock = pygame.time.Clock()
    pygame.display.set_caption(f"Chess - {current_player_turn}'s Turn")

    while running:
        current_time_ticks = pygame.time.get_ticks()

        # --- Determine if current player is AI ---
        is_current_player_ai = (current_player_turn == "White" and PLAYER_WHITE_IS_AI) or \
                               (current_player_turn == "Black" and PLAYER_BLACK_IS_AI)

        # --- Game State Updates (Check, Checkmate, Stalemate) ---
        if not game_is_over:
            current_player_king_is_white = (current_player_turn == "White")
            is_check_active = is_in_check(main_board, current_player_king_is_white)
            
            if not has_any_legal_moves(main_board, current_player_turn):
                if is_check_active:
                    is_checkmate_active = True
                    # The player whose turn it IS, is checkmated. The OTHER player wins.
                    winner = "Black" if current_player_turn == "White" else "White"
                    print(f"Checkmate! {winner} wins.")
                else:
                    is_stalemate_active = True
                    print("Stalemate! It's a draw.")
                game_is_over = True

        # --- Event Handling Loop (Primarily for Quit and Game Over) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Human player input (only if not AI's turn and game not over)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and \
               not game_is_over and not is_current_player_ai:
                
                mouse_pos = pygame.mouse.get_pos()
                clicked_row, clicked_col = get_square_under_mouse(mouse_pos)

                if clicked_row is None: continue

                clicked_square_content = main_board[clicked_row][clicked_col]

                if selected_piece_coords: 
                    if (clicked_row, clicked_col) in valid_moves_for_display:
                        move_piece(main_board, selected_piece_coords, (clicked_row, clicked_col))
                        current_player_turn = "Black" if current_player_turn == "White" else "White"
                        selected_piece_coords = None
                        valid_moves_for_display = []
                    elif clicked_square_content != ".":
                        is_clk_pc_white = clicked_square_content.isupper()
                        is_curr_plyr_white = (current_player_turn == "White")
                        if is_clk_pc_white == is_curr_plyr_white:
                            selected_piece_coords = (clicked_row, clicked_col)
                            valid_moves_for_display = get_valid_moves(main_board, selected_piece_coords, current_player_turn)
                        else:
                            selected_piece_coords = None; valid_moves_for_display = []
                    else:
                        selected_piece_coords = None; valid_moves_for_display = []
                elif clicked_square_content != ".":
                    is_clk_pc_white = clicked_square_content.isupper()
                    is_curr_plyr_white = (current_player_turn == "White")
                    if is_clk_pc_white == is_curr_plyr_white:
                        selected_piece_coords = (clicked_row, clicked_col)
                        valid_moves_for_display = get_valid_moves(main_board, selected_piece_coords, current_player_turn)
            
            if game_is_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: # Allow quitting with 'Q' after game over
                    running = False


        # --- AI's Turn Logic ---
        if not game_is_over and is_current_player_ai:
            if not ai_is_thinking: # AI starts its "thinking" phase
                ai_is_thinking = True
                ai_thinking_start_time = current_time_ticks
                # Caption and board will be updated below before flip to show "thinking"
            
            # Check if thinking duration has passed
            if ai_is_thinking and (current_time_ticks - ai_thinking_start_time >= AI_THINKING_DURATION):
                # AI's thinking time is over, now make the move
                ai_best_move = get_ai_move(main_board, AI_DEPTH, current_player_turn)
                
                if ai_best_move:
                    start_pos, end_pos = ai_best_move
                    move_piece(main_board, start_pos, end_pos)
                else:
                    # This case should be covered by checkmate/stalemate detection
                    print(f"AI ({current_player_turn}) found no move (should be game over).")
                
                current_player_turn = "Black" if current_player_turn == "White" else "White"
                ai_is_thinking = False # Reset thinking flag for the next AI turn
                selected_piece_coords = None # Clear any human selection visual
                valid_moves_for_display = []
        
        # --- Drawing ---
        win.fill(BLACK_SQUARE_COLOR) 
        # Pass current_player_turn for the thinking message color
        draw_board(win, main_board, selected_piece_coords, valid_moves_for_display, 
                   is_check_active, is_checkmate_active, is_stalemate_active, 
                   ai_is_thinking, current_player_turn if ai_is_thinking else None) 
        
        # --- Update Window Caption ---
        if game_is_over:
            if is_checkmate_active:
                # The player whose turn it WAS when checkmate was declared is the loser.
                # So, the winner is the *other* player.
                winner = "Black" if (current_player_turn == "White") else "White"
                pygame.display.set_caption(f"Checkmate! {winner} wins! (Press Q to Quit)")
            elif is_stalemate_active:
                pygame.display.set_caption("Stalemate! It's a draw. (Press Q to Quit)")
        elif ai_is_thinking:
             pygame.display.set_caption(f"Chess - {current_player_turn} is thinking...")
        else:
             pygame.display.set_caption(f"Chess - {current_player_turn}'s Turn {'(Check!)' if is_check_active else ''}")

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
