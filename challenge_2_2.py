from functools import reduce

def solution(xs):
    pos = sorted([x for x in xs if x > 0])
    zero = 0 in xs
    neg = sorted([-x for x in xs if x < 0])
    if len(neg) == 1 and len(pos) == 0 and not zero:
        return str(-neg[0])
    if len(neg) % 2 != 0:
        neg.pop(0)
    merged = pos + neg
    if len(merged) > 0:
        return str(reduce(lambda x, y: x*y, pos + neg))
    return "0"


print solution([-4])