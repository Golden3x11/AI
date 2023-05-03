import json
import sys

from decision_games_reversi import alpha_beta, reversi, heuristics


def get_computer_move(board, symbol):
    return alpha_beta.get_move(board, symbol, heuristics.adaptive_strategy)


def play_one_move(board, current_player):
    move = get_computer_move(board, current_player)
    if move:
        reversi.make_move(board, current_player, move)
    return board


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python one_move.py <symbol> <board file>")
        exit()

    board_file = sys.argv[2]
    current_player = int(sys.argv[1])
    with open(board_file, "r") as f:
        board = json.load(f)

    board = play_one_move(board, current_player)
    with open(board_file, 'w') as f:
        json.dump(board, f)
