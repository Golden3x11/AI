from decision_games_reversi.reversi import calculate_score, SYMBOL_O, SYMBOL_X, calc_possible_moves, \
    BOARD_SIZE, ALL_POSSIBLE_DIRECTIONS, is_on_board

CORNERS = [(0, 0), (0, BOARD_SIZE - 1), (BOARD_SIZE - 1, 0), (BOARD_SIZE - 1, BOARD_SIZE - 1)]
EDGES = [(0, i) for i in range(2, BOARD_SIZE - 2)] + \
        [(BOARD_SIZE - 1, i) for i in range(2, BOARD_SIZE - 2)] + \
        [(i, 0) for i in range(2, BOARD_SIZE - 2)] + \
        [(i, BOARD_SIZE - 1) for i in range(2, BOARD_SIZE - 2)]


def corners(board, max_symbol):
    min_symbol = SYMBOL_O if max_symbol == SYMBOL_X else SYMBOL_X
    corner_count_max = 0
    corner_count_min = 0
    for x, y in CORNERS:
        if board[y][x] == max_symbol:
            corner_count_max += 1
        elif board[y][x] == min_symbol:
            corner_count_min += 1
    return calc_percent(corner_count_max, corner_count_min)


def edges(board, max_symbol):
    min_symbol = SYMBOL_O if max_symbol == SYMBOL_X else SYMBOL_X
    edge_count_max = 0
    edge_count_min = 0
    for x, y in EDGES:
        if board[y][x] == max_symbol:
            edge_count_max += 1
        elif board[y][x] == min_symbol:
            edge_count_min += 1
    return calc_percent(edge_count_max, edge_count_min)


def coin_parity(board, symbol):
    min_symbol = SYMBOL_O if symbol == SYMBOL_X else SYMBOL_X
    score = calculate_score(board)
    return calc_percent(score[symbol], score[min_symbol])


def mobility(board, max_symbol):
    min_symbol = SYMBOL_O if max_symbol == SYMBOL_X else SYMBOL_X
    moves_max = len(calc_possible_moves(board, max_symbol))
    moves_min = len(calc_possible_moves(board, min_symbol))
    return calc_percent(moves_max, moves_min)


def stability(board, max_symbol):
    min_symbol = SYMBOL_O if max_symbol == SYMBOL_X else SYMBOL_X
    stability_max = calc_stability(board, max_symbol)
    stability_min = calc_stability(board, min_symbol)
    return calc_percent(stability_max, stability_min)


def calc_stability(board, symbol):
    other_symbol = SYMBOL_O if symbol == SYMBOL_X else SYMBOL_X
    stability_score = 0
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] == symbol:
                if (x, y) in CORNERS or (x, y) in EDGES:
                    stability_score += 1
                else:
                    stable = True
                    for x_dir, y_dir in ALL_POSSIBLE_DIRECTIONS:
                        x_curr, y_curr = x + x_dir, y + y_dir
                        if is_on_board(x_curr, y_curr) and board[y_curr][x_curr] == other_symbol:
                            stable = False
                            break
                    if stable:
                        stability_score += 1

    return stability_score


def calc_percent(score_max, score_min):
    if (score_min + score_max) != 0:
        return 100 * (score_max - score_min) / (score_max + score_min)
    return 0


def board_current_score(board, max_symbol, weights):
    score = 0
    score += weights["corners"] * corners(board, max_symbol)
    score += weights["mobility"] * mobility(board, max_symbol)
    score += weights["coin_parity"] * coin_parity(board, max_symbol)
    score += weights["edges"] * edges(board, max_symbol)
    score += weights["stability"] * stability(board, max_symbol)
    return score


def stable_strategy(board, max_symbol):
    weights = {"corners": 30,
               "mobility": 5,
               "coin_parity": 25,
               "edges": 10,
               "stability": 25}
    return board_current_score(board, max_symbol, weights)


def adaptive_strategy(board, max_symbol):
    score = calculate_score(board)
    num_pieces = score[SYMBOL_X] + score[SYMBOL_O]
    if num_pieces < 20:
        # most important mobility and coin_parity
        weights = {"corners": 15, "mobility": 15, "coin_parity": 30, "edges": 10, "stability": 5}
    elif num_pieces < 50:
        # all heuristics are important
        weights = {"corners": 20, "mobility": 20, "coin_parity": 20, "edges": 15, "stability": 25}
    else:
        # corners and stability are the most important
        weights = {"corners": 35, "mobility": 5, "coin_parity": 20, "edges": 15, "stability": 25}
    return board_current_score(board, max_symbol, weights)


STATIC_BOARD = [
    [ 4, -3,  2,  2,  2,  2, -3,  4],
    [-3, -4, -1, -1, -1, -1, -4, -3],
    [ 2, -1,  1,  0,  0,  1, -1,  2],
    [ 2, -1,  0,  1,  1,  0, -1,  2],
    [ 2, -1,  0,  1,  1,  0, -1,  2],
    [ 2, -1,  1,  0,  0,  1, -1,  2],
    [-3, -4, -1, -1, -1, -1, -4, -3],
    [ 4, -3,  2,  2,  2,  2, -3,  4]
]



def static_strategy(board, max_symbol):
    other_symbol = SYMBOL_O if max_symbol == SYMBOL_X else SYMBOL_X
    score_max = 0
    score_min = 0
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] == max_symbol:
                score_max += STATIC_BOARD[y][x]
            elif board[y][x] == other_symbol:
                score_min += STATIC_BOARD[y][x]

    return score_max - score_min
