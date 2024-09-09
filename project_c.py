import pandas as pd
import networkx as nx

class Graph:
    def __init__(self):
        self.graph = {} # Initializing an empty dictionary to represent the graph

    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []# Adding node 'u' to the graph if not already present
        self.graph[u].append(v)# Adding edge (u, v) to the graph

    def dfs(self, v, visited, stack):
        visited.add(v)# Marking node 'v' as visited
        for neighbor in self.graph.get(v, []):
            if neighbor not in visited:
                self.dfs(neighbor, visited, stack)# Recursively performing DFS on unvisited neighbors
        stack.append(v) # Adding node 'v' to the stack after visiting all its neighbors

    def transpose(self):
        transposed = Graph()# Creating a new instance of Graph to represent the transposed graph
        for u in self.graph:
            for v in self.graph[u]:
                transposed.add_edge(v, u) #Reversing the direction of each edge in the original graph
        return transposed# Returning the transposed graph

    def fill_order(self, v, visited, stack):
        visited.add(v)# Marking node 'v' as visited
        for neighbor in self.graph.get(v, []):
            if neighbor not in visited:
                self.fill_order(neighbor, visited, stack)# Recursively performing DFS on unvisited neighbors
        stack.append(v)# Adding node 'v' to the stack after visiting all its neighbors

    def get_sccs(self):
        stack = [] # Initializing a stack to store nodes in order of their finishing times
        visited = set()# Initializing a set to store visited nodes
        for node in self.graph:
            if node not in visited:
                self.dfs(node, visited, stack)# Performing DFS on all unvisited nodes
        # Getting the transposed graph
        transposed = self.transpose()
        # Clearing the visited set to reuse it for the next DFS traversal
        visited.clear()
        sccs = []# Initializing a list to store strongly connected components

        while stack:
            v = stack.pop() # Popping a node from the stack
            if v not in visited:
                scc = [] # Initializing a list to store nodes in the current strongly connected component
                transposed.fill_order(v, visited, scc)# Performing DFS on the transposed graph to get the SCC
                sccs.append(scc)# Adding the SCC to the list of SCCs

        return sccs

#Reading the csv file 
data = pd.read_csv('modified_impression_network.csv')

#Creating directed graph from the csv file data
G = nx.DiGraph()
for index, row in data.iterrows():
    node = row.iloc[0]  # Assuming the first column contains the node
    neighbors = row.iloc[1:].dropna().tolist()  # Assuming the rest columns are neighbors
    G.add_node(node)  # Adding nodes to the graph
    for neighbor in neighbors: # Adding neighbors to the graph
        G.add_edge(node, neighbor)
        
# Converting NetworkX graph to adjacency list
adjacency_list = {}
for edge in G.edges:
    if edge[0] not in adjacency_list:
        adjacency_list[edge[0]] = []# Adding node 'u' to the adjacency list if not already present
    adjacency_list[edge[0]].append(edge[1])# Adding edge (u, v) to the adjacency list

# Creating a Graph object and initialize it with the adjacency list
g = Graph()# Creating an instance of the Graph class
for node, neighbors in adjacency_list.items():
    for neighbor in neighbors:
        g.add_edge(node, neighbor)# Adding edges to the graph using the adjacency list

# Finding strongly connected components using Kosaraju's algorithm
sccs = g.get_sccs()# Getting the strongly connected components
print("Strongly Connected Components:")
for scc in sccs:
    print(scc)

# Getting the largest strongly connected component
largest_scc = max(sccs, key=len)

# Number of nodes in the largest strongly connected component
num_nodes_in_largest_scc = len(largest_scc)

print("Number of nodes in the largest strongly connected component:", num_nodes_in_largest_scc)
