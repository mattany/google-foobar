def solution(x, y):
    sorted_x = sorted(x)
    sorted_y = sorted(y)
    for i in range(min(len(x), len(y))):
        if sorted_x[i] != sorted_y[i]:
            return min(sorted_x[i], sorted_y[i])
    if len(x) > len(y):
        return x[-1]
    else:
        return y[-1]