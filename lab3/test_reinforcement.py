from reinforcement_learning import *
from minmax import N_HEAPS, N_GAMES

def print_match_result(A: Player, B: Player, res: list):
    n_A_win = 0
    n_games = len(res)
    for i in range(n_games):
        if res[i][0] == A.name:
            n_A_win += 1
    print(f"{A.name} won {n_A_win} times\n{B.name} won {n_games - n_A_win} times")

heaps = Nim(N_HEAPS)
Alice = reinforcement_learning(heaps, "Alice")
Alice.explore = False
Bob = Player("Bob", nim_sum_strategy)
winners = match(Alice, Bob, heaps, N_GAMES)
print_match_result(Alice, Bob, winners)