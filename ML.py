# This script creates a symetric matrix of dictionaries for the probability of each node

# Imports
import numpy as np
import mat73

# Custom dependencies
import probabilities as p

# Load the directed graph
graph = np.load('parents.npy')


# Load the data
data_dict = mat73.loadmat('preprocessed_data/train.mat')
train = data_dict['train']


if __name__ == '__main__':

    # Get number of nodes N
    N = len(graph)

    # Initialize final matrix
    single_normal = np.zeros((N,2,2))
    mu_bar = np.zeros((N,2,2))
    cov = np.zeros((N,2,2,2))

    # Get all individual probs (prevent double calculations)
    idiv = np.zeros((N,2,2))
    for i in range(N):
        print(i)
        for c in range(2):
            idiv[i][c] = p.getCx_pdf(train, i, c, True)

    # Get all joint probs
    N = len(graph)
    for i in range(N):
        print(i)
        parent = int(graph[i])
        for c in range(2):
            params = p.getJointCx_pdf(train, i, parent, c, True)
            mu_bar[i][c] = params['mu']
            cov[i][c] = params['cov']
            single_normal[i][c] = idiv[parent][c]

    
    
        
    np.save('node_probs/mu_bar.npy', mu_bar)
    np.save('node_probs/cov.npy', cov)
    np.save('node_probs/single_normal.npy', single_normal)
