import numpy as np
import time
from UnionFind import UnionFind

def find_max_spanning_tree(G):
    '''
    Args:
        G: np.Array - Adjacency Matrix of the Graph
    Returns
        np.Array - Adjacency Matrix of MST with all edges equal to 1
    '''
    N, _ = np.shape(G)
    spanning_tree = np.zeros_like(G)

    union_find = UnionFind(N)
    edges = [(G[node1, node2], node1, node2) for node1 in range(N) for node2 in range(node1)]
    edges.sort(key=lambda tup: tup[0])

    edge_count = 0
    while edge_count < N - 1:

        _, node1, node2 = edges.pop()
        root1 = union_find.find(node1)
        root2 = union_find.find(node2)

        if root1 != root2:
            spanning_tree[node1, node2] = 1
            spanning_tree[node2, node1] = 1
            edge_count += 1
            union_find.union(node1, node2)

    return spanning_tree

if __name__ == '__main__':
    A = np.array([
        [0, 3, 5],
        [3, 0, 7],
        [5, 7, 0],
    ], dtype=float)

    mst = find_max_spanning_tree(A)
    print(mst)

    





