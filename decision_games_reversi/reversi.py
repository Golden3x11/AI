BOARD_SIZE = 8
ALL_POSSIBLE_DIRECTIONS = [(1, 0), (1, 1), (1, -1), (0, 1), (0, -1), (-1, 0), (-1, 1), (-1, -1)]
CORNERS = [(0, 0), (0, BOARD_SIZE - 1), (BOARD_SIZE - 1, 0), (BOARD_SIZE - 1, BOARD_SIZE - 1)]
EDGES = [(0, i) for i in range(2, BOARD_SIZE - 2)] + \
        [(BOARD_SIZE - 1, i) for i in range(2, BOARD_SIZE - 2)] + \
        [(i, 0) for i in range(2, BOARD_SIZE - 2)] + \
        [(i, BOARD_SIZE - 1) for i in range(2, BOARD_SIZE - 2)]
BOARD = [
    # 0  1  2  3  4  5  6  7  x/ y
    [0, 0, 0, 0, 0, 0, 0, 0],  # 0
    [0, 0, 0, 0, 0, 0, 0, 0],  # 1
    [0, 0, 0, 0, 0, 0, 0, 0],  # 2
    [0, 0, 0, 1, 2, 0, 0, 0],  # 3
    [0, 0, 0, 2, 1, 0, 0, 0],  # 4
    [0, 0, 0, 0, 0, 0, 0, 0],  # 5
    [0, 0, 0, 0, 0, 0, 0, 0],  # 6
    [0, 0, 0, 0, 0, 0, 0, 0],  # 7
]

SYMBOL_X = 1
SYMBOL_O = 2
SYMBOL_NONE = 0


def calc_possible_moves(board, symbol):
    return [result for x in range(BOARD_SIZE) for y in range(BOARD_SIZE) if
            (result := is_valid_move(board, symbol, x, y))]


def is_valid_move(board, symbol, x, y):
    if board[y][x] != SYMBOL_NONE and is_on_board(x, y):
        return False
    other_symbol = SYMBOL_O if symbol == SYMBOL_X else SYMBOL_X
    change_symbol = []

    for x_dir, y_dir in ALL_POSSIBLE_DIRECTIONS:
        valid = []
        x_curr, y_curr = x + x_dir, y + y_dir

        while is_on_board(x_curr, y_curr) and board[y_curr][x_curr] == other_symbol:
            valid.append((x_curr, y_curr))
            x_curr += x_dir
            y_curr += y_dir

        if is_on_board(x_curr, y_curr) and board[y_curr][x_curr] == symbol and valid:
            change_symbol.extend(valid)

    if change_symbol:
        return x, y, change_symbol
    return False


def is_on_board(x, y):
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE


def make_move(board, symbol, move):
    x, y, cords_to_flip = move
    board[y][x] = symbol
    for x_flip, y_flip in cords_to_flip:
        board[y_flip][x_flip] = symbol

    return board


def print_board(board):
    print("     0   1   2   3   4    5   6   7 ")
    print("  +----------------------------------+")
    for i, row in enumerate(board):
        row_str = f"{i} |"
        for item in row:
            row_str += f" {['🟫', '⚪', '⚫'][item]} "
        row_str += "|"
        print(row_str)
    print("  +----------------------------------+")
    print()


def calculate_score(board):
    score = {
        SYMBOL_X: sum(row.count(SYMBOL_X) for row in board),
        SYMBOL_O: sum(row.count(SYMBOL_O) for row in board)
    }
    return score


def is_game_over(board):
    if calc_possible_moves(board, SYMBOL_X) or calc_possible_moves(board, SYMBOL_O):
        return False
    else:
        return True


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


def calc_percent(score_max, score_min):
    if (score_min + score_max) != 0:
        return 100 * (score_max - score_min) / (score_max + score_min)
    return 0


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


def board_current_score(board, max_symbol, weights):
    score = 0
    score += weights["corners"] * corners(board, max_symbol)
    score += weights["mobility"] * mobility(board, max_symbol)
    score += weights["coin_parity"] * coin_parity(board, max_symbol)
    score += weights["edges"] * edges(board, max_symbol)
    score += weights["stability"] * stability(board, max_symbol)
    return score


def stable_strategy(board, max_symbol):
    weights = {"corners": 30, "mobility": 5, "coin_parity": 25, "edges": 10, "stability": 25}
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
        weights = {"corners": 35, "mobility": 10, "coin_parity": 20, "edges": 10, "stability": 25}
    return board_current_score(board, max_symbol, weights)
