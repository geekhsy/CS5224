import os
from functools import lru_cache

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, StandardScaler

from constant import NUMERICAL_COLUMN, CATEGORY_COLUMN, TEXT_COLUMN, TEXT_FEA_LEN, \
    NUMERICAL_ENCODER, TEXT_ENCODER, RNG, GENERAL_K, TEXT_K, PROCESSED_DATA_DIC, PRICE_ENCODER, NUM_CLUSTER
from transformerss import TSNETransformer


def load_text_data(text_path: str, dataset: str) -> pd.DataFrame:
    if not TEXT_COLUMN:
        return None

    text_feature = []
    for col_name in TEXT_COLUMN:
        filePath = os.path.join(text_path, f'{col_name}_{dataset}.npy')
        data = np.load(filePath)
        text_feature += [pd.DataFrame(data, columns=[f'{col_name}_{i}' for i in range(TEXT_FEA_LEN)])]
    text_feature = pd.concat(text_feature, axis=1)
    return text_feature

def load_text_testdata(data) -> pd.DataFrame:
    if not TEXT_COLUMN:
        return None

    text_feature = []
    for col_name in TEXT_COLUMN:
        text_feature += [pd.DataFrame(data, columns=[f'{col_name}_{i}' for i in range(TEXT_FEA_LEN)])]
    text_feature = pd.concat(text_feature, axis=1)
    return text_feature

@lru_cache
def load_data(data_path: str, train_file: str, test_file: str, text_feature_path: str) -> (
        pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, object):
    print('-' * 50)
    if need_to_generate_data():
        print('Preprocessing data')
        X_train, X_holdout, X_test, Y_train, Y_holdout, price_encoder = generate_preprocessed_data(data_path,
                                                                                                   train_file,
                                                                                                   test_file,
                                                                                                   text_feature_path)
        print('-' * 50)
        print('Dumping processed data')
        dump_preprocessed_data(X_train, X_holdout, X_test, Y_train, Y_holdout, price_encoder)
    else:
        print('Loading processed data')
        X_train, X_holdout, X_test, Y_train, Y_holdout, price_encoder = load_processed_data()
    return X_train, X_holdout, X_test, Y_train, Y_holdout, price_encoder


