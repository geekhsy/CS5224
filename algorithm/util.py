import os

import joblib
import numpy as np
import pandas as pd

from catboost_model import CatBoostModel
from constant import PREDICT_DIC, MODEL_DIC, CATEGORY_COLUMN, TREE_MODEL, LightGBM_params, XGBoost_params, \
    CatBoost_params
from lightgbm_model import LightgbmModel
from xgboost_model import XGBoostModel


def construct_df(model, X: pd.DataFrame) -> pd.DataFrame:
    predict_prices = model.predict_inverse(X)

    predict_result = pd.DataFrame({'ID': [i for i in range(len(predict_prices))], 'Predicted': predict_prices})
    return predict_result


def write_to_csv(output_data: pd.DataFrame, file_name: str):
    if not os.path.exists(PREDICT_DIC):
        os.makedirs(PREDICT_DIC)

    output_data.to_csv(os.path.join(PREDICT_DIC, f'{file_name}.csv'),
                       index=False)


def save_data_to_disk(saving_data, time_string: str):
    if not os.path.exists(MODEL_DIC):
        os.mkdir(MODEL_DIC)
    models_path = os.path.join(MODEL_DIC, f'{time_string}.pkl')
    joblib.dump(saving_data, models_path)


def load_data_from_disk(time_string: str):
    models_path = os.path.join(MODEL_DIC, f'{time_string}.pkl')
    return joblib.load(models_path)


def get_data_model(X_train: pd.DataFrame, X_holdout: pd.DataFrame, X_test: pd.DataFrame, price_encoder):
    re = []

    cat_col = CATEGORY_COLUMN + ['k_means_fea']
    if TREE_MODEL in ['lightgbm', 'all']:
        x_train, x_holdout, x_test = X_train.copy(), X_holdout.copy(), X_test.copy()
        x_train[cat_col] = x_train[cat_col].astype('category')
        x_holdout[cat_col] = x_holdout[cat_col].astype('category')
        x_test[cat_col] = x_test[cat_col].astype('category')
        param = LightGBM_params
        model = LightgbmModel(MODEL_DIC, price_encoder)
        re += [(x_train, x_holdout, x_test, param, model)]
    if TREE_MODEL in ['xgboost', 'all']:
        x_train, x_holdout, x_test = X_train.copy(), X_holdout.copy(), X_test.copy()
        x_train[cat_col] = x_train[cat_col].astype('category')
        x_holdout[cat_col] = x_holdout[cat_col].astype('category')
        x_test[cat_col] = x_test[cat_col].astype('category')
        param = XGBoost_params
        model = XGBoostModel(MODEL_DIC, price_encoder)
        re += [(x_train, x_holdout, x_test, param, model)]
    if TREE_MODEL in ['catboost', 'all']:
        x_train, x_holdout, x_test = X_train.copy(), X_holdout.copy(), X_test.copy()

        x_train[cat_col] = x_train[cat_col].astype(str)
        x_holdout[cat_col] = x_holdout[cat_col].astype(str)
        x_test[cat_col] = x_test[cat_col].astype(str)
        param = CatBoost_params
        model = CatBoostModel(MODEL_DIC, price_encoder)
        re += [(x_train, x_holdout, x_test, param, model)]
    return re


def get_final_y_predict(Y_pre: [pd.DataFrame]) -> pd.DataFrame:
    y_data = np.mean([y['Predicted'].to_numpy() for y in Y_pre], axis=0)
    Y_pre[0]['Predicted'] = y_data
    return Y_pre[0]


def ultimate_train_predict(data_model_list, Y_train, Y_holdout):
    Y_pre = []
    saving_data = []
    for x_train, x_holdout, x_test, param, model in data_model_list:
        # train models
        cat_col = CATEGORY_COLUMN + ['k_means_fea']

        x_all, y_all = pd.concat([x_train, x_holdout], axis=0), pd.concat([Y_train, Y_holdout], axis=0)
        if isinstance(x_train[cat_col[0]].dtype, pd.CategoricalDtype):
            x_all[cat_col] = x_all[cat_col].astype('category')

        model.train_model_KFold(x_all, y_all, param)
        saving_data += [(model, x_test)]

        # make predict
        Y_predict = construct_df(model, x_test)
        Y_pre += [Y_predict]
    Y_final = get_final_y_predict(Y_pre)
    return saving_data, Y_final


def ultimate_loaded_model_predict(loaded_model) -> pd.DataFrame:
    Y_pre = []
    print(loaded_model)
    for model, x_test in loaded_model:
        print('model',model)
        print('\n x',x_test)
        Y_predict = construct_df(model, x_test)
        # print('Y_predict',Y_predict)
        Y_pre += [Y_predict]
        # print('Y_pre',Y_pre)
        print('next\n')
    Y_final = get_final_y_predict(Y_pre)
    print('finaly',Y_final)
    return Y_final
 

