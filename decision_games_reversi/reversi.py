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
    moves = []
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            result = is_valid_move(board, symbol, x, y)
            if result:
                moves.append(result)
    return moves


def is_valid_move(board, symbol, x, y):
    if board[y][x] != 0 and is_on_board(x, y):
        return False
    other_symbol = 2 if symbol == 1 else 1
    change_symbol = []

    for x_next, y_next in ALL_POSSIBLE_DIRECTIONS:
        valid = []
        x_curr = x + x_next
        y_curr = y + y_next

        while is_on_board(x_curr, y_curr) and board[y_curr][x_curr] == other_symbol:
            valid.append((x_curr, y_curr))
            x_curr += x_next
            y_curr += y_next

        if is_on_board(x_curr, y_curr) and board[y_curr][x_curr] == symbol and valid:
            change_symbol.extend(valid)

    if change_symbol:
        return x, y, change_symbol
    else:
        return False


def is_on_board(x, y):
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE


if __name__ == '__main__':
    moves = calc_possible_moves(BOARD, 1)

    print(moves)
    for move in moves:
        BOARD[move[1]][move[0]] = 4

    for x in range(BOARD_SIZE):
        print(BOARD[x])
