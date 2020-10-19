# class Edge(object):
#     def __init__(self, capacity, source, sink):
SINK = -1
SOURCE = -2
CAPACITY = 1

def solution(entrances, exits, path):
    return get_flow_network(entrances, exits, path)





def get_flow_network(entrances, exits, path):
    """
    add source and sink to the matrix, as well as a flow field for each edge (corridor) initialized to 0
    :return: matrix representation of the new flow network
    """
    length = xrange(len(path) + 2)
    source = [(0, sum(path[i])) if i in entrances else (0, 0) for i in length]
    sink = [(0, sum(path[j][i] for j in xrange(len(path)))) if i in exits else (0, 0) for i in length]
    network = [[(0, path[i][j]) if j < len(path) else (0, 0) for j in length] for i in
               xrange(len(path))] + [source, sink]
    for i in entrances:
        max_flow = sum(network[i][j][CAPACITY] for j in xrange(len(network[i])))
        network[i][SOURCE] = (0, max_flow)
    for i in exits:
        max_flow = sum(network[j][i][CAPACITY] for j in xrange(len(network[i])))
        network[i][SINK] = (0, max_flow)
    return network


entrances = [0, 1]
exits = [4, 5]
path = [
    [0, 0, 4, 6, 0, 0],  # Room 0: Bunnies
    [0, 0, 5, 2, 0, 0],  # Room 1: Bunnies
    [0, 0, 0, 0, 4, 4],  # Room 2: Intermediate room
    [0, 0, 0, 0, 6, 6],  # Room 3: Intermediate room
    [0, 0, 0, 0, 0, 0],  # Room 4: Escape pods
    [0, 0, 0, 0, 0, 0],  # Room 5: Escape pods
]

for r in get_flow_network(entrances, exits, path):
    print(r)
