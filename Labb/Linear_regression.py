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
        self._y_hat = None
        self.XtX_inv = None

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

        self.XtX_inv = np.linalg.pinv(X.T @ X)
        self.b = self.XtX_inv @ (self.X.T @ self.y)

        self.sigma2 = None
        self.C = None
        self._y_hat = None
        self.y = y

    @property
    def y_hat(self):
        self._check_fitted()
        if self._y_hat is None:
            self._y_hat = (self.X @ self.b).reshape(-1)
        return self._y_hat

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
        """Returns Root of mean squared errors (RMSE)"""
        self._check_fitted()

        RMSE = np.sqrt(self.MSE())
        return RMSE
    
    def Syy(self):
        """Total sum of squares: sum((y - y_mean)^2)."""
        self._check_fitted()
        y_mean = np.mean(self.y)
        Syy = np.sum((self.y - y_mean) **2)
        return Syy

    def SSR(self):
        """Regression sum of squares: Syy -SSE"""
        self._check_fitted()
        SSR = self.Syy() - self.SSE()
        return SSR
    
    def var(self):
        """Beräkna och spara unbiased estimator för sigma^2 och kovariansmatris C. Returns sigma2 (variance)."""
        self._check_fitted()
        
        n = self.n
        d = self.d

        self.sigma2 = self.SSE() / (n-d-1)
        self.C = self.sigma2 * self.XtX_inv
        return self.sigma2
        
    def residual_std(self):
        """Returns standard deviation."""
        self._check_fitted()

        if self.sigma2 is None:
            self.var()

        return np.sqrt(self.sigma2)
    
    def significance(self):
        """Returns the significance of the regression. F and p values."""
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
    
    def residuals(self):
        r = self.y - self.y_hat
        return r
    
    def confidence_interval(self, alpha=None):
        """Evaluates the confidelce intervals for the regression. Input alpha between 0-1, standard is 0.95."""
        
        if alpha is None:
            alpha = 1 - self.confidence_level
        else:
            alpha = float(alpha)
        if self.sigma2 is None:
            self.var()
        df = self.n - self.d -1
        se = np.sqrt(np.diag(self.C))
        t_crit = st.t.ppf(1 - alpha / 2, df)
        
        lower = self.b - t_crit * se
        upper = self.b + t_crit * se

        return np.column.stack([lower, upper])
    
    def r_squared(self):
        self._check_fitted()

        r_squared = self.SSR() / self.syy()
        return r_squared
    