def generate_preprocessed_data(data_path: str, train_file: str, test_file: str, text_feature_path: str) -> (
        pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):
    # load text features
    train_text_feature, test_text_feature = load_text_data(text_feature_path, train_file), load_text_data(
        text_feature_path, test_file)

    # load csv file
    train_path, test_path = os.path.join(data_path, f'{train_file}.csv'), os.path.join(data_path, f'{test_file}.csv')
    train_df, test_df = pd.read_csv(train_path), pd.read_csv(test_path)

    # get price
    price = train_df['price']
    Y_df = pd.DataFrame({'price': price})

    # date time
    train_manufacture_year = train_df['manufactured'].fillna(method='ffill').astype(int)
    train_manufacture_year[train_manufacture_year > 2021] = 2021
    train_df['manufactured'] = (pd.to_datetime(train_manufacture_year, format='%Y').astype('int64') // 10 ** 9).astype(
        'float64')

    test_manufacture_year = test_df['manufactured'].fillna(method='ffill').astype(int)
    test_manufacture_year[test_manufacture_year > 2022] = 2022
    test_df['manufactured'] = (pd.to_datetime(test_manufacture_year, format='%Y').astype('int64') // 10 ** 9).astype(
        'float64')

    manufactured_shift = abs(min(min(train_df['manufactured']), min(test_df['manufactured'])))
    train_df['manufactured'] += manufactured_shift
    test_df['manufactured'] += manufactured_shift

    train_df['reg_date'] = (
            pd.to_datetime(train_df['reg_date'].fillna(method='ffill')).astype('int64') // 10 ** 9).astype(
        'float64')
    test_df['reg_date'] = (
            pd.to_datetime(test_df['reg_date'].fillna(method='ffill')).astype('int64') // 10 ** 9).astype('float64')

    reg_date_shift = abs(min(min(train_df['reg_date']), min(test_df['reg_date'])))
    train_df['reg_date'] += reg_date_shift
    test_df['reg_date'] += reg_date_shift

    # concat text feature
    if train_text_feature is not None:
        train_df = pd.concat([train_df, train_text_feature], axis=1)
    if test_text_feature is not None:
        test_df = pd.concat([test_df, test_text_feature], axis=1)

    augmented_text_column = []
    for col in TEXT_COLUMN:
        augmented_text_column += [f'{col}_{i}' for i in range(TEXT_FEA_LEN)]
    k_best_text_col = []
    for col in TEXT_COLUMN:
        k_best_text_col += [f'{col}_{i}' for i in range(TEXT_K)]

    # abandon redundant col
    train_df = train_df[augmented_text_column + NUMERICAL_COLUMN + CATEGORY_COLUMN]
    X_test = test_df[augmented_text_column + NUMERICAL_COLUMN + CATEGORY_COLUMN]

    # make all words lower
    for cat_col in CATEGORY_COLUMN:
        train_df[cat_col] = train_df[cat_col].astype(str).str.lower()

    # create numerical and categorical pipeline
    text_pip = [('imputer', SimpleImputer(strategy='mean'))]
    if TEXT_ENCODER:
        text_pip += [('enc', TEXT_ENCODER)]

    num_pip = [('imputer', SimpleImputer(strategy='mean'))]
    if NUMERICAL_ENCODER:
        num_pip += [('enc', NUMERICAL_ENCODER)]

    cat_pip = [('imputer', SimpleImputer(strategy='most_frequent')),
               ('enc', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1))]

    text_encoders = [Pipeline(text_pip) for _ in range(len(TEXT_COLUMN))]
    num_encoder = Pipeline(num_pip)
    cat_encoder = Pipeline(cat_pip)

    # create preprocessing pipeline
    transformers = [
        ('num', num_encoder, NUMERICAL_COLUMN),
        ('cat', cat_encoder, CATEGORY_COLUMN),
    ]
    for i in range(len(text_encoders)):
        transformers += [(TEXT_COLUMN[i], text_encoders[i], [f'{TEXT_COLUMN[i]}_{j}' for j in range(TEXT_FEA_LEN)])]

    preprocessing = ColumnTransformer(transformers=transformers)

    new_col = NUMERICAL_COLUMN + CATEGORY_COLUMN + k_best_text_col
    train_df = pd.DataFrame(preprocessing.fit_transform(train_df, Y_df), columns=new_col)
    X_test = pd.DataFrame(preprocessing.transform(X_test), columns=new_col)

    # k-means
    km = KMeans(NUM_CLUSTER)
    train_df['k_means_fea'] = km.fit_predict(train_df)
    X_test['k_means_fea'] = km.predict(X_test)

    # PCA
    pca = Pipeline([
        ('pca', PCA(n_components=GENERAL_K)),
        ('std', StandardScaler()),
    ])
    train_df[[f'pca_fea_{i}' for i in range(GENERAL_K)]] = pca.fit_transform(train_df)
    X_test[[f'pca_fea_{i}' for i in range(GENERAL_K)]] = pca.fit_transform(X_test)

    # tsne
    tsne = Pipeline([
        ('tsne', TSNETransformer(n_components=GENERAL_K)),
        ('std', StandardScaler()),
    ])
    train_df[[f'tsne_fea_{i}' for i in range(GENERAL_K)]] = tsne.fit_transform(train_df)
    X_test[[f'tsne_fea_{i}' for i in range(GENERAL_K)]] = tsne.fit_transform(X_test)

    X_train, X_holdout, Y_train, Y_holdout = train_test_split(train_df, Y_df, test_size=0.1, shuffle=True,
                                                              random_state=RNG)

    if PRICE_ENCODER is not None:
        Y_train['price'] = PRICE_ENCODER.fit_transform(np.array(Y_train['price']).reshape(-1, 1))
        Y_holdout['price'] = PRICE_ENCODER.transform(np.array(Y_holdout['price']).reshape(-1, 1))

    return X_train, X_holdout, X_test, Y_train, Y_holdout, PRICE_ENCODER


def dump_preprocessed_data(X_train: pd.DataFrame, X_holdout: pd.DataFrame, X_test: pd.DataFrame, Y_train: pd.DataFrame,
                           Y_holdout: pd.DataFrame, price_encoder):
    if not os.path.exists(PROCESSED_DATA_DIC):
        os.mkdir(PROCESSED_DATA_DIC)

    hyper_param = get_preprocessing_hyper_parameters()
    joblib.dump(hyper_param, os.path.join(PROCESSED_DATA_DIC, 'hyper_param.pkl'))
    joblib.dump(X_train, os.path.join(PROCESSED_DATA_DIC, 'X_train.pkl'))
    joblib.dump(X_holdout, os.path.join(PROCESSED_DATA_DIC, 'X_holdout.pkl'))
    joblib.dump(X_test, os.path.join(PROCESSED_DATA_DIC, 'X_test.pkl'))
    joblib.dump(Y_train, os.path.join(PROCESSED_DATA_DIC, 'Y_train.pkl'))
    joblib.dump(Y_holdout, os.path.join(PROCESSED_DATA_DIC, 'Y_holdout.pkl'))
    joblib.dump(price_encoder, os.path.join(PROCESSED_DATA_DIC, 'price_encoder.pkl'))


