import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error


class BaseModel:
    def __init__(self, model_dic: str, price_encoder):
        self.model_dic = model_dic
        self.price_encoder = price_encoder
        self.models = []

    def inverse(self, X: np.ndarray) -> np.ndarray:
        if self.price_encoder is None:
            return X
        return self.price_encoder.inverse_transform(X.reshape(-1, 1)).reshape(-1)

    def eval_models(self, X: pd.DataFrame, Y: pd.DataFrame) -> float:
        Y_predict = self.predict_inverse(X)
        Y_ori = self.inverse(Y.to_numpy())
        return mean_squared_error(Y_ori, Y_predict, squared=False)

    def predict_inverse(self, X: pd.DataFrame) -> np.ndarray:
        return self.inverse(self.predict(X))

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        Y_predict = [model.predict(X).reshape(-1, 1) for model in self.models]
        Y_avg = np.concatenate(Y_predict, axis=1).mean(axis=1)
        return Y_avg
