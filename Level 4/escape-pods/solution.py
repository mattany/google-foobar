FLOW = 0
CAPACITY = 1
NOT_NONE = -1
SINK = -1
SOURCE = -2
MAX_BUNNIES = 2000000

def solution(entrances, exits, path):
    return edmonds_karp(get_flow_network(entrances, exits, path))

def edmonds_karp(graph):
    """
    find max flow in graph
    :param graph: 2d matrix
    :param s: source
    :param t: sink
    :return: max flow
    """
    flow = 0
    pred = [NOT_NONE]
    while pred[SINK] is not None:
        q = list()
        q.append(SOURCE)
        pred = [None for i in xrange(len(graph))]
        while len(q) > 0:
            cur = q.pop(0)
            for (i, edge) in enumerate(graph[cur]):
                if pred[i] is None and edge[FLOW] < edge[CAPACITY]:
                    pred[i] = cur
                    q.append(i)
        if pred[SINK] is not None:
            new_flow = MAX_BUNNIES

            # Find optimal Flow for the shortest path
            e = (pred[SINK], SINK)
            while e[SOURCE] is not None:
                edge = graph[e[SOURCE]][e[SINK]]
                new_flow = min(new_flow, edge[CAPACITY] - edge[FLOW])
                e = (pred[e[SOURCE]], e[SOURCE])

            # Update the capacity of edges on that path
            e = (pred[SINK], SINK)
            while e[SOURCE] is not None:
                graph[e[SOURCE]][e[SINK]] = (graph[e[SOURCE]][e[SINK]][FLOW] + new_flow, graph[e[SOURCE]][e[SINK]][CAPACITY])
                e = (pred[e[SOURCE]], e[SOURCE])

            flow = flow + new_flow
    return flow

def get_flow_network(entrances, exits, path):
    """
    add source and sink to the matrix, as well as a flow field for each edge (corridor) initialized to 0
    :return: matrix representation of the new flow network
    """
    network_size = xrange(len(path) + 2)
    source = [(0, sum(path[i])) if i in entrances else (0, 0) for i in network_size]
    sink = [(0, 0) for i in network_size]
    network = [[(0, path[i][j]) if j < len(path) else (0, 0) for j in network_size] for i in
               xrange(len(path))] + [source, sink]

    for i in exits:
        max_flow = sum(network[j][i][CAPACITY] for j in network_size)
        network[i][SINK] = (0, max_flow)
    return network