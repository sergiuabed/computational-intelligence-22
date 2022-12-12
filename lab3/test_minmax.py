from minmax import *

if __name__ == "__main__":

    # minmax vs random
    heaps = Nim(N_HEAPS)
    Alice = MinMaxPlayer("Alice", minmax_strategy, 1)
    Bob = Player("Bob", random_strategy)
    winners = match(Alice, Bob, heaps, N_GAMES)
    print_match_result(Alice, Bob, winners)

    print("---------------------")

    # minmax vs minmax
    heaps = Nim(N_HEAPS)
    Alice = MinMaxPlayer("Alice", minmax_strategy, 1)
    Bob = MinMaxPlayer("Bob", minmax_strategy, 1)
    winners = match(Alice, Bob, heaps, N_GAMES)
    print_match_result(Alice, Bob, winners)