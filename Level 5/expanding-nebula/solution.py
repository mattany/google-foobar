import itertools

def solution(g):
    global num_rows, num_cols
    num_rows, num_cols = len(g), len(g[0])
    column_pred, column_succ = dict(), dict()
    transposed = [[g[x][y] for x in xrange(num_rows)] for y in xrange(num_cols)]
    int_representations = list()
    for col in transposed:
        representation = to_int(col)
        int_representations.append(representation)
        if representation not in column_pred:
            column_pred[representation], column_succ[representation] = dict(), dict()
            update_dicts(col, representation, column_pred, column_succ)
    col = column_succ[int_representations[0]]
    for _ in xrange(1, num_cols):
        int_rep = int_representations[_]
        next_col_pred, next_col_succ = column_pred[int_rep], column_succ[int_rep]
        col = get_edges(col, next_col_pred)
    return sum(col.values())


def get_edges(col1_succ, col2_pred):
    ret = dict()
    for c2p in col2_pred:
        if c2p in col1_succ:
            amount_of_paths_to_c2 = col1_succ[c2p]
            for c2s in col2_pred[c2p]:
                if c2s in ret:
                    ret[c2s] += amount_of_paths_to_c2
                else:
                    ret[c2s] = amount_of_paths_to_c2
    return ret


def update_dicts(col, representation, column_pred, column_succ):
    for c1 in itertools.product((0, 1), repeat=num_rows + 1):
        for c2 in itertools.product((0, 1), repeat=num_rows + 1):
            next_state = advance(c1, c2)
            if next_state == col:
                if to_int(c1) not in column_pred[representation]:
                    column_pred[representation][to_int(c1)] = [to_int(c2)]
                else:
                    column_pred[representation][to_int(c1)] += [to_int(c2)]
                if to_int(c2) not in column_succ[representation]:
                    column_succ[representation][to_int(c2)] = 1
                else:
                    column_succ[representation][to_int(c2)] += 1


def advance(c1, c2):
    ret = []
    for i in xrange(num_rows):
        s = c1[i] + c1[i + 1] + c2[i] + c2[i + 1]
        if s == 1:
            ret.append(1)
        else:
            ret.append(0)
    return ret


def to_int(arr):
    ret = arr[-1]
    shift = 0
    for _ in xrange(len(arr) - 2, -1, -1):
        if arr[_]:
            ret += 2 << shift
        shift += 1
    return ret


input_0 = [[True, True, False, True, False, True, False, True, True, False],
           [True, True, False, False, False, False, True, True, True, False],
           [True, True, False, False, False, False, False, False, False, True],
           [False, True, False, False, False, False, True, True, False, False]]

input_1 = [[True, False, True], [False, True, False], [True, False, True]]

input_2 = [[True, False, True, False, False, True, True, True],
           [True, False, True, False, False, False, True, False],
           [True, True, True, False, False, False, True, False],
           [True, False, True, False, False, False, True, False],
           [True, False, True, False, False, True, True, True]]

inputs = [input_2, input_1, input_0]

for g in inputs:
    for i in xrange(100):
        print solution(g)