def load_processed_data():
    X_train = joblib.load(os.path.join(PROCESSED_DATA_DIC, 'X_train.pkl'))
    X_holdout = joblib.load(os.path.join(PROCESSED_DATA_DIC, 'X_holdout.pkl'))
    X_test = joblib.load(os.path.join(PROCESSED_DATA_DIC, 'X_test.pkl'))
    Y_train = joblib.load(os.path.join(PROCESSED_DATA_DIC, 'Y_train.pkl'))
    Y_holdout = joblib.load(os.path.join(PROCESSED_DATA_DIC, 'Y_holdout.pkl'))
    price_encoder = joblib.load(os.path.join(PROCESSED_DATA_DIC, 'price_encoder.pkl'))

    return X_train, X_holdout, X_test, Y_train, Y_holdout, price_encoder


def get_preprocessing_hyper_parameters() -> tuple:
    hyper_param = tuple([NUMERICAL_COLUMN, CATEGORY_COLUMN, TEXT_COLUMN,
                         tuple(NUMERICAL_ENCODER.named_steps.keys()) if NUMERICAL_ENCODER else None,
                         tuple(TEXT_ENCODER.named_steps.keys()) if TEXT_ENCODER else None,
                         tuple(PRICE_ENCODER.named_steps.keys()) if PRICE_ENCODER else None,
                         RNG, GENERAL_K, TEXT_K, NUM_CLUSTER])
    return hyper_param


def need_to_generate_data() -> bool:
    if not os.path.exists(os.path.join(PROCESSED_DATA_DIC, 'hyper_param.pkl')):
        return True
    saved_hyper_param = joblib.load(os.path.join(PROCESSED_DATA_DIC, 'hyper_param.pkl'))
    current_hyper_param = get_preprocessing_hyper_parameters()
    return saved_hyper_param != current_hyper_param


