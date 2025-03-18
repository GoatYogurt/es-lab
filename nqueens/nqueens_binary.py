from pysat.solvers import Glucose3
import math


def generate_binary_combinations(n):
    binary_combinations = []
    for i in range(int(math.pow(2, n))):
        binary_combinations.append(format(i, '0' + str(n) + 'b'))
    return binary_combinations


def at_least_one(clauses, variables):
    clauses.append(variables)


def at_most_one_binary(clauses, variables, new_variables, combinations):
    for i in range(len(variables)):  # at most one
        combination = combinations[i]
        index = 0
        for k in range(len(combination) - 1, -1, -1):
            if combination[k] == '0':
                clauses.append([-variables[i], -new_variables[index]])
                index += 1
            else:
                clauses.append([-variables[i], new_variables[index]])
                index += 1


def solve_nqueens(n):
    with Glucose3() as g:
        vars = [[(i * n + j + 1) for j in range(n)] for i in range(n)]
        new_vars = [i for i in range(
            n ** 2 + 1, n ** 2 + math.ceil(math.log(n ** 2, 2)) + 1)]
        print(new_vars)
        binary_combinations = generate_binary_combinations(n)
        # print(combinations)
        clauses = []

        # exactly one for each row
        for i in range(n):  # at least one
            at_least_one(clauses, vars[i])

        start = 0
        for i in range(n):  # at most one
            end = start + 4
            combinations = binary_combinations[start:end]
            print(combinations)
            at_most_one_binary(clauses, vars[i], new_vars, combinations)
            start += 4

        # exactly one for each column
        for j in range(n):  # at least one
            col = [vars[i][j] for i in range(n)]
            
            at_least_one(clauses, col)
            

        # at most one for each diagonal
        for i1 in range(n):
            for j1 in range(n):
                for i2 in range(n):
                    for j2 in range(n):
                        if (i1 != i2 and j1 != j2) and (abs(i1 - i2) == abs(j1 - j2)):
                            g.add_clause([-vars[i1][j1], -vars[i2][j2]])

        for clause in clauses:
            g.add_clause(clause)

        if g.solve():
            model = g.get_model()
            board = [['.' for _ in range(n)] for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    if vars[i][j] in model:
                        board[i][j] = 'Q'
            for row in board:
                print(' '.join(row))
        else:
            print("UNSATISFIABLE")


solve_nqueens(4)
