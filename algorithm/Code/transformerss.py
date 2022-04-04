import numpy as np
from scipy.special import inv_boxcox
from scipy.stats import boxcox
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.manifold import TSNE


class BoxCoxTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, Y=None, **fit_params_steps):
        self.lmbdas = [boxcox(X[:, i] + 1e-6)[1] for i in range(X.shape[1])]
        return self

    def transform(self, X, Y=None, **fit_params_steps):
        return np.concatenate([boxcox(X[:, i] + 1e-6, self.lmbdas[i]).reshape(-1, 1) for i in range(X.shape[1])],
                              axis=1)

    def inverse_transform(self, X, Y=None, **fit_params_steps):
        return np.concatenate([(inv_boxcox(X[:, i], self.lmbdas[i]) - 1e-6).reshape(-1, 1) for i in range(X.shape[1])],
                              axis=1)


class TSNETransformer(TSNE, TransformerMixin):
    def __init__(self, n_components=2):
        super().__init__(n_components=n_components)

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return super().fit_transform(X, y)
