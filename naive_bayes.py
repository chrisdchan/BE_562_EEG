import numpy as np
from scipy.stats import norm, multivariate_normal

class NaiveBayes():
    def __init__(self, single_normal, priors, num_classes=2, num_dims=300):
        self.single_normal = single_normal
        self.num_classes = num_classes
        self.num_dims = num_dims
        self.priors = priors

    def classify(self, x):
        likelihood = np.zeros((self.num_classes, ))

        for c in range(self.num_classes):
            mus = self.single_normal[:, c, 0]
            sigmas = self.single_normal[:, c, 1]
            node_probs = norm.pdf(x, mus, sigmas)
            log_node_probs = np.log(node_probs)
            likelihood[c] = np.sum(log_node_probs) + self.priors[c]

        return np.argmax(likelihood)

    def test(self, X, y):
        N, _ = X.shape
        correct = 0

        for i in range(N):
            x = X[i]
            prediction = self.classify(x)

            if prediction == y[i]:
                correct += 1

            if i % 500 == 0 and i != 0:
                print(f'Running Accuracy is {correct / i} for {i} samples')