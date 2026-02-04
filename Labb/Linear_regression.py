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

    def _check_fitted(self):
        if self.b is None or self.X is None or self.y is None:
            raise RuntimeError('Model must be fitted before calling this method.')
        
    def fit(self, X, y):

        self.y = y

        ones = np.ones((X.shape[0], 1))
        X_matrix = np.hstack([ones, X])

        self.X = X_matrix
        self.n = X_matrix.shape[0]
        self.d = X_matrix.shape[1] - 1

        XtX = X_matrix.T @ X_matrix
        XtX_inv = np.linalg.pinv(XtX)
        XtY = X_matrix.T @ y

        self.b = XtX_inv @ XtY

        self.C = XtX_inv

    def var(self):
        self._check_fitted()
        
        n = self.n
        d = self.d

        y_hat = self.X @ self.b
        SSE = np.sum((self.y - y_hat)**2)
        self.sigma2 = SSE / (n-d-1)

        return self.sigma2
        
    def std(self):
        self._check_fitted()

        sigma2 = self.sigma2
        sigma = np.sqrt(sigma2)

        return sigma
    
    def RMSE(self):
        self._check_fitted()

        if self.sigma2 == None:
            self.var()
            
        return np.sqrt(self.sigma2)
