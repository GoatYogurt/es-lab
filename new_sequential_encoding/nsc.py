from pysat.solvers import Glucose3


def generate_variables(n):
    """
    Generate variables from 1 to n (not n - 1)
    """
    return [i for i in range(0, n + 1)]


def ij_to_R(i, j, R_list):
    """
    Return the variable at position (i, j).

    :param i: the row index for R. i is 1-indexed.
    :param j: the column index for R. j in 1-indexed. jth position return the last element in row (bit-packing).
    """
    row = R_list[i - 1]
    return row[len(row) - j]


def get_next_variable(current):
    return current + 1


def generate_new_variables(n, k):
    rows, cols = n - 1, k
    arr = []
    current = n + 1
    for i in range(rows):
        col = [0] * cols  # Initialize the column with zeros
        fill_count = min(i + 1, cols)
        for j in range(fill_count):
            col[cols - fill_count + j] = current
            current += 1
        arr.append(col)
    return arr


def generate_clauses_1(n: int, clauses: list, variables: list, R_list: list):
    for i in range(1, n):
        clauses.append([-variables[i], ij_to_R(i, 1, R_list)])


def generate_clauses_2(n: int, k: int, clauses: list, R_list: list):
    for i in range(2, n):
        for j in range(1, min(i - 1, k) + 1):
            clauses.append([-ij_to_R(i - 1, j, R_list), ij_to_R(i, j, R_list)])


def generate_clauses_3(n: int, k: int, variables: list, clauses: list, R_list: list):
    for i in range(2, n):
        for j in range(2, min(i, k) + 1):
            clauses.append([-variables[i], -ij_to_R(i - 1, j - 1, R_list), ij_to_R(i, j, R_list)])


def generate_clauses_4(n: int, k: int, variables: list, clauses: list, R_list: list):
    for i in range(2, n):
        for j in range(1, min(i - 1, k) + 1):
            clauses.append([variables[i], ij_to_R(i - 1, j, R_list), -ij_to_R(i, j, R_list)])


def generate_clauses_5(k: int, clauses: list, variables: list, R_list: list):
    for i in range(1, k + 1):
        clauses.append([variables[i], -ij_to_R(i, i, R_list)])


def generate_clauses_6(n: int, k: int, clauses: list, R_list: list):
    for i in range(2, n):
        for j in range(2, min(i, k) + 1):
            clauses.append([ij_to_R(i - 1, j - 1, R_list), -ij_to_R(i, j, R_list)])


def generate_clauses_7(n: int, k: int, clauses: list, R_list: list, variables: list):
    if k == 1:
        return
    clauses.append([ij_to_R(n - 1, k, R_list), variables[n]])
    clauses.append([ij_to_R(n - 1, k, R_list), ij_to_R(n - 1, k - 1, R_list)])


def generate_clauses_8(n: int, k: int, R_list: list, variables: list, clauses: list):
    for i in range(k + 1, n + 1):
        clauses.append([-variables[i], -ij_to_R(i - 1, k, R_list)])


def at_least_k(n: int, k: int, R_list: list, variables: list, clauses: list):
    generate_clauses_1(n, clauses, variables, R_list)
    generate_clauses_2(n, k, clauses, R_list)
    generate_clauses_3(n, k, variables, clauses, R_list)
    generate_clauses_4(n, k, variables, clauses, R_list)
    generate_clauses_5(k, clauses, variables, R_list)
    generate_clauses_6(n, k, clauses, R_list)
    generate_clauses_7(n, k, clauses, R_list, variables)


def at_most_k(n: int, k: int, R_list: list, variables: list, clauses: list):
    generate_clauses_1(n, clauses, variables, R_list)
    generate_clauses_2(n, k, clauses, R_list)
    generate_clauses_3(n, k, variables, clauses, R_list)
    generate_clauses_8(n, k, R_list, variables, clauses)


def exactly_k(n: int, k: int, R_list: list, variables: list, clauses: list):
    generate_clauses_1(n, clauses, variables, R_list)
    generate_clauses_2(n, k, clauses, R_list)
    generate_clauses_3(n, k, variables, clauses, R_list)
    generate_clauses_4(n, k, variables, clauses, R_list)
    generate_clauses_5(k, clauses, variables, R_list)
    generate_clauses_6(n, k, clauses, R_list)
    generate_clauses_7(n, k, clauses, R_list, variables)
    generate_clauses_8(n, k, R_list, variables, clauses)


def test(n, k):
    variables = generate_variables(n)
    R_list = generate_new_variables(n, k)
    # print(R_list)
    clauses = []

    # at_least_k(n, k, R_list, variables, clauses)
    at_most_k(n, k, R_list, variables, clauses)
    # exactly_k(n, k, R_list, variables, clauses)
    # print(clauses)

    with Glucose3() as g:
        for clause in clauses:
            g.add_clause(clause)

        if g.solve():
            model = g.get_model()
            print(model)
            for i in model:
                if i > 0 and i <= 10:
                    print(i)
        else:
            print("UNSATISFIABLE")


test(10, 7)