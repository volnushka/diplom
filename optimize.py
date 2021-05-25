import random
import sys


class Population:
    def __init__(self, operators, project_list, constraint):
        self.total = 0
        self.compare_buffer = 0
        self.pairs = []
        self.specimens = []
        self.ancestors = []
        self.constraint = constraint
        self.operators = operators
        self.project_list = project_list
        self.reversed_sum = 0
        self.coefficients = []
        self.probabilities = []
        self.offspring = []
        self.compare = []
        self.generation_counter = 1
        for a in range(5):  # number of ancestors
            self.genes = []
            for i in range(5):  # number of chromosomes in an ancestor
                self.genes.append(random.randint(3, 12))
            self.ancestors.append(self.genes)
        print('All random integers (genes): ' + str(self.ancestors))

    def count_income(self, random_hours):
        self.total = 0
        for operator in self.operators.items():  # 1: (a, 100, [1, 2 ...])
            operator_projects = []
            operator_income = 0
            time = random_hours[operator[0]]
            for project in self.project_list.keys():  # 1, 2 ...
                if project in operator[1][2]:
                    operator_projects.append(project)
                    operator_income += self.project_list[project][1] * self.project_list[project][2]
            final_income = operator_income - operator[1][1] * time
            # print("{0}\nHours: {1}\n".
            #       format(op[1][0], time))
            self.total += final_income
        # print(self.global_income)
        # print(self.genes)
        return self.total

    def test(self, genes_list):  # generate 5 specimens out of the equation
        self.specimens = []
        self.coefficients = []
        for i in range(len(self.ancestors)):  # number of specimens generated
            test_genes = []
            for j in range(len(self.ancestors)):
                test_genes.append(genes_list[i][j])
            # print("Test genes are".format(test_genes))
            self.specimens.append(self.count_income(test_genes))
            self.coefficients.append(abs(int(self.specimens[i]) - self.constraint))
            if self.coefficients[i] < 100:  # the answer
                print('Done, the answer is {}'.format(genes_list[i]))
                sys.exit()
            self.reversed_sum += 1 / self.coefficients[i]   # get a sum of reversed coefficients
        print('Generation: {0}\nSpecimens: {1}\n'.format(self.generation_counter, self.specimens))
        x = sum(self.coefficients) / len(self.coefficients)
        self.compare.append(x)
        # print('Coefficients of viability: ' + str(self.coefficients))
        # print('Average fitness: ' + str(x))
        # print('Reversed sum: ' + str(self.reversed_sum))

        self.probabilities = []
        for i in range(len(self.ancestors)):  # probability of each chromosome
            self.probabilities.append((1 / self.coefficients[i]) / self.reversed_sum)
        # print('Probabilities: ' + str(self.probabilities))

    def breed(self, population):  # generate new offspring
        print('Breeding...')
        i = 0
        while i < len(self.ancestors):
            ch = random.choices(population=population, weights=self.probabilities, k=2)
            if ch[0] != ch[1]:
                self.pairs.append(ch)
                i += 1
        # print('Pairs of parents: ' + str(self.pairs))
        self.offspring = []
        for i in range(len(self.ancestors)):
            crossover = random.choice([[self.pairs[i][0][:1] + self.pairs[i][1][1:]],
                                       [self.pairs[i][0][:2] + self.pairs[i][1][2:]],
                                       [self.pairs[i][0][:3] + self.pairs[i][1][3:]]])
            self.offspring.extend(crossover)
        self.generation_counter += 1
        # print('Next generation: ' + str(self.offspring))

    def mutate(self):  # change random digit in a random chromosome
        print('Mutating...')
        self.offspring[random.randint(0, 4)][random.randint(0, 4)] = random.randint(3, 12)
        # print(self.offspring)
        self.compare_buffer = self.compare[1]
        self.compare = []
        self.test(self.offspring)
        self.compare.insert(0, self.compare_buffer)
