import numpy as np
from scipy.stats import norm

class NaiveBayes():

    def __init__(self, single_normal, num_classes=2, num_dims=300):
        self.single_normal = single_normal
        self.num_classes = num_classes
        self.num_dims = num_dims

    def classify(self, x):
        x_given_class = np.zeros((x))

        for c in range(self.num_classes):
            mus = self.single_normal[:, c, 0]
            sigmas = self.single_normal[:, c, 1]
            node_probs = norm.pdf(x, mus, sigmas)
            x_given_class[c] = np.prod(node_probs)

        return np.argmax(x_given_class)

    def classi(self, x):
        node_probs = norm.pdf(
            x, 
            self.single_normal[:, :, 0], 
            self.single_normal[:, :, 1]
        )
        x_given_class = np.prod(node_probs, axis=0)
        return np.argmax(x_given_class)

    def test(self, X, y):
        N, _ = X.shape
        correct = 0

        for i in range(N):
            x = X[i]
            prediction = self.classi(x)
            if prediction == y[i]:
                correct += 1

            if i % 100 == 0 and i != 0:
                print(f'Running Accuracy is {correct / i} for {i} samples')




        
        
