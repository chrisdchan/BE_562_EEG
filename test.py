import numpy as np
import multiprocessing as m
import time

def calPDF(x,j):
    x[j] = j
    time.sleep(1)



if __name__ == '__main__':

    with m.Manager() as manager:
        L = manager.list()  # <-- can be shared between processes.
        L.extend(np.zeros(10))
        processes = []
        for i in range(10):
            p = m.Process(target=calPDF, args=(L,i))  # Passing the list
            p.start()
            processes.append(p)
        for p in processes:
            p.join()
        print(L)

