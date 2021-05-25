from optimize import Population

p = Population(5000)
# p.count_income(p.genes)
p.test(p.ancestors)
p.breed(p.ancestors)
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
