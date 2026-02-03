import numpy as np
import scipy.stats as st

class LinearRegression:
    def __init__(self, confidence_level=0.95):
        self.confidence_level = confidence_level

        self.b = None
        self.d = None
        self.n = None
        self.X = None
        self.y = None
        self.sigma2 = None
        self.C = None

    def fit(self, X, y):

        self.y = y

        ones = np.ones((X.shape[0], 1))
        X_matrix = np.hstack([ones, X])

        self.X = X_matrix
        self.n = X_matrix.shape[0]
        self.d = X_matrix.shape[1] - 1


