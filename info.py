# This script creates a symetric matrix containing the mutual information of the data

# Imports
import mat73
import numpy as np
import matplotlib.pyplot as plt
import time
import multiprocessing as m

# Custom dependencies
import probabilities as p

# Load the data
data_dict = mat73.loadmat('data/sub-01_task-rsvp_parsed.mat')
parsed = data_dict['parsed']


def buildI(data, i, j, I):
    start = time.perf_counter()
    I[i][j] = p.getI(data,i,j)
    finish = time.perf_counter()
    print(f'Finished in {round(finish-start, 2)} second(s)')

'''
if __name__ == '__main__':

    # Define matrix
    with m.Manager() as manager:
        L = manager.list()  # <-- can be shared between processes.
        L.extend(np.zeros((300,300)))
        processes = []
        for i in range(300):
            for j in range(i):
                p = m.Process(target=buildI, args=(parsed, i, j, L))  # Passing the list
                p.start()
                processes.append(p)
            for p in processes:
                p.join()
        I = L
'''

print(p.getI(parsed,1,3))


