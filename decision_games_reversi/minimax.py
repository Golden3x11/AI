import copy

from decision_games_reversi.util import timeit
from reversi import calc_possible_moves, make_move, is_game_over

MAX_DEPTH_OF_TREE = 3
SYMBOL = None


@timeit
def get_move(board, symbol, score_heuristic):
    possible_moves = calc_possible_moves(board, symbol)
    best_move = None
    best_score = float('-inf')
    other_symbol = 2 if symbol == 1 else 1
    nodes_visited = 0
    global SYMBOL
    SYMBOL = symbol

    for move in possible_moves:
        board_copy = copy.deepcopy(board)
        board_copy = make_move(board_copy, symbol, move)
        score, visited = _minimax(board_copy, other_symbol, 1, False, score_heuristic)
        nodes_visited += visited
        print(score, move)
        if score > best_score:
            best_move = move
            best_score = score
    print(f'Nodes visited: {nodes_visited}')
    return best_move


def _minimax(board, symbol, depth, is_max_round, score_heuristic):
    possible_moves = calc_possible_moves(board, symbol)
    other_symbol = 2 if symbol == 1 else 1
    nodes_visited = 1

    if not possible_moves:
        if not is_game_over(board):
            score, visited = _minimax(board, other_symbol, depth + 1, not is_max_round, score_heuristic)
            nodes_visited += visited
            return score, nodes_visited
        return score_heuristic(board, SYMBOL), nodes_visited

    if depth < MAX_DEPTH_OF_TREE:
        scores = []
        for move in possible_moves:
            board_copy = copy.deepcopy(board)
            board_copy = make_move(board_copy, symbol, move)

            score, visited = _minimax(board_copy, other_symbol, depth + 1, not is_max_round, score_heuristic)
            nodes_visited += visited

            scores.append(score)

        return max(scores) if is_max_round else min(scores), nodes_visited

    return score_heuristic(board, SYMBOL), nodes_visited

