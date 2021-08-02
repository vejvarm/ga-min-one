import math
import random
from MinOne import MinOne
from helpers import dot, element_sum, cumsum


class Problem:

    def __init__(self):
        self.costFun = MinOne()
        self.nVar = 100


class Params:

    def __init__(self):
        self.maxIt = 50
        self.nPop = 100

        self.beta = 5.  # best parent selection pressure (higher beta == good parents selected more often)
        self.pC = 1.  # parent crossover ratio (percentage)
        self.mu = 0.02  # mutation ratio (percentage of genes to be mutated)


class Individual:

    def __init__(self, position, cost_fun):
        self.position = position
        self.cost = cost_fun(self.position)

        self._cost_fun = cost_fun

    def set_position(self, position):
        self.position = position
        self.cost = self._cost_fun(self.position)


# run Genetic algorithm
def run(problem, params):

    # problem
    cost_fun = problem.costFun
    nVar = problem.nVar

    # params
    maxIt = params.maxIt
    nPop = params.nPop
    beta = params.beta
    pC = params.pC
    nC = int(pC*nPop/2)*2  # number of children (has to be even)
    mu = params.mu  # mutation ratio

    # Best solution ever found
    best_pop = Individual([1]*nVar, cost_fun)

    # 1. Initialization
    pop = []
    for _ in range(nPop):
        pop.append(Individual([random.randint(0, 1) for _ in range(nVar)], cost_fun))

        # Compare to best solution ever found
        if pop[-1].cost < best_pop.cost:
            best_pop = pop[-1]

    # best cost of iterations
    best_costs = [None]*maxIt

    # main loop
    for it in range(maxIt):
        popc = []  # children
        # Initialize offsprings (children)
        for _ in range(nC//2):
            popc.append((Individual([random.randint(0, 1) for _ in range(nVar)], cost_fun),
                        Individual([random.randint(0, 1) for _ in range(nVar)], cost_fun)))

        # Crossover
        for k in range(nC//2):

            # select parents (randomly)
            p1 = roulette_wheel(pop, beta)
            p2 = roulette_wheel(pop, beta)
            # p1, p2 = random.sample(pop, 2)

            # perform crossover
            x1 = p1.position
            x2 = p2.position
            popc[k][0].position, popc[k][1].position = uniform_crossover(x1, x2)

        # flatten children back to single column
        popc = [p for pp in popc for p in pp]

        # Mutation of offsprings
        for c in popc:
            # perform mutation and update cost (evaluation)
            c.set_position(mutate(c.position, mu))

            # compare solution to best solution ever found
            if c.cost < best_pop.cost:
                best_pop = c

        # update best cost of iteration
        best_costs[it] = best_pop.cost

        # merge and sort population
        pop = sort_population([*pop, *popc])

        # remove extra individuals
        pop = pop[:nPop]

        # print best results
        print(f"Iteration: {it} | best_cost: {best_costs[it]}")

    return best_pop, best_costs


def single_point_crossover(x1, x2):
    # randomly select cross point position
    n_var = len(x1)
    j = random.randint(0, n_var-1)

    y1 = [*x1[:j], *x2[j:]]
    y2 = [*x2[:j], *x1[j:]]

    return y1, y2


def uniform_crossover(x1, x2):
    mask = [random.randint(0, 1) for _ in range(len(x1))]
    not_mask = [1-m for m in mask]

    y1 = element_sum(dot(x1, mask), dot(x2, not_mask))
    y2 = element_sum(dot(x2, mask), dot(x1, not_mask))

    return y1, y2


def mutate(x, mu):
    y = []
    for g in x:
        m = random.random()
        if m < mu:
            y.append(1 - g)
        else:
            y.append(g)

    return y


def sort_population(pop):
    sorted_pop = sorted(enumerate(pop), key=lambda x: x[1].cost)
    return [p[1] for p in sorted_pop]


def roulette_wheel(pop, beta):
    cst = [p.cost for p in pop]
    avgc = sum(cst)/len(cst)
    if avgc == 0:
        avgc = 1
    probs = [math.exp(-beta*c/avgc) for c in cst]
    probs = [p/sum(probs) for p in probs]
    cumprobs = cumsum(probs)
    selection = random.random()
    for i in range(len(cumprobs)):
        if selection < cumprobs[i]:
            return pop[i]


if __name__ == '__main__':
    # Problem definition
    problem = Problem()

    # GA Parameters
    params = Params()

    # Run GA
    best_pop, best_costs = run(problem, params)