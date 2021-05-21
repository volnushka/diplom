import random
import sys


def equation(x1, x2, x3, x4):
    f = x1 + 2 * x2 + 3 * x3 + 4 * x4
    return f


class Population:
    def __init__(self):  # generate 5 groups of 4 random numbers within an integer constraint interval
        self.compare_buffer = 0
        self.pairs = []
        self.specimens = []
        self.genes = []
        self.constraint = 30
        self.reversed_sum = 0
        self.coefficients = []
        self.probabilities = []
        self.offspring = []
        self.compare = []
        for a in range(5):
            self.ans = []
            for i in range(5):
                self.ans.append(random.randint(0, 1))
            self.genes.append(self.ans)
        print('All random integers (genes): ' + str(self.genes))

    def test(self, genes_list):  # generate 5 specimens out of the equation
        self.specimens = []
        self.coefficients = []
        for i in range(5):  # generate coefficients of viability
            a, b, c, d = genes_list[i][0], genes_list[i][1], genes_list[i][2], genes_list[i][3]
            print(a, b, c, d)
            self.specimens.append(equation(a, b, c, d))
            print('Specimens: ' + str(self.specimens))
            self.coefficients.append(abs(int(self.specimens[i]) - self.constraint))
            if self.coefficients[i] == 0: # the answer
                print('Done, the answer is {}'.format(genes_list[i]))
                sys.exit()
            self.reversed_sum += 1 / self.coefficients[i]   # get a sum of reversed coefficients
        x = sum(self.coefficients) / len(self.coefficients)
        self.compare.append(x)
        print('Coefficients of viability: ' + str(self.coefficients))
        print('Average fitness: ' + str(x))
        print('Reversed sum: ' + str(self.reversed_sum))

        self.probabilities = []
        for i in range(5):  # probability of each chromosome
            self.probabilities.append((1 / self.coefficients[i]) / self.reversed_sum)
        print('Probabilities: ' + str(self.probabilities))

    def breed(self, population):  # generate new offspring
        i = 0
        while i < 5:
            ch = random.choices(population=population, weights=self.probabilities, k=2)
            if ch[0] != ch[1]:
                self.pairs.append(ch)
                i += 1
            else:
                pass
        print('Pairs of parents: ' + str(self.pairs))

        self.offspring = []
        for i in range(5):
            crossover = random.choice([[self.pairs[i][0][:1] + self.pairs[i][1][1:]],
                                       [self.pairs[i][0][:2] + self.pairs[i][1][2:]],
                                       [self.pairs[i][0][:3] + self.pairs[i][1][3:]]])
            self.offspring.extend(crossover)
            print('Next generation: ' + str(self.offspring))

    def mutate(self): # change random digit in a random chromosome
        print(self.offspring)
        self.offspring[random.randint(0, 4)][random.randint(0, 3)] = random.randint(1, 30)
        print(self.offspring)
        self.compare_buffer = self.compare[1]
        p.compare = []
        p.test(p.offspring)
        p.compare.insert(0, self.compare_buffer)


# generate first population -> test -> breed -> get the offspring ->
# -> test the offspring -> get 2 average fitness coefficients
p = Population()
p.test(p.genes)
p.breed(p.genes)
p.test(p.offspring)


while True:
    while p.compare[1] < p.compare[0]: # mutate when offspring is less viable
        p.mutate()
    else: # breed when offspring is more viable
        p.breed(p.offspring)
        p.compare_buffer = p.compare[1]
        p.compare = []
        p.test(p.offspring)
        p.compare.insert(0, p.compare_buffer)
