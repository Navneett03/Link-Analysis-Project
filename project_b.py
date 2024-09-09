import numpy as np
import networkx as nx
import pandas as pd

def predict_zero_values(adj_matrix):
    zero_indices = np.argwhere(adj_matrix == 0)  # Finding indices of zeroes in the matrix
    if len(zero_indices) == 0:
        print("No zero found in the adjacency matrix.")
        return None

    predicted_values = []#List for storing the predicted values

    for zero_index in zero_indices:
        row, col = zero_index #Rows and columns corresponding to zeroes in the matrix
        deleted_row = adj_matrix[row]# Extracting the row containing the zero
        deleted_row = np.delete(deleted_row, col, axis=0)# Deleting the zero element from the row
        deleted_col = adj_matrix[:, col]# Extracting the column containing the zero
        deleted_col = np.delete(deleted_col, row, axis=0) # Deleting the zero element from the column

        # Deleting row and column
        adj_matrix_temp = np.delete(adj_matrix, row, axis=0)# Deleting the row from the adjacency matrix
        adj_matrix_temp = np.delete(adj_matrix_temp, col, axis=1)# Deleting the column from the adjacency matrix

        # Expressing deleted row as linear combination of remaining rows using numpy built in function (matrix method)
        '''working of the built in function used here:

        np.linalg.lstsq: This function computes the least-squares solution to a linear matrix equation. It is commonly used when you have an overdetermined system of linear equations, meaning there are more equations than unknowns.

        adj_matrix_temp.T: This is the matrix of independent variables , it represents the remaining rows of the adjacency matrix after deleting the row corresponding to the zero element.
        
        deleted_row: This is the dependent variable vector, representing the row containing the zero element that we want to express as a linear combination of the remaining rows.

        rcond=None: This argument specifies the cutoff for small singular values. When rcond is set to None, NumPy internally determines the threshold for determining rank of the coefficient matrix, which is used to solve the least squares problem. It essentially controls the numerical stability of the solution.

        [0]: The result of np.linalg.lstsq is a tuple containing several elements, including the solution to the least squares problem. By accessing element [0], we're extracting the solution coefficients from the tuple.
                '''
        coefficients = np.linalg.lstsq(adj_matrix_temp.T, deleted_row, rcond=None)[0]

        # Predicting the value of the zero in the deleted row/column
        predicted_value = np.dot(coefficients, deleted_col)

        # Storing the predicted value along with its index
        predicted_values.append((zero_index, predicted_value))

    return predicted_values


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

adj_matrix = nx.adjacency_matrix(G).todense()# Generating the adjacency matrix from the graph

predicted_values = predict_zero_values(adj_matrix)# Predicting zero values in the adjacency matrix
missing_links = []# List to store missing links
persons = list(G.nodes())# List of persons in the graph so that i can get the entry no. of the students corresponding to its index in adjacency matrix
for zero_index, predicted_value in predicted_values:
    
    if predicted_value > 0.6:# Checking if predicted value exceeds a threshold
        i,j = zero_index# Extracting row and column indices
        missing_links.append((persons[i], persons[j]))# Storing missing links in the form of entry no. of the students
        G.add_edge(persons[i], persons[j])# Adding missing links to the graph

# Printing missing links
print("missing links")
for m in missing_links:
    print(m)


