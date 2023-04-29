import json
import shutil
import subprocess

from decision_games_reversi import reversi

if __name__ == '__main__':
    clear_board_file = 'clean_board.json'
    board_file = 'board.json'

    shutil.copy2(clear_board_file, board_file)
    current_player = reversi.SYMBOL_X

    with open(board_file, 'r') as f:
        board = json.load(f)
    while not reversi.is_game_over(board):
        subprocess.run(['python', 'one_move.py', str(current_player), board_file])
        current_player = reversi.SYMBOL_X if current_player == reversi.SYMBOL_O else reversi.SYMBOL_O
        with open(board_file, 'r') as f:
            board = json.load(f)

    # Print the final score
    reversi.print_board(board)
    score = reversi.calculate_score(board)
    if score[reversi.SYMBOL_X] > score[reversi.SYMBOL_O]:
        print("Player ⚪ wins!")
    elif score[reversi.SYMBOL_X] < score[reversi.SYMBOL_O]:
        print("Player ⚫ wins!")
    else:
        print("Tie game!")
