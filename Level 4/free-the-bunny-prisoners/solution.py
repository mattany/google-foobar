import copy
import itertools
import random
import operator as op
from functools import reduce
CUTOFF = 10000000

def is_trivial(num_blocks, num_required):
    if num_required == 0:
        return [[] for _ in xrange(num_blocks)]
    if num_required == 1:
        return [[0] for _ in xrange(num_blocks)]
    if num_required == num_blocks:
        return [[_] for _ in xrange(num_blocks)]
    return False


def covered_iterator(block_combo, reps):
    block_length, block_amount = len(block_combo[0]), len(block_combo)
    bunny_combinations = list(itertools.combinations(xrange(block_amount), reps))
    for c in bunny_combinations:
        covered = [0 for _ in xrange(block_length)]
        for bunny in c:
            covered = [1 if block_combo[bunny][j] or covered[j] else 0 for j in xrange(block_length)]
        yield covered


def check_incidence(block_combo, num_required):
    # print(convert_mat_to_output(block_combo))
    for i in xrange(num_required):
        for c in covered_iterator(block_combo, i):
            if all(c):
                return False
    for c in covered_iterator(block_combo, num_required):
        if not all(c):
            return False
    return True


def convert_mat_to_output(incidence_matrix):
    return sorted([[_ for _ in xrange(len(incidence_matrix[0])) if incidence_matrix[i][_]] for i in
                   xrange(len(incidence_matrix))])


def convert_output_to_incidence_matrix(output):
    maxdigit = max(max(i) for i in output)
    return [[1 if _ in output[j] else 0 for _ in xrange(maxdigit + 1)] for j in xrange(len(output))]

def minimize(solution_matrix, num_keys):
    subs = [set(range(_)) for _ in xrange(max(num_keys, 10))]
    row_length = len(solution_matrix[0])
    for i in xrange(len(solution_matrix)):
        solution_matrix[i] = list(reversed(sorted(solution_matrix[i])))
        not_relevant = set()
        for j in xrange(row_length):
            not_relevant |= set(solution_matrix[i])
            candidate = solution_matrix[i][j]
            if subs[candidate]:
                sub_options = subs[candidate] - not_relevant
                if sub_options:
                    sub = min(sub_options)
                    solution_matrix[i][j] = sub
                    for k in xrange(i + 1, len(solution_matrix)):
                        for l in xrange(row_length):
                            if solution_matrix[k][l] == candidate:
                                solution_matrix[k][l] = sub
                            elif solution_matrix[k][l] == sub:
                                solution_matrix[k][l] = candidate
        all, row = set(range(1, num_keys)), set(solution_matrix[i])
        rem = all - row
        for elem in rem:
            subs[elem] = subs[elem] - row
    return sorted([sorted(row) for row in solution_matrix])


def solution(num_bunnies, num_required):
    result = is_trivial(num_bunnies, num_required)
    if result:
        return result
    solution_matrix = [[_] for _ in xrange(num_required)]

    for j in xrange(num_required, num_bunnies):
        num_blocks = j + 1
        prev_row_length = len(solution_matrix[0])
        solution_matrix.insert(1, range(prev_row_length))
        row_length = solution_matrix[-1][-1] + 1
        solution_matrix[0] += range(prev_row_length, row_length)

        if num_required == 2 or num_required == 3:
            i, count, elem = 1, 0, row_length
            for _ in xrange(j * (row_length - prev_row_length)):
                if i == num_blocks:
                    i = 1
                if count == j - num_required + 2:
                    count, elem = 0, elem + 1
                solution_matrix[i].append(elem)
                count, i = count + 1, i + 1
        else:
            repeats = (num_blocks - num_required + 1)
            num_keys = (row_length * num_blocks) // repeats
            repeat_count = [repeats if _ < row_length else 0 for _ in xrange(num_keys)]
            kpb = row_length
            keys_per_block = [prev_row_length for _ in xrange(num_blocks)]
            keys_per_block[0] = kpb
            initial_matrix = convert_output_to_incidence_matrix(solution_matrix)
            for t in xrange(num_blocks):
                initial_matrix[t] += [0 for _ in xrange(num_keys - row_length)]
            solution_matrix = copy.deepcopy(initial_matrix)
            index_q = []
            for i in range(CUTOFF):
                # if not i % 100000:
                #     print i / 100000, num_blocks, num_required, num_keys, repeats

                while any(_ != repeats for _ in repeat_count):
                        # or any(_ != kpb for _ in keys_per_block):
                    min_key = random.choice([_ for _ in xrange(num_keys) if repeat_count[_] < repeats])
                    block_candidates = [_ for _ in xrange(num_blocks) if
                                        keys_per_block[_] < kpb and solution_matrix[_][min_key] == 0]
                    repeat_count[min_key] += 1
                    if len(block_candidates) > 0:
                        selected_block = random.choice(block_candidates)
                        solution_matrix[selected_block][min_key] = 1
                        index_q.append((selected_block, min_key))
                        keys_per_block[selected_block] += 1
                    else:
                        selected_block, to_evict_key = index_q.pop(random.randint(0, len(index_q) - 1))
                        solution_matrix[selected_block][to_evict_key] = 0
                        repeat_count[to_evict_key] -= 1
                        index_q.append((selected_block, min_key))
                        solution_matrix[selected_block][min_key] = 1
                # print(convert_mat_to_output(solution_matrix))
                if check_incidence(solution_matrix, num_required):
                    solution_matrix = minimize(convert_mat_to_output(solution_matrix), num_keys)
                    # for r in solution_matrix:
                    #     print r, ","
                    break
                repeat_count = [repeats if _ < row_length else 0 for _ in xrange(num_keys)]
                kpb = row_length
                keys_per_block = [prev_row_length for _ in xrange(num_blocks)]
                keys_per_block[0] = kpb
                solution_matrix = copy.deepcopy(initial_matrix)
                index_q = []
    return solution_matrix


