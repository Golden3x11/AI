import alpha_beta
import reversi
import minimax


def get_computer_move(board, symbol):
    return alpha_beta.get_move(board, symbol, reversi.adaptive_strategy)


def play_game():
    board = reversi.BOARD
    current_player = reversi.SYMBOL_X

    while not reversi.is_game_over(board):
        if current_player == reversi.SYMBOL_X:
            move = get_computer_move(board, reversi.SYMBOL_X)
        else:
            move = get_computer_move(board, reversi.SYMBOL_O)
        if move:
            reversi.make_move(board, current_player, move)
        current_player = reversi.SYMBOL_X if current_player == reversi.SYMBOL_O else reversi.SYMBOL_O

    reversi.print_board(board)
    score = reversi.calculate_score(board)
    if score[reversi.SYMBOL_X] > score[reversi.SYMBOL_O]:
        print("Player ⚪ wins!")
    elif score[reversi.SYMBOL_X] < score[reversi.SYMBOL_O]:
        print("Player ⚫ wins!")
    else:
        print("Tie game!")


if __name__ == '__main__':
    play_game()
