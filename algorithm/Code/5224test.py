import warnings
import sys
import json

from base_model import BaseModel
from constant import LOAD_MODEL_NAME,CATEGORY_COLUMN
from preprocessing import generate_preprocessed, load_data,generate_preprocessed_testdata
from util import write_to_csv, save_data_to_disk, load_data_from_disk, get_data_model, \
    ultimate_train_predict, ultimate_loaded_model_predict, get_final_y_predict,construct_df

import numpy as np
import pandas as pd


warnings.filterwarnings("ignore")

def predict(x_str):
    # print("_____________________________")
    # print("x_str",x_str)
    # x_str = sys.argv[1]
    # print(x_str)
    x_ori = json.loads(x_str)
    # print("x_ori",x_ori)
    # print('x',x_ori)
    x_ori = pd.DataFrame([x_ori])
    # print(x_ori)
    xt = pd.read_csv("test.csv", low_memory=False)
    xt = xt.drop(labels=range(0,500),axis=0)
    x_df = pd.concat([x_ori,xt])
    # print(x_df.dtypes)
    xt_df = pd.read_csv("train.csv")
    # print(xt_df)
    x_test = generate_preprocessed(xt_df,x_df)
    # x_test = generate_preprocessed_testdata(x_df)
    # print('Loading models')
    loaded_model = load_data_from_disk(LOAD_MODEL_NAME)
    # print('-' * 50)
    # print('Predicting')
    Y_pre = []
    cat_col = CATEGORY_COLUMN + ['k_means_fea']
    i=1
    for model, x in loaded_model:
        if i<3:
            x_test[cat_col] = x_test[cat_col].astype('category')
        else:
            x_test[cat_col] = x_test[cat_col].astype(str)
        Y_predict = construct_df(model, x_test)
        # print('Y_predict',Y_predict)
        Y_pre += [Y_predict]
        # print('Y_pre',Y_pre)
        i+=1
    Y_final = get_final_y_predict(Y_pre)
    # print(Y_final['Predicted'][0])
    return Y_final['Predicted'][0]

if __name__ == '__main__':
    # print('output: ',sys.argv[1])
    price = predict(sys.argv[1])
    print(price)
    # sys.exit(price)





