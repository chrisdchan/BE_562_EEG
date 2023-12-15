import numpy as np
from scipy.stats import multivariate_normal, norm
import math

class Model():

    def __init__(self, single_normal, mu_bar, cov, parents, num_classes=2, num_dims=300):
        self.single_normal = single_normal
        self.mu_bar = mu_bar
        self.cov = cov
        self.parents = parents

        self.num_classes = num_classes
        self.num_dims = num_dims

        self.mu_parents = single_normal[parents, :, 0]
        self.sig_parents = single_normal[parents, :, 1]

    def _normal_pdf(self, x, mu, sigma):
        coef = 1 / (sigma * math.sqrt(2 * math.pi))
        return coef * math.exp(-0.5 * math.pow((x - mu) / sigma, 2))

    def classify(self, x):
        likelihood = np.ones((self.num_classes,))
        for c in range(self.num_classes):

            node_probabilities = np.ones((self.num_dims, ))

            mu_0 = self.single_normal[0][c][0]
            sigma_0 = self.single_normal[0][c][1]

            node_probabilities[0] = self._normal_pdf(x[0], mu_0, sigma_0)

            for node in range(1, self.num_dims):
                mu_bar = self.mu_bar[node, c]
                cov = self.cov[node, c]

                mu_parent = self.mu_parents[node, c]
                sigma_parent = self.sig_parents[node, c]

                node_value = x[node]
                parent_value = x[self.parents[node]]
                joint_value = np.array([node_value, parent_value])

                joint_prob = multivariate_normal.pdf(joint_value, mu_bar, cov)
                parent_prob = self._normal_pdf(parent_value, mu_parent, sigma_parent)
                node_probabilities[node] = joint_prob / parent_prob

            log_node_probabilities = np.log(node_probabilities)
            likelihood[c] = np.sum(log_node_probabilities)

        return np.argmax(likelihood)

    def run_test(self, X, y):
        N, _ = X.shape

        correct = 0
        correct_local = 0

        for i in range(N):
            x = X[i]
            prediction = self.classify(x)

            if prediction == y[i]:
                correct += 1
                correct_local += 1

            if i % 100 == 0 and i != 0:
                print(f'Running Accuracy: {correct / i} windowed: {correct_local / 100} for {i} samples')
                correct_local = 0

        accuracy = correct / N
        print(f'Accuracy is {accuracy}')
