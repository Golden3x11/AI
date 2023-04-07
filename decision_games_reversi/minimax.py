import copy

from reversi import calc_possible_moves, make_move

MAX_DEPTH_OF_TREE = 4


def get_move(board, symbol, score_heuristic):
    possible_moves = calc_possible_moves(board, symbol)
    best_move = None
    best_score = float('-inf')

    for move in possible_moves:
        board_copy = copy.deepcopy(board)
        score = _minimax(board_copy, symbol, MAX_DEPTH_OF_TREE, True, score_heuristic)
        if score > best_score:
            best_move = move
            best_score = score

    return best_move


def _minimax(board, symbol, depth, is_max_round, score_heuristic):
    possible_moves = calc_possible_moves(board, symbol)
    other_symbol = 2 if symbol == 1 else 1

    if not possible_moves:
        if not calc_possible_moves(board, other_symbol):
            return _minimax(board, other_symbol, depth + 1, not is_max_round, score_heuristic)
        else:
            return score_heuristic(board, symbol)

    if depth < MAX_DEPTH_OF_TREE:
        scores = []
        for move in possible_moves:
            board_copy = copy.deepcopy(board)
            board_copy = make_move(board_copy, symbol, move)

            scores.append(_minimax(board_copy, other_symbol, depth + 1, not is_max_round, score_heuristic))

        return max(scores) if is_max_round else min(scores)

    return score_heuristic(board, symbol)
