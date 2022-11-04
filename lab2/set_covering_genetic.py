import random
import copy

def problem(N, seed=None):
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]

class Individual:
    # gene = list in the list of lists generated by "problem()"
    # genome = list of genes
    # individual = conceptually, it is a representation of a genome with some extra information (set of covered elements w/o repetitions, weight)
    # weight = nr of elements covered by considering the repetitions
    # fittness = -weight

    def __init__(self, genome: list):
        self.genome = genome
        self.representation = set()
        self.weight = 0

        for t in genome:
            self.representation.update(set(t))
            self.weight += len(t)

        #self.fitness = self.weight - len(self.representation)
        self.fitness = -self.weight

    @property
    def genome_copy(self):
        return copy.deepcopy(self.genome)

n = 100
SEED = 42
POPULATION_SIZE = 1000
OFFSPRING = 10
GENERATIONS = 1000

alleles = problem(N=n, seed=SEED)

#def initialize_population(alleles):    # IGNORE THIS
#    population = []
#    
#    i = 0
#    while i < POPULATION_SIZE:
#        weight = 0
#        genome = []
#        while weight < n:
#            allele = alleles[random.randint(0, len(alleles)-1)]
#            genome.append(allele)
#            weight += len(allele)
#
#        population.append(Individual(genome=genome))
#        i+=1
#
#    return population

def check_solution(genome):     # used for producing the first "generation" of individuals in the population
    s = set()                   # used also for checking if a new individual produced by mutation or recombination is a solution
    for l in genome:
        s.update(set(l))

    solutionRepr = set(range(0, n))

    return s == solutionRepr

def initialize_population(alleles):
    population = []
    
    i = 0
    while i < POPULATION_SIZE:
        genome = []
        while not check_solution(genome):
            allele = alleles[random.randint(0, len(alleles)-1)]
            genome.append(allele)

        population.append(Individual(genome=genome))
        i+=1

    return population
    
def mutation(ind: Individual):
    genome = ind.genome_copy
    locus = random.randint(0, len(genome)-1)

    new_allele = alleles[random.randint(0, len(alleles)-1)]

    genome[locus] = new_allele

    return Individual(genome=genome)

def recombination(ind1: Individual, ind2: Individual):
    genome1 = ind1.genome_copy
    genome2 = ind2.genome_copy
    new_genome = []

    splitIndex = random.randint(0, min(len(genome1), len(genome2)))

    new_genome.extend(genome1[:splitIndex])
    new_genome.extend(genome2[splitIndex:])

    return Individual(new_genome)

def tournament(population, tournament_size=2):
    return max(random.choices(population=population, k=tournament_size), key=lambda i: i.fitness)

def evolution(population):
    offspring = []
    for g in range(GENERATIONS):
        offspring = []
        for i in range(OFFSPRING):
            o = Individual([])
            if random.random() < 0.3:
                while not check_solution(o.genome):
                    p = tournament(population)
                    o = mutation(p)
            else:
                while not check_solution(o.genome):
                    p1 = tournament(population)
                    p2 = tournament(population)
                    o = recombination(p1, p2)
            
            offspring.append(o)
        population += offspring
        population = sorted(population, key = lambda i: i.fitness, reverse = True)[:POPULATION_SIZE]

    return population[0]

if __name__ == '__main__':
    population = initialize_population(alleles)
    
    solution = evolution(population)
    print("weight")
    print(solution.weight)
    print(solution.representation)
