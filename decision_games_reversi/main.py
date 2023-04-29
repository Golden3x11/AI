from decision_games_reversi import reversi
from decision_games_reversi import alpha_beta
from decision_games_reversi import minimax


def get_computer_move(board, symbol):
    return alpha_beta.get_move(board, symbol, reversi.adaptive_strategy)


def get_user_move(board, symbol):
    move = alpha_beta.get_move(board, symbol, reversi.adaptive_strategy)
    print("Suggested move:", (move[0], move[1]))
    valid_moves = reversi.calc_possible_moves(board, symbol)
    print("Valid moves:", [(x, y) for x, y, flipped in valid_moves])
    move = None
    while move not in valid_moves:
        move_str = input("Enter your move (in the format of row, col): ").strip()
        move = tuple(map(int, move_str.split(',')))
        move = (move[0], move[1], [])
        for x, y, flipped in valid_moves:
            if x == move[0] and y == move[1]:
                move = (x, y, flipped)
                break

    return move


def play_game():
    board = reversi.BOARD
    current_player = reversi.SYMBOL_X

    while not reversi.is_game_over(board):
        reversi.print_board(board)

        if current_player == reversi.SYMBOL_X:
            print("Player ⚪'s turn:")
            move = get_computer_move(board, reversi.SYMBOL_X)
        else:
            print("Player ⚫'s turn.")
            move = get_computer_move(board, reversi.SYMBOL_O)
            
        if move:
            print(f"Move: ({move[0]}, {move[1]})")
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
