# This script creates a symetric matrix of dictionaries for the probability of each node

# Imports
import numpy as np
import mat73

# Custom dependencies
import probabilities as p

# Change this to calculate parameters for 'visible' or 'position'
CLASS = 'visible'

# Load the directed graph
graph = np.load(('distributions/' + CLASS + '/intuitive/parents.npy'))

# Load the data
data_dict = mat73.loadmat('preprocessed_data/all_subjects/train.mat')
train = data_dict['train']


if __name__ == '__main__':

    # Get number of nodes N
    N = len(graph)

    # Get the unique values of the class
    c_range = np.unique(train[CLASS]).astype(int)
    cN = len(c_range)

    # Initialize final matrix
    single_normal = np.zeros((N,cN,2))
    mu_bar = np.zeros((N,cN,2))
    cov = np.zeros((N,cN,2,2))

    # Get all individual probs (prevent double calculations)
    idiv = np.zeros((N,cN,2))
    for i in range(N):
        print(i)
        for c in c_range:
            if CLASS == 'position':
                idiv[i][c-1] = p.getCx_pdf(train, i, c, CLASS, True)
            else:    
                idiv[i][c] = p.getCx_pdf(train, i, c, CLASS, True)

    # Get all joint probs
    N = len(graph)
    for i in range(N):
        print(i)
        parent = int(graph[i])
        for c in c_range:
            params = p.getJointCx_pdf(train, i, parent, c, CLASS, True)
            
            if CLASS == 'position':
                c_idx = c - 1
            else:
                c_idx = c

            mu_bar[i][c_idx] = params['mu']
            cov[i][c_idx] = params['cov']
            single_normal[i][c_idx] = idiv[parent][c_idx]

    # Save the data
    root = 'distributions/' + CLASS + '/intuitive/'
    np.save((root + 'mu_bar.npy'), mu_bar)
    np.save((root + 'cov.npy'), cov)
    np.save((root + 'single_normal.npy'), single_normal)
