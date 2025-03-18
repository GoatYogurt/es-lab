from pysat.solvers import Glucose3
import math


def at_most_one_binomial(clauses, variables):
    for i in range(0, len(variables)):
        for j in range(i + 1, len(variables)):
            clauses.append([-variables[i], -variables[j]])


def at_least_one(clauses, variables):
    clauses.append(variables)


def exactly_one_binomial(clauses, variables):
    at_least_one(clauses, variables)
    at_most_one_binomial(clauses, variables)


def at_most_one_commander():




def solve_nqueens(n):
    with Glucose3() as g:
        vars = [[(i * n + j + 1) for j in range(n)] for i in range(n)]
        commanders = [i for i in range(
            n ** 2 + 1, n ** 2 + math.ceil(math.log(n ** 4, 2)) + 1)]
        clauses = []

        print(commanders)

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
