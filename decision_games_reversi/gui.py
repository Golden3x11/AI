import copy

import pygame
from decision_games_reversi import reversi, heuristics
from decision_games_reversi import alpha_beta

# Define constants for the game screen
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 560
CELL_SIZE = 60

# Define colors for the board and the pieces
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 128, 0)

# Initialize Pygame
pygame.init()

# Set up the game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Reversi")

# Load the images for the white and black pieces
piece_size = 60
white_piece = pygame.transform.scale(pygame.image.load('pieces/white.png'), (piece_size, piece_size))
white_smaller_piece = pygame.transform.scale(white_piece, (int(piece_size * 0.7), int(piece_size * 0.7)))
black_piece = pygame.transform.scale(pygame.image.load('pieces/black.png'), (piece_size, piece_size))
black_smaller_piece = pygame.transform.scale(black_piece, (int(piece_size * 0.7), int(piece_size * 0.7)))
grey_piece = pygame.transform.scale(pygame.image.load('pieces/grey.png'), (piece_size / 2, piece_size / 2))

def draw_board(board, valid_moves=None, current_player=None):
    """Draw the game board, pieces, current player, and scores on the screen."""
    screen.fill(GREEN)
    for row in range(reversi.BOARD_SIZE):
        for col in range(reversi.BOARD_SIZE):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
            if board[col][row] == reversi.SYMBOL_X:
                screen.blit(white_piece, (x, y))
            elif board[col][row] == reversi.SYMBOL_O:
                screen.blit(black_piece, (x, y))
    if valid_moves:
        for row, col, _ in valid_moves:
            x = col * CELL_SIZE + piece_size/4
            y = row * CELL_SIZE + piece_size/4
            screen.blit(grey_piece, (x, y))

    font = pygame.font.SysFont(None, 32)
    current_player_text = "Current player: " if current_player == reversi.SYMBOL_X else "Current player: "
    current_player_piece = white_piece if current_player == reversi.SYMBOL_X else black_piece
    screen.blit(current_player_piece, (175, SCREEN_HEIGHT - 70))
    text = font.render(current_player_text, True, BLACK)
    screen.blit(text, (10, SCREEN_HEIGHT - 55))

    score = reversi.calculate_score(board)
    white_score_text = f": {score[reversi.SYMBOL_X]}"
    screen.blit(white_smaller_piece, (400, SCREEN_HEIGHT - 80))
    text = font.render(white_score_text, True, BLACK)
    screen.blit(text, (445, SCREEN_HEIGHT - 70))

    black_score_text = f": {score[reversi.SYMBOL_O]}"
    screen.blit(black_smaller_piece, (400, SCREEN_HEIGHT - 40))
    text = font.render(black_score_text, True, BLACK)
    screen.blit(text, (445, SCREEN_HEIGHT - 30))

def draw_end_game(score):
    screen.fill(GREEN)
    if score[reversi.SYMBOL_X] > score[reversi.SYMBOL_O]:
        winner_text = "Player White wins!"
    elif score[reversi.SYMBOL_X] < score[reversi.SYMBOL_O]:
        winner_text = "Player Black wins!"
    else:
        winner_text = "It's a tie!"
    font = pygame.font.SysFont(None, 48)
    text = font.render(winner_text, True, BLACK)
    screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, SCREEN_HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.wait(3000)

def get_move(board, symbol):
    """Get the move from either the user or computer."""
    if symbol == reversi.SYMBOL_X:
        move = get_user_move(board, symbol)
    else:
        move = alpha_beta.get_move(board, symbol, heuristics.adaptive_strategy)

    return move

def get_user_move(board, symbol):
    """Get the move from the user."""
    move = None
    valid_moves = reversi.calc_possible_moves(board, symbol)
    if not valid_moves:
        return None
    draw_board(board, valid_moves, symbol)
    pygame.display.update()
    while move not in valid_moves:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = pos[0] // CELL_SIZE
                row = pos[1] // CELL_SIZE
                move = (row, col, [])
                for x, y, flipped in valid_moves:
                    if x == row and y == col:
                        move = (x, y, flipped)
                        break
    return move

def play_game():
    """Play the game of Reversi."""
    board = copy.deepcopy(reversi.BOARD)
    current_player = reversi.SYMBOL_X
    while not reversi.is_game_over(board):
        draw_board(board, current_player=current_player)
        pygame.display.update()
        move = get_move(board, current_player)
        if move:
            reversi.make_move(board, current_player, move)
        current_player = reversi.SYMBOL_X if current_player == reversi.SYMBOL_O else reversi.SYMBOL_O

    score = reversi.calculate_score(board)
    draw_end_game(score)

if __name__ == '__main__':
    play_game()
