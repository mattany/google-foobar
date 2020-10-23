import copy

right_options = [{0, 1, 4, 5}, {2, 3, 6, 7}, {0, 1, 4, 5}, {2, 3, 6, 7},
                 {8, 9, 12, 13}, {10, 11, 14, 15}, {8, 9, 12, 13}, {10, 11, 14, 15},
                 {0, 1, 4, 5}, {2, 3, 6, 7}, {0, 1, 4, 5}, {2, 3, 6, 7},
                 {8, 9, 12, 13}, {10, 11, 14, 15}, {8, 9, 12, 13}, {10, 11, 14, 15}
                 ]
down_options = [{0, 1, 2, 3}, {4, 5, 6, 7}, {8, 9, 10, 11}, {12, 13, 14, 15},
                {0, 1, 2, 3}, {4, 5, 6, 7}, {8, 9, 10, 11}, {12, 13, 14, 15},
                {0, 1, 2, 3}, {4, 5, 6, 7}, {8, 9, 10, 11}, {12, 13, 14, 15},
                {0, 1, 2, 3}, {4, 5, 6, 7}, {8, 9, 10, 11}, {12, 13, 14, 15}
                ]
up_options = [{0, 4, 8, 12}, {0, 4, 8, 12}, {0, 4, 8, 12}, {0, 4, 8, 12},
              {1, 5, 9, 13}, {1, 5, 9, 13}, {1, 5, 9, 13}, {1, 5, 9, 13},
              {2, 6, 10, 14}, {2, 6, 10, 14}, {2, 6, 10, 14}, {2, 6, 10, 14},
              {3, 7, 11, 15}, {3, 7, 11, 15}, {3, 7, 11, 15}, {3, 7, 11, 15}]

left_options = [{0, 2, 8, 10}, {0, 2, 8, 10}, {1, 3, 9, 11}, {1, 3, 9, 11},
                {0, 2, 8, 10}, {0, 2, 8, 10}, {1, 3, 9, 11}, {1, 3, 9, 11},
                {4, 6, 12, 14}, {4, 7, 12, 14}, {5, 7, 13, 15}, {5, 7, 13, 15},
                {4, 6, 12, 14}, {4, 7, 12, 14}, {5, 7, 13, 15}, {5, 7, 13, 15}]

