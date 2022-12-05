from nim_utils import *
from evolution import *

if __name__ == '__main__':
    #state = Nim(5)
    #print(state)
    #game_status = cook_status(state)
    #print(f"active rows: {game_status['active_rows_number']}")
    #shy_pick(state)
    #print(state)
    #game_status = cook_status(state)
    #print(f"active rows: {game_status['active_rows_number']}")
#
    #shy_pick(state)
    #print(state)
    #game_status = cook_status(state)
    #print(f"active rows: {game_status['active_rows_number']}")

    first_population = initialize_population(POPULATION_SIZE)
    best_individual = evolution(first_population)

    print(best_individual)
    print(fitness(best_individual))