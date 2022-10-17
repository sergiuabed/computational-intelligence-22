from gx_utils import *
from utilities import *
import random

def problem(N, seed=None):
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]
if __name__ == '__main__':
    seed = 42
    N = 20

    l = problem(N, seed)
    initialState = State([[]])

    state_cost = dict()
    parent_state = dict()
    goal_test = lambda s: s == State([list(range(0, N))])

    #path = search(initialState, set(range(0, 5)), dict(), dict(), lambda x : len(state_cost))
    path, cost = search(initialState, goal_test = goal_test, parent_state = parent_state, state_cost = state_cost, priority_function = lambda s : len(state_cost), unit_cost=lambda s : len(s), lists=l)

    print(path)
    print(cost)
    
    
    #st = State(l[0])
    #print(st)
    #dict1={}
    #dict1[st]='hello there'
    #print(dict1)

