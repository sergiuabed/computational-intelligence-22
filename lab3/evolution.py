from nim_utils import *
from collections import namedtuple

def greedy_pick(state: Nim) -> Nimply: # (not to be confused with Greedy Nim, which is a variation of how the game is played)
    # this rule assumes that every time the opponent makes a move, it will always take all the elements in a row, leaving it empty
    # In such a (very unlikely) situation, the player will also pick all the elements in a row ONLY IF there are n odd nr of active rows left. Otherwise,
    # it will leave only one element in the row, hoping that the opponent will empty that row (or any other) so that the nr of rows is odd.

    # if you think this rule is silly, you're right.
    greedy_ply= None
    game_status = cook_status(state)
    if game_status["active_rows_number"] % 2: # nr of active rows is odd
        index_val = [(i,v) for i, v in enumerate(state.rows) if v != 0] # discards empty rows
        indx = random.choice([i for (i,_) in index_val])

        greedy_ply = Nimply(indx, state.rows[indx]) # empty the chosen row
        #state.nimming(ply=greedy_ply)
        
    else:
        index_val = [(i,v) for i, v in enumerate(state.rows) if v != 0] # discards empty rows
        index_val2 = [(i,v) for i, v in index_val if v>1] # discards rows with only 1 element

        if len(index_val2) != 0:
            indx = random.choice([i for (i,_) in index_val2])
            greedy_ply = Nimply(indx, state.rows[indx]-1) # leave only one element in the chosen row
            #state.nimming(ply=greedy_ply)
        else:   # i.e., all rows have only one element. In this case, pick a random row and empty it.
            indx = random.choice([i for (i,_) in index_val])
            greedy_ply = Nimply(indx, state.rows[indx]) # empty the chosen row
            #state.nimming(ply=greedy_ply)
    
    return greedy_ply


def even_odd(state: Nim) -> Nimply:
    # pick a random row and remove from it an odd random nr of elements from it if the index of the row is odd. Otherwise, remove an even random nr of elements
    # this rule is even sillier...

    index = [i for i, v in enumerate(state.rows) if v!=0]

    row_i = random.choice(index)
    ply = None
    if row_i % 2:
        objPicked = 2*random.randint(0, state.rows[row_i]//2)+1
        if not state.rows[row_i] % 2:  # if state.rows[row_i] is even, then the "+1" could result in objPicked > state.rows[row_i]
            objPicked-=1

        ply = Nimply(row_i, objPicked)
        #state.nimming(ply)
    else:
        if state.rows[row_i]==1:
            objPicked = 1   # if row_i is even and the value at this index 1, an even value <1 can't be picked (0 would mean skipping the move, which is not allowed)
                            # so, we make an exception to the rule: in case row_i even and state.rows[row_i]=1, always pick 1 element
        else:
            objPicked = 2*random.randint(1, state.rows[row_i]//2)
        ply = Nimply(row_i, objPicked)
        #state.nimming(ply)
    
    return ply

def shy_pick(state: Nim) -> Nimply:
    # always pick only one object from a random row
    index = [i for i, v in enumerate(state.rows) if v!=0]

    row_i = random.choice(index)
    ply = Nimply(row_i, 1)
    #state.nimming(ply)
    return ply

# list of rules
rules = [pure_random, greedy_pick, even_odd, shy_pick]

# defining how a genome of an individual is structured
# each entry (locus) in the genome corresponds to the probability (gene) of a rule being used as a ply made by the player
Genome = namedtuple("Genome", "pure_random_p, greedy_p, even_odd_p, shy_pick") # here, genes are the probabilities of the rules, not the rules themselves

def initialize_population(size) -> list:
    population = []
    i=0
    while i<size:
        g = Genome(random.randint(0, 10), random.randint(0, 10), random.randint(0, 10), random.randint(0, 10))
        g = Genome(*[x/sum(g) for x in g]) # computing the probabilities. They sum to 1.
        population.append(g)

        i+=1

    return population

def mutation(g: Genome) -> Genome:  # generate a new gene (probability) and place it in a random locus. Then, renormalize the genes, so that the probabilities sum up to 1
    locus = random.randint(0, len(g)-1)
    new_gene = random.uniform(0, 1)

    g_new = list(g)
    g_new[locus] = new_gene
    g_new = Genome(*[x/sum(g_new) for x in g_new])

    return g_new

def recombination(g1: Genome, g2: Genome) -> Genome:
    split = random.randint(1, len(g1)-1)    
    new_genome = Genome(*g1[:split], *g2[split:])
    new_genome = Genome(*[x/sum(new_genome) for x in new_genome])

    return new_genome

def sample_distribution(g: Genome) -> list:
    # defines a distribution based on the probabilities and samples it
    loci = [i for i in range(len(g))]
    sample = random.choices(loci, g, k=1)

    return sample.pop()     # sample is a list of 1 element, since "random.choices()" returns a list

def make_strategy(g: Genome) -> Callable:
    def strategy(state: Nim) -> Nimply:
        return rules[sample_distribution(g=g)](state)

    return strategy

def fitness(g: Genome) -> float:
    strategy = make_strategy(g=g)
    return evaluate(strategy=strategy)

def tournament(population, tournament_size=20):
    return max(random.choices(population=population, k=tournament_size), key=lambda i: fitness(i))

POPULATION_SIZE = 10
OFFSPRING = 5
GENERATIONS = 10

def evolution(population):
    offspring = []
    for g in range(GENERATIONS):
        offspring = []
        for i in range(OFFSPRING):
            o = None
            if random.random() < 0.3:
                p = tournament(population)
                o = mutation(p)
            else:
                p1 = tournament(population)
                p2 = tournament(population)
                o = recombination(p1, p2)
            
            offspring.append(o)
        population += offspring
        population = sorted(population, key = lambda i: fitness(i), reverse = True)[:POPULATION_SIZE]

    return population[0]