sol = solution(7, 4)

for j in xrange(1, 8):
    for i in xrange(j + 1, 10):
        sol = solution(i, j)
        print i, j, check_incidence(convert_output_to_incidence_matrix(sol), j)
        for r in sol:
            print r


b2 = [[0],
      [1]]
b3 = [[[0, 1],
       [0, 2],
       [1, 2]]]
b4 = [[0, 1, 2],
      [0, 1, 3],
      [0, 2, 3],
      [1, 2, 3]]
b5 = [[0, 1, 2, 3],
      [0, 1, 2, 4],
      [0, 1, 3, 4],
      [0, 2, 3, 4],
      [1, 2, 3, 4]]

# 3 1
# 3 ** 0
c3 = [[0],
      [1],
      [2]]
# 5 2
# 3 * 1
c4 = [[0, 1, 2],
      [0, 3, 4],
      [1, 3, 5],
      [2, 4, 5]]

# 10 3
#
c5 = [[0, 1, 2, 3, 4, 5],
      [0, 1, 2, 6, 7, 8],
      [0, 3, 4, 6, 7, 9],
      [1, 3, 5, 6, 8, 9],
      [2, 4, 5, 7, 8, 9]]
# 10 4
#
c6 = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
      [0, 1, 2, 3, 4, 5, 10, 11, 12, 13],
      [0, 1, 2, 6, 7, 8, 10, 11, 12, 14],
      [0, 3, 4, 6, 7, 9, 10, 11, 13, 14],
      [1, 3, 5, 6, 8, 9, 10, 12, 13, 14],
      [2, 4, 5, 7, 8, 9, 11, 12, 13, 14]]
# 28 5
#
c7 = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 15, 16, 17, 18, 19],
      [0, 1, 2, 3, 4, 5, 10, 11, 12, 13, 15, 16, 17, 18, 20],
      [0, 1, 2, 6, 7, 8, 10, 11, 12, 14, 15, 16, 17, 19, 20],
      [0, 3, 4, 6, 7, 9, 10, 11, 13, 14, 15, 16, 18, 19, 20],
      [1, 3, 5, 6, 8, 9, 10, 12, 13, 14, 15, 17, 18, 19, 20],
      [2, 4, 5, 7, 8, 9, 11, 12, 13, 14, 16, 17, 18, 19, 20]]

d4 = [[0],
      [1],
      [2],
      [3]]
d5 = [[0, 1, 2, 3],
      [0, 4, 5, 6],
      [1, 4, 7, 8],
      [2, 5, 7, 9],
      [3, 6, 8, 9]]
d6 = [[0, 1, 2, 3,  4,  5,  6,  7,  8,  9],
      [0, 1, 2, 3, 10, 11, 12, 13, 14, 15],
      [0, 4, 5, 6, 10, 11, 12, 16, 17, 18],
      [1, 4, 7, 8, 10, 13, 14, 16, 17, 19],
      [2, 5, 7, 9, 11, 13, 15, 16, 18, 19],
      [3, 6, 8, 9, 12, 14, 15, 17, 18, 19]]
d7 = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19] ,
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29] ,
[0, 1, 2, 3, 10, 11, 12, 13, 14, 15, 20, 21, 22, 23, 24, 25, 30, 31, 32, 33] ,
[0, 4, 5, 6, 10, 11, 12, 16, 17, 18, 20, 21, 22, 26, 27, 28, 30, 31, 32, 34] ,
[1, 4, 7, 8, 10, 13, 14, 16, 17, 19, 20, 23, 24, 26, 27, 29, 30, 31, 33, 34] ,
[2, 5, 7, 9, 11, 13, 15, 16, 18, 19, 21, 23, 25, 26, 28, 29, 30, 32, 33, 34] ,
[3, 6, 8, 9, 12, 14, 15, 17, 18, 19, 22, 24, 25, 27, 28, 29, 31, 32, 33, 34] ,]



e6 = [[0, 1, 2, 3, 4],
      [0, 5, 6, 7, 8],
      [1, 5, 9, 10, 11],
      [2, 6, 9, 12, 13],
      [3, 7, 10, 12, 14],
      [4, 8, 11, 13, 14]]

e7 = [[0, 1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14],
      [0, 1,  2,  3,  4,  15, 16, 17, 18, 19],
      [0, 5,  6,  7,  8],
      [1, 5,  9, 10, 11],
      [2, 6,  9, 12, 13],
      [3, 7, 10, 12, 14],
      [4, 8, 11, 13, 14]]
# print check_incidence(convert_output_to_incidence_matrix(d7), 4)
