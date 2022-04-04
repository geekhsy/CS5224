import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.preprocessing import MinMaxScaler

from base_model import BaseModel
from constant import FOLD


class LightgbmModel(BaseModel):
    def train_model_KFold(self, X: pd.DataFrame, Y: pd.DataFrame, LightGBM_params: dict,
                          callbacks=None):
        if callbacks is None:
            callbacks = []

        kf = KFold(FOLD, shuffle=True)
        self.models = []
        for train_dix, val_idx in kf.split(X):
            X_train, X_val = X.iloc[train_dix], X.iloc[val_idx]
            Y_train, Y_val = Y.iloc[train_dix], Y.iloc[val_idx]
            eval_set = (X_val, Y_val)

            model = lgb.LGBMRegressor(**LightGBM_params)
            model.fit(X_train, Y_train,
                      eval_set=eval_set,
                      verbose=-1,
                      callbacks=callbacks,
                      )
            self.models += [model]

    def train_model(self, X_train, X_val, Y_train, Y_val, LightGBM_params: dict, callbacks=None):
        if callbacks is None:
            callbacks = []

        model = lgb.LGBMRegressor(**LightGBM_params)
        eval_set = (X_val, Y_val)
        model.fit(X_train, Y_train,
                  eval_set=eval_set,
                  verbose=-1,
                  callbacks=callbacks,
                  )
        self.models = [model]

    def feature_importance(self):
        model_importance = np.concatenate(
            [self.models[i].feature_importances_.reshape(-1, 1) for i in range(len(self.models))], axis=1)
        importance = np.average(model_importance, axis=1)
        importance = MinMaxScaler().fit_transform(importance.reshape(-1, 1)).reshape(-1)
        result = {}
        for i in range(len(importance)):
            result[self.models[0].feature_name_[i]] = importance[i]
        return result
