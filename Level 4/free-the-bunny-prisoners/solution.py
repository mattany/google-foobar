def is_trivial(num_blocks, num_required):
    if num_required == 0:
        return [[] for _ in xrange(num_blocks)]
    if num_required == 1:
        return [[0] for _ in xrange(num_blocks)]
    if num_required == num_blocks:
        return [[_] for _ in xrange(num_blocks)]
    return False


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
        i, count, elem = 1, 0, row_length
        for _ in xrange(j * (row_length - prev_row_length)):
            if i == num_blocks:
                i = 1
            if count == j - num_required + 2:
                count, elem = 0, elem + 1
            solution_matrix[i].append(elem)
            count, i = count + 1, i + 1
    return solution_matrix


for i in xrange(1, 10):
    for j in xrange(i + 1):
        print i, j
        for r in solution(i, j):
            print r
