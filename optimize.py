import random
import sys

project_list = {         # (price for minute, average minutes per day)
    1: ('Mitsubishi', 5, 300),
    2: ('Cian', 7, 450),
    3: ('Роспоребнадзор', 4, 260),
    4: ('Велодрайв', 9, 180),
    5: ('Сбербанк', 2, 240)
}
operators = {
    0: ('Коновалова С.', 200, [2, 5]),  # (salary per hour, [projects working at])
    1: ('Светов М.', 150, [1, 3]),
    2: ('Людов Г.', 250, [2, 4, 5]),
    3: ('Семиренко Д.', 170, [3, 4])
}


class Population:
    def __init__(self, constraint):
        self.total = 0
        self.compare_buffer = 0
        self.pairs = []
        self.specimens = []
        self.genes = []
        self.constraint = constraint
        self.reversed_sum = 0
        self.coefficients = []
        self.probabilities = []
        self.offspring = []
        self.compare = []
        self.generation_counter = 0
        for a in range(5):
            self.ancestors = []
            for i in range(4):
                self.ancestors.append(random.randint(3, 12))
            self.genes.append(self.ancestors)
        print('All random integers (genes): ' + str(self.genes))

    def count_income(self, random_hours):
        self.total = 0
        for operator in operators.items():  # 1: (a, 100, [1, 2 ...])
            operator_projects = []
            operator_income = 0
            time = random_hours[operator[0]]
            for project in project_list.keys():  # 1, 2 ...
                if project in operator[1][2]:
                    operator_projects.append(project)
                    operator_income += project_list[project][1] * project_list[project][2]
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
        for i in range(5):  # number of specimens generated
            test_genes = []
            for j in range(4):
                test_genes.append(genes_list[i][j])
            # print("Test genes are".format(test_genes))
            self.specimens.append(self.count_income(test_genes))
            self.coefficients.append(abs(int(self.specimens[i]) - self.constraint))
            if self.coefficients[i] < 10:  # the answer
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
        for i in range(5):  # probability of each chromosome
            self.probabilities.append((1 / self.coefficients[i]) / self.reversed_sum)
        # print('Probabilities: ' + str(self.probabilities))

    def breed(self, population):  # generate new offspring
        i = 0
        while i < 5:
            ch = random.choices(population=population, weights=self.probabilities, k=2)
            if ch[0] != ch[1]:
                self.pairs.append(ch)
                i += 1
            else:
                pass
        # print('Pairs of parents: ' + str(self.pairs))
        self.offspring = []
        for i in range(5):
            crossover = random.choice([[self.pairs[i][0][:1] + self.pairs[i][1][1:]],
                                       [self.pairs[i][0][:2] + self.pairs[i][1][2:]],
                                       [self.pairs[i][0][:3] + self.pairs[i][1][3:]]])
            self.offspring.extend(crossover)
        self.generation_counter += 1
        # print('Next generation: ' + str(self.offspring))

    def mutate(self):  # change random digit in a random chromosome
        # print(self.offspring)
        self.offspring[random.randint(0, 4)][random.randint(0, 3)] = random.randint(3, 12)
        # print(self.offspring)
        self.compare_buffer = self.compare[1]
        p.compare = []
        p.test(p.offspring)
        p.compare.insert(0, self.compare_buffer)


p = Population(8000)
# p.count_income(p.genes)
p.test(p.genes)
p.breed(p.genes)
p.test(p.offspring)
while True:
    while p.compare[1] < p.compare[0]:  # mutate when offspring is less viable
        p.mutate()
    else:  # breed when offspring is more viable
        p.breed(p.offspring)
        p.compare_buffer = p.compare[1]
        p.compare = []
        p.test(p.offspring)
        p.compare.insert(0, p.compare_buffer)
