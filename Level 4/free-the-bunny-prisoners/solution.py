def is_trivial(num_blocks, num_required):
    if num_required == 0:
        return [[] for _ in xrange(num_blocks)]
    if num_required == 1:
        return [[0] for _ in xrange(num_blocks)]
    if num_required == num_blocks:
        return [[_] for _ in xrange(num_blocks)]
    return False


def solution(blocks, required):
    result = is_trivial(blocks, required)
    if result:
        return result
    left_part = solution(blocks - 1, required)
    right_part = solution(blocks - 1, required - 1)
    row_length = left_part[-1][-1] + 1
    right_part = [[_ + row_length for _ in row] for row in right_part]
    return [range(row_length)] + [left_part[_] + right_part[_] for _ in xrange(len(left_part))]
