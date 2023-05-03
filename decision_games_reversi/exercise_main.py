import copy
import random
from decision_games_reversi import alpha_beta, heuristics, minimax, reversi

STRATEGIES = {
    'Random Move': lambda b, s: random.choice(reversi.calc_possible_moves(b, s)) if reversi.calc_possible_moves(b, s) else None,
    'Alpha-Beta (Adaptive)': lambda board, symbol: alpha_beta.get_move(board, symbol, heuristics.adaptive_strategy),
    'Alpha-Beta (Stable)': lambda board, symbol: alpha_beta.get_move(board, symbol, heuristics.stable_strategy),
    'Alpha-Beta (Static)': lambda board, symbol: alpha_beta.get_move(board, symbol, heuristics.static_strategy)
}

def play_game(player1, player2):
    board = reversi.BOARD
    board = copy.deepcopy(board)
    current_player = reversi.SYMBOL_X

    while not reversi.is_game_over(board):
        if current_player == reversi.SYMBOL_X:
            move = player1(board, current_player)
        else:
            move = player2(board, current_player)
        if move:
            reversi.make_move(board, current_player, move)
        current_player = reversi.SYMBOL_X if current_player == reversi.SYMBOL_O else reversi.SYMBOL_O

    score = reversi.calculate_score(board)
    if score[reversi.SYMBOL_X] > score[reversi.SYMBOL_O]:
        return 1
    elif score[reversi.SYMBOL_X] < score[reversi.SYMBOL_O]:
        return -1
    else:
        return 0


if __name__ == '__main__':
    player_results = {}
    for p1_name, p1_strategy in STRATEGIES.items():
        for p2_name, p2_strategy in STRATEGIES.items():
            if p1_name == p2_name:
                continue
            if p1_name not in player_results:
                player_results[p1_name] = {"wins": 0, "losses": 0, "ties": 0, "matches": []}
            if p2_name not in player_results:
                player_results[p2_name] = {"wins": 0, "losses": 0, "ties": 0, "matches": []}
            p1_wins, p2_wins, ties = 0, 0, 0
            result = play_game(p1_strategy, p2_strategy)
            if result == 0:
                player_results[p1_name]["ties"] += 1
                player_results[p2_name]["ties"] += 1
                player_results[p1_name]["matches"].append(f"{p1_name} vs {p2_name}: Tie")
                player_results[p2_name]["matches"].append(f"{p1_name} vs {p2_name}: Tie")
            elif result == 1:
                player_results[p1_name]["wins"] += 1
                player_results[p2_name]["losses"] += 1
                player_results[p1_name]["matches"].append(f"{p1_name} vs {p2_name}: Win")
                player_results[p2_name]["matches"].append(f"{p1_name} vs {p2_name}: Lose")
            elif result == -1:
                player_results[p1_name]["losses"] += 1
                player_results[p2_name]["wins"] += 1
                player_results[p1_name]["matches"].append(f"{p1_name} vs {p2_name}: Lose")
                player_results[p2_name]["matches"].append(f"{p1_name} vs {p2_name}: Win")

    for item in player_results.items():
        print(item)
