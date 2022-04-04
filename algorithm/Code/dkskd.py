import warnings
import warnings

import numpy as np

from base_model import BaseModel
from constant import ORIGINAL_DATA_DIC, TEXT_FEA_DIC, TRAIN_FILE, TEST_FILE, MODEL_DIC
from preprocessing import load_data
from util import get_data_model

warnings.filterwarnings("ignore")

X_train, X_holdout, X_test, Y_train, Y_holdout, price_encoder = load_data(ORIGINAL_DATA_DIC, TRAIN_FILE, TEST_FILE,
                                                                          TEXT_FEA_DIC)
data_model_list = get_data_model(X_train, X_holdout, X_test, price_encoder)
bmodel = BaseModel(MODEL_DIC, price_encoder)

print('-' * 50)
print('Training models')
figures = []
for x_train, x_holdout, x_test, param, model in data_model_list:
    # train models
    model.train_model(x_train, x_holdout, Y_train, Y_holdout, param)
    feature_importance_dic = model.feature_importance()
    print(feature_importance_dic)
    figures.append(feature_importance_dic)

    # evaluate models
    print('-' * 50)
    print('Evaluating models')
    rmse_train, rmse_holdout = model.eval_models(x_train, Y_train), model.eval_models(x_holdout, Y_holdout)
    print('RMSE:')
    print(f'train:{rmse_train}')
    print(f'holdout:{rmse_holdout}')

X_train.info()

Y_pres = []
for x_train, x_holdout, x_test, param, model in data_model_list:
    pre = model.predict_inverse(x_train).reshape(-1, 1)
    Y_pres += [pre]
Y_pre = np.mean(Y_pres, axis=0)
Y_ori = bmodel.inverse(Y_train.to_numpy())
percentage = np.divide(Y_ori, Y_pre)

# Y_pre = model.predict_inverse(X_train)
# Y_ori = model.inverse(Y_train.to_numpy())
# percentage = np.divide(Y_ori, Y_final)
# discount=np.subtract(1,percentage)
# print(X_train.head(1))
# print('y_pre',Y_pre.shape)
# print('y_truth',Y_ori)
# print(percentage)
# print(discount.shape)
