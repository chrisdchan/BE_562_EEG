# Function definitions for the probabilities for mutual information
import numpy as np
import math
from scipy import stats
import multiprocessing as m
import time
from scipy import integrate





def seen(data, state=True):
    "This function returns the P(C)"

    total = len(data)
    condition = 0
    for i in range(total):
        if data[i] == 1:
            condition += 1

    prob = condition/total

    if state == True:
        return prob
    else:
        return 1-prob
    
def getCx_pdf(data, x, C):
    "This function returns the mu and sigma for the P(x, C)"

    # Find mu and sigma
    list = []
    for i in range(len(data['data'])):
        if data['visible'][i] == C:
            list.append(data['data'][i][x])
    mu = sum(list)/len(list)
    std = np.std(list)

    return stats.norm(mu, std)

def getJointCx_pdf(data, x1, x2, C):
    "This function returns the mu and sigma for the joint gaussian P(x1, x2 | C)"

    def getLists(data, i, x1, x2, L1, L2):
        if data['visible'][i] == C:
            L1.append(data['data'][i][x1])
            L2.append(data['data'][i][x2])

    # Find mu and sigma
    list1 = []
    list2 = []
    for i in range(len(data['data'])):
        if data['visible'][i] == C:
            list1.append(data['data'][i][x1])
            list2.append(data['data'][i][x2])

    mu1 = np.mean(list1)
    mu2 = np.mean(list2)
    cov = np.cov(list1, list2)
    mu = [mu1, mu2]

    params = {
        "mu": mu,
        "cov": cov
    }

    return stats.multivariate_normal(mu, cov)


def getI(data, X1, X2):

    Ctrue = seen(data['visible'])
    Cfalse = 1 - Ctrue

    I = 0
    epsilon = 0.000000001 

    def calculate(y, x, pC, joint, x1pdf, x2pdf):
        p0 = joint.pdf([y,x])
        p1 = p0*pC
        p2 = x1pdf.pdf(y)
        p3 = x2pdf.pdf(x)

        iter = p1*math.log(((p1*pC)/(p2*p3))+epsilon)

        return iter
    
    for c in range(2):
        start = time.perf_counter()

        joint = getJointCx_pdf(data, X1, X2, c)
        x1pdf = getCx_pdf(data, X1, c)
        x2pdf = getCx_pdf(data, X2, c)
        finish = time.perf_counter()

        print(f'Finished in {round(finish-start, 2)} second(s)')

        if c == 1:
            pC = Ctrue
        else:
            pC = Cfalse

        I += integrate.dblquad(calculate, -60, 60, -60, 60, args=(pC, joint, x1pdf, x2pdf))[0]
        
    return I

