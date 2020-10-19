def solution(l):
    if len(l) < 3:
        return 0
    step_matrix = [[1 if i > j and l[i] % l[j] == 0 else 0 for i in xrange(len(l))] for j in xrange(len(l))]
    return sum(get_solution_vector(step_matrix))


def get_solution_vector(m):
    sum_vector = [sum(m[i]) for i in xrange(len(m))]
    return [sum(sum_vector[j] if m[i][j] else 0 for j in xrange(len(m))) for i in xrange(len(m))]