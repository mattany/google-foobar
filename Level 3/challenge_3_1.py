# def solution(n):
#     n = bin(long(n))
#     stack = [(n, 0)]
#     min_ops = n
#     while len(stack) > 0:
#         print(stack)
#         cur = stack.pop()
#         if cur[0] == 1:
#             min_ops = min(cur[1], min_ops)
#         else:
#             if cur[0] % 2 == 0:
#                 stack.insert(0, (cur[0] >> 1, cur[1] + 1))
#             else:
#                 stack.insert(0, (cur[0] + 1, cur[1] + 1))
#                 stack.insert(0, (cur[0] - 1, cur[1] + 1))
#     return min_ops

def solution(n):
    n = long(n)
    ops = 0
    while n != 1:
        if n % 2 == 0:
            n >>= 1
        elif n > 3 and bin(n)[-2] == "1":
            n += 1
        else:
            n -= 1
        ops += 1
    return ops

# for i in xrange(1, 16):
#     print solution(i)