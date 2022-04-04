import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.preprocessing import MinMaxScaler
from xgboost import DMatrix, train

from base_model import BaseModel
from constant import FOLD


class XGBoostModel(BaseModel):
    def train_model_KFold(self, X: pd.DataFrame, Y: pd.DataFrame, XGBoost_params: dict,
                          callbacks=None):
        if callbacks is None:
            callbacks = []

        kf = KFold(FOLD, shuffle=True)
        self.models = []
        for train_dix, val_idx in kf.split(X):
            X_train, X_val = X.iloc[train_dix], X.iloc[val_idx]
            Y_train, Y_val = Y.iloc[train_dix], Y.iloc[val_idx]
            train_matrix = DMatrix(X_train, Y_train, enable_categorical=True)
            val_matrix = DMatrix(X_val, Y_val, enable_categorical=True)

            model = train(XGBoost_params, train_matrix,
                          num_boost_round=XGBoost_params['num_boost_round'],
                          early_stopping_rounds=XGBoost_params['early_stopping_rounds'],
                          evals=[(val_matrix, 'eval')],
                          callbacks=callbacks,
                          )
            self.models += [model]

    def train_model(self, X_train, X_val, Y_train, Y_val, XGBoost_params: dict, callbacks=None):
        if callbacks is None:
            callbacks = []

        train_matrix = DMatrix(X_train, Y_train, enable_categorical=True)
        val_matrix = DMatrix(X_val, Y_val, enable_categorical=True)

        model = train(XGBoost_params, train_matrix,
                      num_boost_round=XGBoost_params['num_boost_round'],
                      early_stopping_rounds=XGBoost_params['early_stopping_rounds'],
                      evals=[(val_matrix, 'eval')],
                      callbacks=callbacks,
                      )
        self.models = [model]

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        Y_predict = [model.predict(DMatrix(X, enable_categorical=True)).reshape(-1, 1) for model in self.models]
        Y_avg = np.concatenate(Y_predict, axis=1).mean(axis=1)
        return Y_avg

    def feature_importance(self):
        importance_dicts = [self.models[i].get_score() for i in range(len(self.models))]
        result = {}
        for k in importance_dicts[0].keys():
            result[k] = np.average([importance_dicts[i][k] for i in range(len(self.models))])
        feature_names = list(result.keys())
        importance = np.array([result[name] for name in feature_names])
        importance = MinMaxScaler().fit_transform(importance.reshape(-1, 1)).reshape(-1)
        for i in range(len(feature_names)):
            result[feature_names[i]] = importance[i]
        return result
