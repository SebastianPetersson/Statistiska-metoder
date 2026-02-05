import numpy as np
import scipy.stats as st

class LinearRegression:
    def __init__(self, confidence_level=0.95):
        self.confidence_level = confidence_level

        self.X = None
        self.y = None
        self.b = None
        self.d = None
        self.n = None

        self.sigma2 = None
        self.C = None
        self.y_hat = None

    def _check_fitted(self):
        if self.b is None or self.X is None or self.y is None:
            raise RuntimeError('Model must be fitted before calling this method.')
        
    def y_hat(self):
        if self.y_hat is None:
            self.y_hat = self.X @ self.b
        return self.y_hat
    
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

    def SSE(self):
        """Returns sum of squared errors: sum((y - Xb)**2)"""
        self._check_fitted()

        SSE = np.sum((self.y - self.y_hat)**2)
        return SSE
    
    def MSE(self):
        """Returns the mean of squared errors (mean of SSE)"""
        self._check_fitted()

        residuals = self.y - self.y_hat
        MSE = np.mean(residuals**2)
        return MSE

    def RMSE(self):
        self._check_fitted()

        RMSE = np.sqrt(self.MSE())
        return RMSE
    
    def var(self):
        self._check_fitted()
        
        n = self.n
        d = self.d

        self.sigma2 = self.SSE() / (n-d-1)

        return self.sigma2
        
    def std(self):
        self._check_fitted()

        if self.sigma2 is None:
            self.var()

        return np.sqrt(self.sigma2)
    
    def significance(self):
        self._check_fitted()

        d = self.d
        n = self.n
        
        SSE = self.SSE()
        y_mean = np.mean(self.y)
        Syy = np.sum((self.y-y_mean)**2)
        SSR = Syy - SSE

        F = (SSR/d) / (SSE/(n-d-1))
        p = st.f.sf(F, d, n-d-1)
        return F, p

        