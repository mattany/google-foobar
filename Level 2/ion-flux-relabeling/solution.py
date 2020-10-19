def solution(h, q):
    tree = dict()
    stack = [(2**h - 1, h - 1, -1)]
    while len(stack) > 0 and len(tree) < 2**h - 1:
        cur = stack.pop()
        tree[cur[0]] = cur[2]
        stack.insert(0, (cur[0] - 1, cur[1] - 1, cur[0]))
        stack.insert(0, (cur[0] - 2**cur[1], cur[1] - 1, cur[0]))
    return [tree[i] for i in q]