def generate_preprocessed_testdata(test_df) -> pd.DataFrame:
    # # load text features
    # test_text_feature = load_text_testdata(test_df)
    test_text_feature = load_text_data('./bert_feature', 'test')

    # # load csv file
    # train_path, test_path = os.path.join(data_path, f'{train_file}.csv'), os.path.join(data_path, f'{test_file}.csv')
    # train_df, test_df = pd.read_csv(train_path), pd.read_csv(test_path)

    # # get price
    # price = train_df['price']
    # Y_df = pd.DataFrame({'price': price})

    # date time
    # train_manufacture_year = train_df['manufactured'].astype(int)
    # train_manufacture_year[train_manufacture_year > 2021] = 2021
    # train_df['manufactured'] = (pd.to_datetime(train_manufacture_year, format='%Y').astype('int64') // 10 ** 9).astype(
    #     'float64')

    test_manufacture_year = test_df['manufactured'].fillna(method='ffill').astype(int)
    test_manufacture_year[test_manufacture_year > 2022] = 2022
    test_df['manufactured'] = (pd.to_datetime(test_manufacture_year, format='%Y').astype('int64') // 10 ** 9).astype(
        'float64')

    manufactured_shift = abs(min(test_df['manufactured']))
    test_df['manufactured'] += manufactured_shift

    # train_df['reg_date'] = (
    #         pd.to_datetime(train_df['reg_date'].fillna(method='ffill')).astype('int64') // 10 ** 9).astype(
    #     'float64')
    test_df['reg_date'] = (pd.to_datetime(test_df['reg_date'].fillna(method='ffill')).astype('int64') // 10 ** 9).astype(
        'float64')

    reg_date_shift = abs(min(test_df['reg_date']))
    # train_df['reg_date'] += reg_date_shift
    test_df['reg_date'] += reg_date_shift

    # concat text feature
    # if train_text_feature is not None:
    #     train_df = pd.concat([train_df, train_text_feature], axis=1)
    if test_text_feature is not None:
        test_df = pd.concat([test_df, test_text_feature], axis=1)

    augmented_text_column = []
    for col in TEXT_COLUMN:
        augmented_text_column += [f'{col}_{i}' for i in range(TEXT_FEA_LEN)]
    k_best_text_col = []
    for col in TEXT_COLUMN:
        k_best_text_col += [f'{col}_{i}' for i in range(TEXT_K)]

    # abandon redundant col
    # train_df = train_df[augmented_text_column + NUMERICAL_COLUMN + CATEGORY_COLUMN]
    X_test = test_df[augmented_text_column + NUMERICAL_COLUMN + CATEGORY_COLUMN]

    # make all words lower
    # for cat_col in CATEGORY_COLUMN:
    #     train_df[cat_col] = train_df[cat_col].astype(str).str.lower()

    # create numerical and categorical pipeline
    text_pip = [('imputer', SimpleImputer(strategy='mean'))]
    if TEXT_ENCODER:
        text_pip += [('enc', TEXT_ENCODER)]

    num_pip = [('imputer', SimpleImputer(strategy='mean'))]
    if NUMERICAL_ENCODER:
        num_pip += [('enc', NUMERICAL_ENCODER)]

    cat_pip = [('imputer', SimpleImputer(strategy='most_frequent')),
               ('enc', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1))]

    text_encoders = [Pipeline(text_pip) for _ in range(len(TEXT_COLUMN))]
    num_encoder = Pipeline(num_pip)
    cat_encoder = Pipeline(cat_pip)

    # create preprocessing pipeline
    transformers = [
        ('num', num_encoder, NUMERICAL_COLUMN),
        ('cat', cat_encoder, CATEGORY_COLUMN),
    ]
    for i in range(len(text_encoders)):
        transformers += [(TEXT_COLUMN[i], text_encoders[i], [f'{TEXT_COLUMN[i]}_{j}' for j in range(TEXT_FEA_LEN)])]

    preprocessing = ColumnTransformer(transformers=transformers)

    new_col = NUMERICAL_COLUMN + CATEGORY_COLUMN + k_best_text_col
    # print(new_col)
    # train_df = pd.DataFrame(preprocessing.fit_transform(train_df, Y_df), columns=new_col)
    print(X_test)
    X_test = pd.DataFrame(preprocessing.fit_transform(X_test), columns=new_col)

    # k-means
    km = KMeans(NUM_CLUSTER)
    # train_df['k_means_fea'] = km.fit_predict(train_df)
    X_test['k_means_fea'] = km.fit_predict(X_test)

    # PCA
    pca = Pipeline([
        ('pca', PCA(n_components=GENERAL_K)),
        ('std', StandardScaler()),
    ])
    # train_df[[f'pca_fea_{i}' for i in range(GENERAL_K)]] = pca.fit_transform(train_df)
    X_test[[f'pca_fea_{i}' for i in range(GENERAL_K)]] = pca.fit_transform(X_test)

    # tsne
    tsne = Pipeline([
        ('tsne', TSNETransformer(n_components=GENERAL_K)),
        ('std', StandardScaler()),
    ])
    # train_df[[f'tsne_fea_{i}' for i in range(GENERAL_K)]] = tsne.fit_transform(train_df)
    X_test[[f'tsne_fea_{i}' for i in range(GENERAL_K)]] = tsne.fit_transform(X_test)

    # X_train, X_holdout, Y_train, Y_holdout = train_test_split(train_df, Y_df, test_size=0.1, shuffle=True,
    #                                                           random_state=RNG)

    # if PRICE_ENCODER is not None:
    #     Y_train['price'] = PRICE_ENCODER.fit_transform(np.array(Y_train['price']).reshape(-1, 1))
    #     Y_holdout['price'] = PRICE_ENCODER.transform(np.array(Y_holdout['price']).reshape(-1, 1))

    return X_test

