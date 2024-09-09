import pandas as pd
import networkx as nx
import random
import numpy as np

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

"""
    Performing a random walk with teleportation on the given graph.

    Parameters used:
        G (networkx.DiGraph): Directed graph to perform random walk on.
        teleport_prob : Probability of teleportation (default is 0.15).
        num_steps : Number of steps in the random walk (default is 1000000).

    Returns:
        tuple: A tuple containing two lists - nodes and their random walk points.
    """
def random_walk_with_teleportation(G, teleport_prob=0.15, num_steps=1000000):
    nodes = list(G.nodes())# Extracting all nodes from the graph
    rw_points = {node: 0 for node in nodes}# Initializing random walk points for each node
    current_node = random.choice(nodes)# Choosing a random starting node
    for _ in range(num_steps):
                
        # Perform teleportation with a certain probability
        if random.random() <= teleport_prob:
            current_node = random.choice(nodes)# Teleporting to a random node
        else:
            neighbors = list(G.neighbors(current_node))# Getting neighbors of the current node
            if neighbors: # If neighbors exist
                current_node = random.choice(neighbors)# Moving to a random neighbor
            else:
                current_node = random.choice(nodes)# Teleporting if no neighbors exist
        rw_points[current_node] += 1# Incrementing random walk points for the current node
        
    return nodes, rw_points

#Sorting nodes based on their random walk points in descending order
def nodes_sorting(nodes, points):
    points_array = np.array(list(points.values()))  # Extract values from the dictionary
    sorted_indices = np.argsort(-points_array)# Sorting indices in descending order of points
    sorted_nodes = [nodes[i] for i in sorted_indices] # Sorting nodes based on sorted indices
    return sorted_nodes

#Performing the functions defined above
nodes, rw_points = random_walk_with_teleportation(G, teleport_prob=0.15, num_steps=1000000)
sorted_nodes = nodes_sorting(nodes, rw_points)

# Printing the top 10 nodes with their random walk points
print("Node \t\t Random Walk Points")
for node in sorted_nodes[:10]:
    print(f"{node} \t {rw_points[node]}")

#Printing the leader with max random walk points
leader=sorted_nodes[0]
print ("The Top Leader=", leader)
