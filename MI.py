# This script creates a symetric matrix containing the mutual information of the data

# Imports
import mat73
import numpy as np
import time
import multiprocessing as m

# Custom dependencies
import probabilities as p

# Load the data
data_dict = mat73.loadmat('preprocessed_data/train.mat')
parsed = data_dict['train']

print(m.cpu_count())


def buildI(data, i, j, I):
    a = p.getI(data,i,j)

    tmp = I[i]
    tmp[j] = a
    I[i] = tmp

    tmp = I[j]
    tmp[i] = a
    I[j] = tmp


if __name__ == '__main__':

    currentI = np.load('distributions/I.npy')

    # Define matrix
    with m.Manager() as manager:
        L = manager.list()  # <-- can be shared between processes.
        L.extend(currentI)
        for i in range(300):
            print(i)
            start = time.perf_counter()
            processes = []
            for j in range(i):
                pr = m.Process(target=buildI, args=(parsed, i, j, L))  # Passing the list
                pr.start()
                processes.append(pr)
                
            for process in processes:
                process.join()    
            finish = time.perf_counter()
            print(f'Finished in {round(finish-start, 2)} second(s)')
            np.save('distributions/I.npy', L)

