import functools
import itertools
import random

CUTOFF = 10000


# def solution(num_buns, num_required):
#     # solution_matrix = [[0 for i in xrange(10)] for i in xrange(num_buns)]
#     for i in xrange(11):
#         # print(i, "elements")
#         possible_blocks = list(itertools.product((0, 1), repeat=i))
#         buckets = {k: [] for k in xrange(i + 1)}
#         for block in possible_blocks:
#             buckets[sum(block)].append(block)
#         for j in xrange(i + 1):
#             all_perms = ((tuple(1 if _ < j else 0 for _ in xrange(i)),) + _ for _ in
#                          itertools.combinations_with_replacement(buckets[j], num_buns - 1))
#             for perm in all_perms:
#                 if symmetric_permutation(perm):
#                     if check_incidence(perm, num_required):
#                         return convert_mat_to_output(perm)
#                     break
#                     # print(perm)
#                     # print(',')
#             # print(len(buckets[j]), len(all_perms))


def solution(num_buns, num_required):

    for i in xrange(100):
        for j in xrange(num_buns + 1):
            success = construct_incedence_matrix(num_buns, i, j, num_required)
            if success:
                return success






def construct_incedence_matrix(num_blocks, num_keys, repeats, num_required):
    if (num_keys * repeats) % num_blocks:
        return False
    repeat_count = [0 for _ in xrange(num_keys)]
    kpb = (num_keys * repeats) // num_blocks
    keys_per_block = [0 for _ in xrange(num_blocks)]
    solution_matrix = [[0 for _ in xrange(num_keys)] for i in xrange(num_blocks)]
    index_q = []
    for i in range(CUTOFF):
        while any(_ != repeats for _ in repeat_count) or any(_ != kpb for _ in keys_per_block):
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
                selected_block, to_evict_key = index_q.pop(0)
                solution_matrix[selected_block][to_evict_key] = 0
                repeat_count[to_evict_key] -= 1
                index_q.append((selected_block, min_key))
                solution_matrix[selected_block][min_key] = 1
        if check_incidence(solution_matrix, num_required):
            return minimize(convert_mat_to_output(solution_matrix), num_keys)
        repeat_count = [0 for _ in xrange(num_keys)]
        kpb = (num_keys * repeats) // num_blocks
        keys_per_block = [0 for _ in xrange(num_blocks)]
        solution_matrix = [[0 for _ in xrange(num_keys)] for i in xrange(num_blocks)]
        index_q = []
    return False


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
        all, row = set(range(1,num_keys)), set(solution_matrix[i])
        rem = all - row
        for elem in rem:
            subs[elem] = subs[elem] - row
    return sorted([sorted(row) for row in solution_matrix])


def symmetric_permutation(perm):
    if len(perm[0]) == 0:
        return True
    zero_count = sum(perm[_][0] for _ in xrange(len(perm)))
    for i in xrange(1, len(perm[0])):
        if sum(perm[_][i] for _ in xrange(len(perm))) != zero_count:
            return False
    return True


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


num_buns_1, num_required_1 = 2, 1
num_buns_2, num_required_2 = 4, 4
num_buns_3, num_required_3 = 5, 3
output_1 = [[0], [0]]

# print(solution(num_buns_1, num_required_1))
# print(solution(num_buns_2, num_required_2))
# print(solution(num_buns_3, num_required_3))

# print(check_incidence([[0, 1, 2, 3, 4],
#  [0, 1, 2, 3, 5],
#  [0, 1, 2, 5, 6],
#  [0, 1, 2, 7, 9],
#  [0, 1, 4, 8, 9],
#  [0, 3, 6, 7, 8]], 5))


for i in xrange(1,10):
    for j in xrange(0,i+1):
        print "Params", i, j
        print(solution(i, j))