def generate_preprocessed(train_df,test_df) -> pd.DataFrame:
    # load text features
    train_text_feature = load_text_data('./bert_feature', 'train')
    test_text_feature = load_text_testdata(test_df)
    # test_text_feature = load_text_data('./bert_feature', 'test')

    # get price
    price = train_df['price']
    Y_df = pd.DataFrame({'price': price})

    # date time
    train_manufacture_year = train_df['manufactured'].fillna(method='ffill').astype(int)
    train_manufacture_year[train_manufacture_year > 2021] = 2021
    train_df['manufactured'] = (pd.to_datetime(train_manufacture_year, format='%Y').astype('int64') // 10 ** 9).astype(
        'float64')

    test_manufacture_year = test_df['manufactured'].fillna(method='ffill').astype(int)
    test_manufacture_year[test_manufacture_year > 2022] = 2022
    test_df['manufactured'] = (pd.to_datetime(test_manufacture_year, format='%Y').astype('int64') // 10 ** 9).astype(
        'float64')

    manufactured_shift = abs(min(min(train_df['manufactured']), min(test_df['manufactured'])))
    train_df['manufactured'] += manufactured_shift
    test_df['manufactured'] += manufactured_shift

    train_df['reg_date'] = (
            pd.to_datetime(train_df['reg_date'].fillna(method='ffill')).astype('int64') // 10 ** 9).astype(
        'float64')
    test_df['reg_date'] = (
            pd.to_datetime(test_df['reg_date'].fillna(method='ffill')).astype('int64') // 10 ** 9).astype('float64')

    reg_date_shift = abs(min(min(train_df['reg_date']), min(test_df['reg_date'])))
    train_df['reg_date'] += reg_date_shift
    test_df['reg_date'] += reg_date_shift

    # print("train",train_df.dtypes)
    # print("test",test_df.dtypes)

    # concat text feature
    if train_text_feature is not None:
        train_df = pd.concat([train_df, train_text_feature], axis=1)
    if test_text_feature is not None:
        test_df = pd.concat([test_df, test_text_feature], axis=1)
    
    # print("train",train_df.dtypes)
    # print("test",test_df.dtypes)

    augmented_text_column = []
    for col in TEXT_COLUMN:
        augmented_text_column += [f'{col}_{i}' for i in range(TEXT_FEA_LEN)]
    k_best_text_col = []
    for col in TEXT_COLUMN:
        k_best_text_col += [f'{col}_{i}' for i in range(TEXT_K)]

    # abandon redundant col
    train_df = train_df[augmented_text_column + NUMERICAL_COLUMN + CATEGORY_COLUMN]
    X_test = test_df[augmented_text_column + NUMERICAL_COLUMN + CATEGORY_COLUMN]
    
    # make all words lower
    for cat_col in CATEGORY_COLUMN:
        train_df[cat_col] = train_df[cat_col].astype(str).str.lower()

    # create numerical and categorical pipeline
    text_pip = [('imputer', SimpleImputer(strategy='mean'))]
    if TEXT_ENCODER:
        text_pip += [('enc', TEXT_ENCODER)]

    num_pip = [('imputer', SimpleImputer(strategy='mean'))]
    if NUMERICAL_ENCODER:
        num_pip += [('enc', NUMERICAL_ENCODER)]

    cat_pip = [('imputer', SimpleImputer(strategy='most_frequent')),
               ('enc', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1))]

    text_encoders = [Pipeline(text_pip) for _ in range(len(TEXT_COLUMN))]
    num_encoder = Pipeline(num_pip)
    cat_encoder = Pipeline(cat_pip)

    # create preprocessing pipeline
    transformers = [
        ('num', num_encoder, NUMERICAL_COLUMN),
        ('cat', cat_encoder, CATEGORY_COLUMN),
    ]
    for i in range(len(text_encoders)):
        transformers += [(TEXT_COLUMN[i], text_encoders[i], [f'{TEXT_COLUMN[i]}_{j}' for j in range(TEXT_FEA_LEN)])]

    preprocessing = ColumnTransformer(transformers=transformers)

    new_col = NUMERICAL_COLUMN + CATEGORY_COLUMN + k_best_text_col
    # print(train_df.dtypes)
    # print('test',test_df.dtypes)
    train_df = pd.DataFrame(preprocessing.fit_transform(train_df, Y_df), columns=new_col)
    # print(X_test)
    X_test = pd.DataFrame(preprocessing.transform(X_test), columns=new_col)

    # k-means
    km = KMeans(NUM_CLUSTER)
    train_df['k_means_fea'] = km.fit_predict(train_df)
    X_test['k_means_fea'] = km.predict(X_test)

    # PCA
    pca = Pipeline([
        ('pca', PCA(n_components=GENERAL_K)),
        ('std', StandardScaler()),
    ])
    # train_df[[f'pca_fea_{i}' for i in range(GENERAL_K)]] = pca.fit_transform(train_df)
    X_test[[f'pca_fea_{i}' for i in range(GENERAL_K)]] = pca.fit_transform(X_test)

    # tsne
    tsne = Pipeline([
        ('tsne', TSNETransformer(n_components=GENERAL_K)),
        ('std', StandardScaler()),
    ])
    # train_df[[f'tsne_fea_{i}' for i in range(GENERAL_K)]] = tsne.fit_transform(train_df)
    X_test[[f'tsne_fea_{i}' for i in range(GENERAL_K)]] = tsne.fit_transform(X_test)

    # X_train, X_holdout, Y_train, Y_holdout = train_test_split(train_df, Y_df, test_size=0.1, shuffle=True,
    #                                                           random_state=RNG)

    # if PRICE_ENCODER is not None:
    #     Y_train['price'] = PRICE_ENCODER.fit_transform(np.array(Y_train['price']).reshape(-1, 1))
    #     Y_holdout['price'] = PRICE_ENCODER.transform(np.array(Y_holdout['price']).reshape(-1, 1))

    return X_test