udlr = {(None, 1, 0, None): {0, 5, 6, 9, 10, 12, 13, 14}, (1, None, 1, None): {0, 3, 5, 6, 7, 9},
        (None, 1, 0, 0): {0, 5, 6, 9, 10, 12, 13, 14}, (1, None, 0, 1): {0, 3, 6, 9, 10, 11},
        (1, None, 1, 0): {0, 3, 5, 6, 7, 9}, (0, 1, None, None): {0, 5, 6, 9, 10, 12, 13, 14}, (1, 1, 1, 1): {0, 9, 6},
        (1, 1, None, None): {0, 9, 10, 5, 6},
        (None, None, 0, 1): {0, 3, 6, 9, 10, 11, 12, 14}, (0, 1, 1, None): {0, 5, 6, 9, 12, 13},
        (0, None, None, 0): {0, 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15},
        (1, 0, 0, None): {0, 3, 5, 6, 7, 9, 10, 11},
        (0, None, 0, 0): {0, 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15}, (0, 0, 1, 1): {0, 9, 3, 12, 6},
        (None, 1, 0, 1): {0, 6, 9, 10, 12, 14}, (0, None, 1, 0): {0, 3, 5, 6, 7, 9, 12, 13},
        (None, 0, 0, 0): {0, 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15},
        (1, 0, 1, 1): {0, 9, 3, 6},
        (None, 0, 1, 0): {0, 3, 5, 6, 7, 9, 12, 13}, (1, 0, None, 1): {0, 3, 6, 9, 10, 11},
        (None, 0, 1, 1): {0, 9, 3, 12, 6}, (0, 1, 1, 1): {0, 9, 12, 6}, (1, 1, None, 0): {0, 9, 10, 5, 6},
        (0, None, 1, 1): {0, 9, 3, 12, 6}, (0, 0, 1, None): {0, 3, 5, 6, 7, 9, 12, 13},
        (None, 0, None, 1): {0, 3, 6, 9, 10, 11, 12, 14}, (1, None, 0, 0): {0, 3, 5, 6, 7, 9, 10, 11},
        (0, 1, None, 1): {0, 6, 9, 10, 12, 14}, (None, 1, None, 0): {0, 5, 6, 9, 10, 12, 13, 14},
        (0, 0, None, 0): {0, 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15},
        (None, None, 0, 0): {0, 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15}, (None, 1, 1, 0): {0, 5, 6, 9, 12, 13},
        (0, None, 1, None): {0, 3, 5, 6, 7, 9, 12, 13}, (0, None, 0, 1): {0, 3, 6, 9, 10, 11, 12, 14},
        (1, 1, 0, 1): {0, 9, 10, 6}, (None, 0, 1, None): {0, 3, 5, 6, 7, 9, 12, 13},
        (1, 0, 0, 0): {0, 3, 5, 6, 7, 9, 10, 11}, (None, 0, 0, 1): {0, 3, 6, 9, 10, 11, 12, 14},
        (0, 0, None, None): {0, 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15},
        (1, 0, 1, 0): {0, 3, 5, 6, 7, 9},
        (0, 0, 0, 1): {0, 3, 6, 9, 10, 11, 12, 14}, (None, None, 1, 0): {0, 3, 5, 6, 7, 9, 12, 13},
        (None, None, 1, 1): {0, 9, 3, 12, 6}, (0, 1, 0, 0): {0, 5, 6, 9, 10, 12, 13, 14},
        (0, 1, 0, None): {0, 5, 6, 9, 10, 12, 13, 14}, (1, 0, None, None): {0, 3, 5, 6, 7, 9, 10, 11},
        (1, 0, None, 0): {0, 3, 5, 6, 7, 9, 10, 11},
        (0, 1, 1, 0): {0, 5, 6, 9, 12, 13}, (1, 1, None, 1): {0, 9, 10, 6}, (1, 1, 0, None): {0, 9, 10, 5, 6},
        (1, None, None, 0): {0, 3, 5, 6, 7, 9, 10, 11}, (0, 1, None, 0): {0, 5, 6, 9, 10, 12, 13, 14},
        (None, 0, 0, None): {0, 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15}, (0, 0, None, 1): {0, 3, 6, 9, 10, 11, 12, 14},
        (None, 0, None, 0): {0, 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15}, (1, 1, 1, 0): {0, 9, 5, 6},
        (None, 1, 1, 1): {0, 9, 12, 6}, (1, None, None, None): {0, 3, 5, 6, 7, 9, 10, 11},
        (0, None, 0, None): {0, 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15},
        (1, 1, 0, 0): {0, 9, 10, 5, 6},
        (0, None, None, 1): {0, 3, 6, 9, 10, 11, 12, 14}, (1, 0, 0, 1): {0, 3, 6, 9, 10, 11},
        (0, 0, 1, 0): {0, 3, 5, 6, 7, 9, 12, 13}, (None, 1, 1, None): {0, 5, 6, 9, 12, 13},
        (1, None, 0, None): {0, 3, 5, 6, 7, 9, 10, 11},
        (0, 0, 0, None): {0, 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15},
        (0, 0, 0, 0): {0, 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15}, (None, None, 1, None): {0, 3, 5, 6, 7, 9, 12, 13},
        (1, 1, 1, None): {0, 9, 5, 6}, (0, 1, 0, 1): {0, 6, 9, 10, 12, 14}, (1, 0, 1, None): {0, 3, 5, 6, 7, 9},
        (1, None, None, 1): {0, 3, 6, 9, 10, 11}, (None, 1, None, 1): {0, 6, 9, 10, 12, 14},
        (1, None, 1, 1): {0, 9, 3, 6}}

gas_options = {1, 2, 4, 8}


def get_possibilities_by_neighbors():
    possibilities = dict()
    for u in range(3):
        for d in range(3):
            for l in range(3):
                for r in range(3):
                    if u:
                        u_options = gas_options
                    else:
                        u_options = {_ for _ in xrange(16)} - gas_options
                    if d:
                        d_options = gas_options
                    else:
                        d_options = {_ for _ in xrange(16)} - gas_options
                    if l:
                        l_options = gas_options
                    else:
                        l_options = {_ for _ in xrange(16)} - gas_options
                    if r:
                        r_options = gas_options
                    else:
                        r_options = {_ for _ in xrange(16)} - gas_options
                    u_possibilities, d_possibilities, l_possibilities, r_possibilities = set(), set(), set(), set()
                    for u_opt in u_options:
                        u_possibilities |= down_options[u_opt]
                    for d_opt in d_options:
                        d_possibilities |= up_options[d_opt]
                    for l_opt in l_options:
                        l_possibilities |= right_options[l_opt]
                    for r_opt in r_options:
                        r_possibilities |= left_options[r_opt]
                    if u == 2: u, u_possibilities = None, {_ for _ in xrange(16)}
                    if d == 2: d, d_possibilities = None, {_ for _ in xrange(16)}
                    if l == 2: l, l_possibilities = None, {_ for _ in xrange(16)}
                    if r == 2: r, r_possibilities = None, {_ for _ in xrange(16)}
                    possibilities[(u, d, l, r)] = u_possibilities & r_possibilities & d_possibilities & l_possibilities \
                                                  - {1, 2, 4, 8}
    print possibilities


def solution(g):
    # return construct_solution(g, 0, 0, [[None for _ in xrange(len(g[0]))] for _ in xrange(len(g))])
    mat = get_starting_matrix(g)
    return construct_solution([(mat, 0, 0)], 0)


def insert(m, v, i, j):
    m[i][j] = v
    return m


