from optimize import Population

project_list = {         # (price for minute, average minutes per day)
    0: ('Mitsubishi', 5, 300),
    1: ('Cian', 7, 450),
    2: ('Роспоребнадзор', 4, 260),
    3: ('Велодрайв', 9, 180),
    4: ('Сбербанк', 2, 240)
}
operators = {
    0: ('Коновалова С.', 200, [2, 5]),  # (salary per hour, [projects working at])
    1: ('Светов М.', 150, [1, 3]),
    2: ('Людов Г.', 250, [2, 4, 5]),
    3: ('Семиренко Д.', 170, [3, 4]),
    4: (' ', 230, [5])
}
p = Population(operators, project_list, 5000)
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
