# Function definitions for the probabilities for mutual information
import numpy as np
from math import log
from scipy import stats, integrate

def pClass(data, state):
    """
    returns the probability of a class

    param data: a list of class integers
    param state: current state
    return: P(C)
    """

    total = len(data)
    condition = 0
    for i in range(total):
        if data[i] == state:
            condition += 1

    prob = condition/total

    return prob

    
def getCx_pdf(data, X, C, class_type="visible", return_params=False):
    """
    returns the mu and sigma for the P(x|C)

    param data: data structure
    param X: attribute #
    param C: value of the given class
    param class_type: string of the structure key for the class (default is 'visible')
    param return_params: return model parameters instead of the distribution object
    return: P(x|C) distribution
    """

    # Find mu and sigma
    list = []
    for i in range(len(data['data'])):
        if data[class_type][i] == C:
            list.append(data['data'][i][X])
    mu = np.mean(list)
    std = np.std(list)

    # Return the paramerters or the distribution object
    if return_params == False:
        return stats.norm(mu, std)
    else:
        return [mu, std]


def getJointCx_pdf(data, X1, X2, C, class_type="visible", return_params=False):
    """
    returns the distribution for the joint gaussian of two attributes P(x1, x2 | C)

    param data: data structure
    param X1: first attribute #
    param X1: second attribute #
    param C: value of the given class
    param class_type: string of the structure key for the class (default is 'visible')
    param return_params: return model parameters instead of the distribution object
    return: P(x1, x2 | C) distribution
    """

    # Find mu and sigma
    list1 = []
    list2 = []
    for i in range(len(data['data'])):
        if data[class_type][i] == C:
            list1.append(data['data'][i][X1])
            list2.append(data['data'][i][X2])

    mu1 = np.mean(list1)
    mu2 = np.mean(list2)
    cov = np.cov(list1, list2)
    mu = [mu1, mu2]

    params = {
        "mu": mu,
        "cov": cov
    }

    if return_params == False:
        return stats.multivariate_normal(mu, cov)
    else:
        return params



def getI(data, X1, X2, class_type="visible"):
    """
    returns the mutual information between two attributes X1 and X2

    param data: data structure
    param X1: first attribute #
    param X1: second attribute #
    param class_type: string of the structure key for the class (default is 'visible')
    return: mutual information between two attributes X1 and X2
    """

    # Initialize information and an epsilon
    I = 0
    epsilon = 0.0000000000000001 

    # Define the integrand for integration
    def integrand(y, x, joint, x1pdf, x2pdf):
        p0 = joint.pdf([y,x])
        p2 = x1pdf.pdf(y)
        p3 = x2pdf.pdf(x)

        iter = p0*log(((p0)/(p2*p3))+epsilon)

        return iter

    # Get the unique values of the class
    c_range = np.unique(data[class_type]).astype(int)

    # Sum mutal information for each class
    for c in c_range:
        joint = getJointCx_pdf(data, X1, X2, c, class_type)
        x1pdf = getCx_pdf(data, X1, c, class_type)
        x2pdf = getCx_pdf(data, X2, c, class_type)

        pC = pClass(data[class_type], c)

        I += integrate.dblquad(integrand, -60, 60, -60, 60, args=(joint, x1pdf, x2pdf))[0]*pC

    return I
