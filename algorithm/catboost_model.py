import numpy as np
import pandas as pd
from catboost import CatBoostRegressor, Pool
from sklearn.model_selection import KFold
from sklearn.preprocessing import MinMaxScaler

from base_model import BaseModel
from constant import CATEGORY_COLUMN, FOLD


class CatBoostModel(BaseModel):
    def train_model_KFold(self, X: pd.DataFrame, Y: pd.DataFrame, CatBoost_params: dict):
        cat_col = CATEGORY_COLUMN + ['k_means_fea']
        self.feature_names = list(X.columns)

        kf = KFold(FOLD, shuffle=True)
        self.models = []
        for train_dix, val_idx in kf.split(X):
            X_train, X_val = X.iloc[train_dix], X.iloc[val_idx]
            Y_train, Y_val = Y.iloc[train_dix], Y.iloc[val_idx]

            train_pool = Pool(X_train, Y_train, cat_col)
            val_pool = Pool(X_val, Y_val, cat_col)

            model = CatBoostRegressor(**CatBoost_params)
            model.fit(train_pool, eval_set=val_pool)
            self.models += [model]

    def train_model(self, X_train: pd.DataFrame, X_val: pd.DataFrame, Y_train: pd.DataFrame, Y_val: pd.DataFrame,
                    CatBoost_params: dict) -> [CatBoostRegressor]:
        cat_col = CATEGORY_COLUMN + ['k_means_fea']
        self.feature_names = list(X_train.columns)

        train_pool = Pool(X_train, Y_train, cat_col)
        val_pool = Pool(X_val, Y_val, cat_col)

        model = CatBoostRegressor(**CatBoost_params)
        model.fit(train_pool, eval_set=val_pool)
        self.models = [model]

    def feature_importance(self):
        model_importance = np.concatenate(
            [self.models[i].get_feature_importance().reshape(-1, 1) for i in range(len(self.models))], axis=1)
        importance = np.average(model_importance, axis=1)
        importance = MinMaxScaler().fit_transform(importance.reshape(-1, 1)).reshape(-1)
        names = self.feature_names
        result = {}
        for i in range(len(importance)):
            result[names[i]] = importance[i]
        return result
