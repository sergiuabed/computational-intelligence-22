from nim_utils import *
from evolution import *

if __name__ == '__main__':

    first_population = initialize_population(POPULATION_SIZE)
    best_individual = evolution(first_population)

    print(best_individual)
    print(fitness(best_individual))