from collections import namedtuple
from copy import deepcopy
from operator import xor
import random
from itertools import accumulate
from typing import Callable


Nimply = namedtuple("Nimply", "row, num_objects")

class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [i * 2 + 1 for i in range(num_rows)]
        self._k = k

    def __bool__(self):
        return sum(self._rows) > 0

    def __str__(self):
        return "<" + " ".join(str(_) for _ in self._rows) + ">"

    @property
    def rows(self) -> tuple:
        return tuple(self._rows)

    @property
    def k(self) -> int:
        return self._k

    def nimming(self, ply: Nimply) -> None:
        row, num_objects = ply
        assert self._rows[row] >= num_objects
        assert self._k is None or num_objects <= self._k
        self._rows[row] -= num_objects

# function used for "brute_force" (see "cook_status")
def nim_sum(state: Nim) -> int:
    *_, result = accumulate(state.rows, xor)
    return result

# cook_status returns a dict of rules used for evolving a solution
def cook_status(state: Nim) -> dict:
    cooked = dict()
    cooked["possible_moves"] = [
        (r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if state.k is None or o <= state.k
    ]
    cooked["active_rows_number"] = sum(o > 0 for o in state.rows)
    cooked["shortest_row"] = min((x for x in enumerate(state.rows) if x[1] > 0), key=lambda y: y[1])[0]
    cooked["longest_row"] = max((x for x in enumerate(state.rows)), key=lambda y: y[1])[0]
    cooked["nim_sum"] = nim_sum(state)

    brute_force = list()
    for m in cooked["possible_moves"]:
        tmp = deepcopy(state)
        tmp.nimming(m)
        brute_force.append((m, nim_sum(tmp)))
    cooked["brute_force"] = brute_force

    return cooked

# working solutions given by the professor. "pure_random" is used for evolving a solution based on rules
def pure_random(state: Nim) -> Nimply:
    row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
    num_objects = random.randint(1, state.rows[row])
    return Nimply(row, num_objects)

def optimal_startegy(state: Nim) -> Nimply:
   data = cook_status(state)
   return next((bf for bf in data["brute_force"] if bf[1] == 0), random.choice(data["brute_force"]))[0]


#def make_strategy(genome: dict) -> Callable:
#    def evolvable(state: Nim) -> Nimply:
#        data = cook_status(state)
#
#        if random.random() < genome["p"]:
#            ply = Nimply(data["shortest_row"], random.randint(1, state.rows[data["shortest_row"]]))
#        else:
#            ply = Nimply(data["longest_row"], random.randint(1, state.rows[data["longest_row"]]))
#
#        return ply
#
#    return evolvable


NUM_MATCHES = 100
NIM_SIZE = 10

def evaluate(strategy: Callable) -> float:
    opponent = (strategy, pure_random)
    won = 0

    for m in range(NUM_MATCHES):
        nim = Nim(NIM_SIZE)
        player = 0
        while nim:
            ply = opponent[player](nim)
            nim.nimming(ply)
            player = 1 - player
        if player == 1:
            won += 1
    return won / NUM_MATCHES