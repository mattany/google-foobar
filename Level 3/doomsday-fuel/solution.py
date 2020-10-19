import fractions
import functools

epsilon = 0.000001
rounding_factor = 1000


def solution(m):
    terminals = [i for i in xrange(len(m)) if sum(m[i]) == 0]
    if len(terminals) == 0:
        return []
    make_probability_matrix(m)
    prev = [1] + [i for i in xrange(len(m) - 1)]
    cur = m[0]
    while distance(prev, cur) > epsilon:
        prev = cur
        cur = [sum(cur[i] * m[i][j] for i in xrange(len(cur))) for j in xrange(len(cur))]
    cur = [fractions.Fraction(i).limit_denominator(rounding_factor) for i in cur]
    denominators = (int(i.denominator) for i in cur)
    lcm = int(functools.reduce(lambda x, y: x * y // fractions.gcd(x, y), denominators))
    return [int(item.numerator * (lcm / item.denominator)) for i, item in enumerate(cur) if i in terminals] + [lcm]


def distance(x, y):
    return sum(abs(x[i] - y[i]) for i in range(len(x)))


def make_probability_matrix(arr):
    for i, state in enumerate(arr):
        if sum(state) == 0:
            arr[i][i] = 1
        denominator = sum(state)
        arr[i] = [float(fractions.Fraction(x, denominator)) for x in state]


