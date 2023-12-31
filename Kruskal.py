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
    spanning_tree = np.zeros_like(G, dtype=bool)

    union_find = UnionFind(N)
    
    # Create a list of edges sorted edges based on Mutual Info stored as (Mutual Info, node1, node2)
    edges = [(G[node1, node2], node1, node2) for node1 in range(N) for node2 in range(node1)]
    edges.sort(key=lambda tup: tup[0])

    edge_count = 0
    while edge_count < N - 1:

        _, node1, node2 = edges.pop()
        root1 = union_find.find(node1)
        root2 = union_find.find(node2)

        # Check if node1 and node2 are already connected in the tree (if they have the same root)
        if root1 != root2:
            # Add edge to the tree
            spanning_tree[node1, node2] = 1
            spanning_tree[node2, node1] = 1
            edge_count += 1
            # Mark that the two nodes are connected in the Union Find
            union_find.union(node1, node2)

    return spanning_tree

def compute_mst(mi_path):
    '''
    Args:
        mi_path: path to a mutual info graph .npy file
    Returns: MST
    '''
    mutual_info_graph = np.load(mi_path)
    mst = find_max_spanning_tree(mutual_info_graph)
    return mst

def get_network_parents(mst, start_node=0):
    '''
    Given an MST graph, set the root and perform depth first search on
    the graph to determine the direction of all the edges
    Args:
        mst: numpy array representing adjacency matrix of the mst graph 
    '''

    stack = [] # Store nodes that are set to be visited
    seen = {} # Keep track of all nodes already visited

    stack.append(start_node)
    n, _ = mst.shape
    parents = np.ones(n) * -1

    # Continue until stack is empty
    while len(stack) > 0:
        node = stack.pop()
        seen[node] = True
        children = np.nonzero(mst[node])[0]
        for child in children:
            if child not in seen:
                # This check ensures that the inputted graph does not contain cycles
                assert parents[child] == -1
                parents[child] = node
                stack.append(child)
    
    return parents

def save_graph_npy(graph, path):
    np.save(path, graph)
    print(f'Graph computed and saved to {path}')

def save_graph_csv(graph, path):
    np.savetxt(path, graph, delimiter=',')
    print(f'Graph computed and saved to {path}')


if __name__ == '__main__':
    mi_path = "distributions/I.npy"
    network_path = "distributions/parents.npy"
    mst = compute_mst(mi_path)
    parents = get_network_parents(mst)
    np.save(network_path, parents)

    





