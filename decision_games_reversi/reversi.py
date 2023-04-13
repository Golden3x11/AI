BOARD_SIZE = 8
ALL_POSSIBLE_DIRECTIONS = [(1, 0), (1, 1), (1, -1), (0, 1), (0, -1), (-1, 0), (-1, 1), (-1, -1)]
CORNERS = [(0, 0), (0, BOARD_SIZE - 1), (BOARD_SIZE - 1, 0), (BOARD_SIZE - 1, BOARD_SIZE - 1)]
EDGES = [(0, i) for i in range(1, BOARD_SIZE - 1)] + \
        [(BOARD_SIZE - 1, i) for i in range(1, BOARD_SIZE - 1)] + \
        [(i, 0) for i in range(1, BOARD_SIZE - 1)] + \
        [(i, BOARD_SIZE - 1) for i in range(1, BOARD_SIZE - 1)]
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
    moves = [result for x in range(BOARD_SIZE) for y in range(BOARD_SIZE) if
             (result := is_valid_move(board, symbol, x, y))]
    return moves


def is_valid_move(board, symbol, x, y):
    if board[y][x] != 0 and is_on_board(x, y):
        return False
    other_symbol = 2 if symbol == 1 else 1
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
        SYMBOL_X: 0,
        SYMBOL_O: 0
    }
    flat_board = [val for row in board for val in row]
    score[SYMBOL_X] = flat_board.count(SYMBOL_X)
    score[SYMBOL_O] = flat_board.count(SYMBOL_O)
    return score

def is_game_over(board):
    if calc_possible_moves(board, SYMBOL_X) or calc_possible_moves(board, SYMBOL_O):
        return False
    else:
        return True

def corners(board, symbol):
    corner_count = 0
    for x, y in CORNERS:
        if board[y][x] == symbol:
            corner_count += 1
    return corner_count


def edges(board, symbol):
    edge_count = 0
    for x, y in EDGES:
        if board[y][x] == symbol:
            edge_count += 1
    return edge_count


def coin_parity(board, symbol):
    other_symbol = SYMBOL_O if symbol == SYMBOL_X else SYMBOL_X
    score = calculate_score(board)
    return score[symbol] - score[other_symbol]


def board_score(board, symbol):
    score = 0
    score += 10 * coin_parity(board, symbol)
    score += 500 * corners(board, symbol)
    score += 100 * edges(board, symbol)
    return score



if __name__ == '__main__':
    moves = calc_possible_moves(BOARD, 1)

    print(moves)
    for move in moves:
        BOARD[move[1]][move[0]] = 4

    for x in range(BOARD_SIZE):
        print(BOARD[x])
