from minimax import get_move, make_move
import reversi

SYMBOL_1 = 1
SYMBOL_2 = 2

if __name__ == '__main__':
    board = reversi.BOARD

    reversi.print_board(board)

    move = get_move(board, SYMBOL_1, reversi.board_score)
    print(move)
    print()
    make_move(board, SYMBOL_1, move)

    reversi.print_board(board)
