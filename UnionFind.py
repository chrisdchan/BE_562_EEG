class UnionFind():
    def __init__(self, N):
        self.parent = [i for i in range(N)]
        self.rank = [0 for i in range(N)]

    def find(self, node):
        current_node = node
        while self.parent[current_node] != current_node:
            current_node = self.parent[current_node]
        return current_node

    def union(self, node1, node2):
        root1 = self.find(node1)
        root2 = self.find(node2)

        if root1 != root2:
            if self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            elif self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1