BOARD_SIZE = 8
ALL_POSSIBLE_DIRECTIONS = [(1, 0), (1, 1), (1, -1), (0, 1), (0, -1), (-1, 0), (-1, 1), (-1, -1)]
BOARD = [
    # 0  1  2  3  4  5  6  7  x/ y
    [0, 0, 0, 0, 0, 0, 0, 0],  # 0
    [0, 0, 0, 0, 0, 0, 0, 0],  # 1
    [0, 0, 0, 1, 0, 0, 0, 0],  # 2
    [0, 0, 2, 1, 2, 0, 0, 0],  # 3
    [0, 0, 0, 2, 1, 0, 0, 0],  # 4
    [0, 0, 2, 1, 0, 0, 0, 0],  # 5
    [0, 0, 0, 0, 0, 0, 0, 0],  # 6
    [0, 0, 0, 0, 0, 0, 0, 0],  # 7
]


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


def board_score(board, symbol):
    other_symbol = 2 if symbol == 1 else 1
    flat_board = [val for row in board for val in row]
    score_symbol = flat_board.count(symbol)
    score_other = flat_board.count(other_symbol)
    return score_symbol - score_other


def make_move(board, symbol, move):
    x, y, cords_to_flip = move
    board[y][x] = symbol
    for x_flip, y_flip in cords_to_flip:
        board[y_flip][x_flip] = symbol

    return board


def print_board(board):
    print("    0  1  2  3  4  5  6  7 ")
    print("  +------------------------+")
    for i, row in enumerate(board):
        row_str = f"{i} |"
        for item in row:
            row_str += f" {'.XO'[item]} "
        row_str += "|"
        print(row_str)
    print("  +------------------------+")
    print()


if __name__ == '__main__':
    moves = calc_possible_moves(BOARD, 1)

    print(moves)
    for move in moves:
        BOARD[move[1]][move[0]] = 4

    for x in range(BOARD_SIZE):
        print(BOARD[x])
