import numpy as np
import scipy.stats as st
import pandas as pd

class LinearRegression:
    def __init__(self, confidence_level=0.95):
        self.confidence_level = confidence_level
        self.X = None
        self.y = None
        self.b = None
        self.d = None
        self.n = None
        self.sigma2 = None
        self.cov_matrix = None
        self._y_hat = None
        self.XtX_inv = None

    def _check_fitted(self):
        if self.b is None or self.X is None or self.y is None:
            raise RuntimeError('Model must be fitted before calling this method.')

    
    def fit(self, X, y):
        y = np.asarray(y).reshape(-1)
        ones = np.ones((X.shape[0], 1))
        X_matrix = np.hstack([ones, X])

        self.X = X_matrix
        self.y = y
        self.n = X_matrix.shape[0]
        self.d = X_matrix.shape[1] - 1

        self.XtX_inv = np.linalg.pinv(self.X.T @ self.X)
        self.b = self.XtX_inv @ (self.X.T @ self.y)

        self.sigma2 = None
        self.cov_matrix = None
        self._y_hat = None

    @property
    def y_hat(self):
        self._check_fitted()
        if self._y_hat is None:
            self._y_hat = (self.X @ self.b).reshape(-1)
        return self._y_hat

    def residuals(self):
        """Returns residuals between actual y and expected y."""
        r = self.y - self.y_hat
        return r
    
    def sse(self):
        """Returns sum of squared errors: sum((y - Xb)**2)"""
        self._check_fitted()

        sse = np.sum((self.y - self.y_hat)**2)
        return sse
    
    def mse(self):
        """Returns mean squared error: SSE / n"""
        self._check_fitted()
        return self.sse() / (self.n-self.d-1)

    def rmse(self):
        """Returns Root of mean squared errors (RMSE)"""
        self._check_fitted()

        rmse = np.sqrt(self.mse())
        return rmse
    
    def syy(self):
        """Total sum of squares: sum((y - y_mean)^2)."""
        self._check_fitted()
        y_mean = np.mean(self.y)
        syy = np.sum((self.y - y_mean) **2)
        return syy

    def ssr(self):
        """Regression sum of squares: syy -sse"""
        self._check_fitted()
        ssr = self.syy() - self.sse()
        return ssr
    
    def r_squared(self):
        self._check_fitted()

        r_squared = self.ssr() / self.syy()
        return r_squared
    
    def var(self):
        """Estimates and saves unbiased estimator for sigma^2 and cov_matrix. Returns sigma2 (variance)."""
        self._check_fitted()
        
        n = self.n
        d = self.d

        self.sigma2 = self.sse() / (n-d-1)
        self.cov_matrix = self.sigma2 * self.XtX_inv
        return self.sigma2

        
    def std(self):
        """Returns standard deviation."""
        self._check_fitted()

        if self.sigma2 is None:
            self.var()

        return np.sqrt(self.sigma2)
    
    def significance(self):
        """Returns the significance of the regression. F-statistic and p value."""
        self._check_fitted()
        d = self.d
        n = self.n
        
        F = (self.ssr()/d) / (self.sse()/(n-d-1))
        p = st.f.sf(F, d, (n-d-1))
        return F, p
    
    def parameter_significance(self):
        """t-test and p-values for individual parameters"""
        self._check_fitted()

        n = self.n
        d = self.d

        if self.sigma2 is None:
            self.var()

        se = np.sqrt(np.diag(self.cov_matrix))
        t_vals = self.b / se

        p_vals = 2 * np.minimum(
            st.t.cdf(t_vals, (n-d-1)),
            st.t.sf(t_vals, (n-d-1))
        )

        return t_vals, p_vals
    
    def confidence_interval(self, alpha=None):
        """Evaluates the confidence intervals for the regression. Input alpha between 0-1, standard is 0.95."""
        
        d = self.d
        n = self.n

        if alpha is None:
            alpha = 1 - self.confidence_level
        else:
            alpha = float(alpha)
        if self.sigma2 is None:
            self.var()

        se = np.sqrt(np.diag(self.cov_matrix))
        t_crit = st.t.ppf(1 - alpha / 2, (n-d-1))
        
        lower = self.b - t_crit * se
        upper = self.b + t_crit * se

        return np.column_stack([lower, upper])

    def pearson_corr(self):
        """Calculates the Pearson number between all pairs of parameters."""

        self._check_fitted()

        X = self.X[:, 1:]
        n, p = X.shape
        
        corr = np.eye(p)

        for i in range(p):
            for j in range(i+1, p):
                Xi = X[:, i]
                Xj = X[:, j]

                Xi_c = Xi - Xi.mean()
                Xj_c = Xj - Xj.mean()

                numerator = np.sum(Xi_c * Xj_c)
                denom = np.sqrt(np.sum(Xi_c**2) * np.sum(Xj_c**2))

                r = numerator / denom if denom != 0 else 0.0

                corr[i,j] = r
                corr[j, i] = r

        return corr
    
    def summary_basic(self, title=None):
        self._check_fitted()

        F, p = self.significance()

        summary = pd.DataFrame([{
            'n' : self.n,
            'd' : self.d,
            'R2' : np.round(self.r_squared(), 4),
            'Variance' : np.round(self.var(), 2),
            'Standard deviation' : np.round(self.std(), 2),
            'rmse' : np.round(self.rmse(), 2),
            'F-statistic': np.round(F, 2),
            'P-value' : np.round(p, 2)
        }], index = [f'{title} summary']
        )

        return summary
    
    def summary_coef(self, param_names=None):
        self._check_fitted()

        t_vals, p_vals = self.parameter_significance()
        ci = self.confidence_interval()
        se = np.sqrt(np.diag(self.cov_matrix))

        summary = pd.DataFrame({
            'Parameter': param_names,
            'Beta': np.round(self.b, 2),
            'Std.Err': np.round(se, 2),
            't': np.round(t_vals, 2),
            'p': np.round(p_vals, 2),
            'CI lower': np.round(ci[:, 0], 2),
            'CI upper': np.round(ci[:, 1], 2)
        })

        return summary