def convert_matrix(input_matrix):
    output = [[0 for _ in xrange(len(input_matrix[0]) + 1)] for _ in xrange(len(input_matrix) + 1)]
    for i in xrange(len(input_matrix)):
        for j in xrange(len(input_matrix[0])):
            a = [int(_) for _ in bin(input_matrix[i][j]).split('b')[1]]
            for _ in xrange(4 - len(a)):
                a.insert(0, 0)
            output[i][j] = a[0]
            if j == len(input_matrix[0]) - 1:
                output[i][j + 1] = a[1]
            if i == len(input_matrix) - 1:
                output[i + 1][j], output[i + 1][j + 1] = a[2], a[3]
    return output


def get_starting_matrix(input_matrix):
    min_length = 16
    starting_row, starting_col = 0, 0
    output_matrix = [[{_ for _ in xrange(16)} for _ in xrange(len(g[0]))] for _ in xrange(len(g))]
    for i in xrange(len(input_matrix)):
        for j in xrange(len(input_matrix[0])):
            u, d, l, r = None, None, None, None
            if i > 0:
                u = input_matrix[i - 1][j]
            if j > 0:
                l = input_matrix[i][j - 1]
            if not input_matrix[i][j]:
                if i < len(input_matrix) - 1:
                    d = input_matrix[i + 1][j]
                if j < len(input_matrix[0]) - 1:
                    r = input_matrix[i][j + 1]
                options = udlr[(u, d, l, r)]
                output_matrix[i][j] = options
            else:
                output_matrix[i][j] = gas_options
    return output_matrix


def construct_solution(stack, sum):
    while stack:
        output_matrix, i, j = stack.pop()
        if i == len(output_matrix) - 1 and j == len(output_matrix[0]) - 1:
            # todo delete
            # for opt in options:
            #     for row in convert_matrix(insert(output_matrix, opt, i, j)):
            #         print row
            #     print
            #     for row in insert(output_matrix, opt, i, j):
            #         print row
            #     print
            sum += len(output_matrix[i][j])
        else:
            if len(output_matrix[i][j]) == 1:
                (j, i) = (j + 1, i) if j + 1 < len(output_matrix) else (0, i + 1)
                stack.append(output_matrix, i, j)
            else:
                for opt in output_matrix[i][j]:
                    output_matrix[i][j] = {opt}
                    temp = copy.deepcopy(output_matrix)
                    if update_matrix(i, j, temp):
                        (j, i) = (j + 1, i) if j + 1 < len(output_matrix) else (0, i + 1)
                        stack.append(temp, i, j)
    return sum


def update_matrix(i, j, matrix, dirs):
    if i > 0 and dirs[0]:
        if not update(i, j, up_options, matrix, 0):
            return False
    if i < len(matrix) - 1 and dirs[1]:
        if not update(i, j, down_options, matrix, 1):
            return False
    if j > 0 and dirs[2]:
        if not update(i, j, i, j - 1, left_options, matrix):
            return False
    if j < len(matrix) - 1 and dirs[3]:
        if not update(i, j, i, j + 1, right_options, matrix):
            return False
    return True


def update(i, j, options, matrix, dir):
    if dir == 0:
        dirs = (1, 0, 1, 1)
        ni, nj = i - 1, j
    elif dir == 1:
        dirs = (0, 1, 1, 1)
        ni, nj = i + 1, j
    elif dir == 2:
        dirs = (1, 1, 1, 0)
        ni, nj = i, j - 1
    elif dir == 3:
        dirs = (1, 1, 0, 1)
        ni, nj = i, j + 1
    else:
        assert False

    directional_options = set()
    for opt in matrix[i][j]:
        directional_options |= options[opt]
    # if change happened
    temp = matrix[ni][nj]
    matrix[ni][nj] = matrix[ni][nj] & directional_options
    if not matrix[ni][nj]:
        return False
    if temp != matrix[ni][nj]:
        return update_matrix(ni, nj, matrix, dirs)
    return True


# def construct_solution(all_options):
#     output_matrix = [[None for _ in xrange(len(g[0]))] for _ in xrange(len(g))]
#     for i in xrange(len(all_options)):
#         for j in xrange(len(all_options[0])):
#             for k in all_options[i][j]:
#                 output_matrix[i][j] = k
#


input_0 = [[True, True, False, True, False, True, False, True, True, False],
           [True, True, False, False, False, False, True, True, True, False],
           [True, True, False, False, False, False, False, False, False, True],
           [False, True, False, False, False, False, True, True, False, False]]

input_1 = [[True, False, True], [False, True, False], [True, False, True]]

input_2 = [[True, False, True, False, False, True, True, True],
           [True, False, True, False, False, False, True, False],
           [True, True, True, False, False, False, True, False],
           [True, False, True, False, False, False, True, False],
           [True, False, True, False, False, True, True, True]]

inputs = [input_0, input_1, input_2]
for g in inputs:
    # for r in solution(g):
    #     print r
    print solution(g)
# get_possibilities_by_neighbors()
# for k, v in get_possibilities_by_neighbors().items():
#     print k, v
