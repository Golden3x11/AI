import copy

from decision_games_reversi.util import timeit
from reversi import calc_possible_moves, make_move, is_game_over

MAX_DEPTH_OF_TREE = 3

MAX_SYMBOL = None
@timeit
def get_move(board, symbol, score_heuristic):
    possible_moves = calc_possible_moves(board, symbol)
    best_move = None
    best_score = float('-inf')
    other_symbol = 2 if symbol == 1 else 1
    nodes_visited = 0
    global MAX_SYMBOL
    MAX_SYMBOL = symbol


    for move in possible_moves:
        board_copy = copy.deepcopy(board)
        board_copy = make_move(board_copy, symbol, move)
        score, visited = _alpha_beta(board_copy, other_symbol, 1, False, score_heuristic)
        nodes_visited += visited

        if score > best_score:
            best_move = move
            best_score = score
    print(f'Nodes visited: {nodes_visited}')
    return best_move


def _alpha_beta(board, symbol, depth, is_max_round, score_heuristic, alpha=float('-inf'), beta=float('inf')):
    possible_moves = calc_possible_moves(board, symbol)
    other_symbol = 2 if symbol == 1 else 1
    nodes_visited = 1


    if not possible_moves:
        if not is_game_over(board):
            score, visited = _alpha_beta(board, other_symbol, depth + 1, not is_max_round, score_heuristic, alpha, beta)
            nodes_visited += visited
            return score, nodes_visited

        return score_heuristic(board, MAX_SYMBOL), nodes_visited

    if depth < MAX_DEPTH_OF_TREE:
        for move in possible_moves:
            board_copy = copy.deepcopy(board)
            board_copy = make_move(board_copy, symbol, move)

            value, visited = _alpha_beta(board_copy, other_symbol, depth + 1, not is_max_round, score_heuristic, alpha, beta)
            nodes_visited += visited

            if is_max_round:
                alpha = max(alpha, value)
            else:
                beta = min(beta, value)

            if alpha >= beta:
                break

        return alpha if is_max_round else beta, nodes_visited

    return score_heuristic(board, MAX_SYMBOL), nodes_visited
