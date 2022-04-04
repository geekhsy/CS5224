import GPUtil
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

GENERATE_CSV = False

LOAD_MODEL = True
LOAD_MODEL_NAME = '2022_03_11_11_49_57'

ORIGINAL_DATA_DIC = './original_data'
PROCESSED_DATA_DIC = './processed_data'
TEXT_FEA_DIC = './bert_feature'
PREDICT_DIC = './result'
MODEL_DIC = './models'
TRAIN_FILE = 'train'
TEST_FILE = 'test'

# ['lightgbm', 'xgboost', 'catboost', 'all']
TREE_MODEL = 'all'

FOLD = 5
RNG = 666
GENERAL_K = 2
TEXT_K = 3

NUM_CLUSTER = 5

# 'curb_weight', 'power', 'engine_cap', 'no_of_owners', 'depreciation', 'coe', 'road_tax', 'dereg_value', 'mileage',
# 'omv', 'arf','manufactured','reg_date'
NUMERICAL_COLUMN = ['listing_id', 'curb_weight', 'power', 'engine_cap', 'no_of_owners', 'depreciation',
                    'dereg_value', 'mileage', 'omv', 'arf', 'coe', 'road_tax',
                    'manufactured', 'reg_date'
                    ]

# 'manufactured', 'type_of_vehicle', 'category', 'transmission', 'make', 'model'
CATEGORY_COLUMN = ['type_of_vehicle', 'category', 'transmission', 'make', 'model']

#  ['accessories', 'features', 'description']
TEXT_COLUMN = ['accessories', 'features', 'description']
TEXT_FEA_LEN = 768  # fixed by bert

NUMERICAL_ENCODER = None
TEXT_ENCODER = Pipeline([
    ('pca', PCA(n_components=TEXT_K)),
    # ('tsne', TSNETransformer(n_components=TEXT_K)),
    ('std', StandardScaler())])
PRICE_ENCODER = None

XGBoost_params = {
    'alpha': 0.000538319498258817,
    'booster': 'dart',
    'colsample_bytree': 0.9251107243369172,
    'eta': 0.6108881820393085,
    'gamma': 0.004577530010195187,
    'grow_policy': 'depthwise',
    'lambda': 0.00288923187762921,
    'max_depth': 9,
    'min_child_weight': 8,
    'normalize_type': 'forest',
    'rate_drop': 0.2747606521769868,
    'sample_type': 'uniform',
    'skip_drop': 1.0634192915731993e-06,
    'subsample': 0.9320275898168436,
    # 'bagging_fraction': 0.9717921789613708,
    # 'bagging_freq': 1,
    # 'colsample_bytree': 0.8,
    # 'feature_fraction': 0.9866294267334812,
    # 'lambda_l1': 0.6250673671796301,
    # 'lambda_l2': 0.6104808356217407,
    # 'max_depth': 5,
    # 'num_leaves': 23,
    # 'subsample': 1.0,
    'early_stopping_rounds': 20,
    # 'learning_rate': 0.09728421673734854,
    'eval_metric': "rmse",
    'num_boost_round': 1000,
    # 'boosting_type': 'gbdt',
    # 'enable_categorical':True,
}

LightGBM_params = {
    'n_estimators': 1000,
    'bagging_fraction': 0.8184368927635437,
    'bagging_freq': 2,
    'colsample_bytree': 0.9,
    'feature_fraction': 0.946290269136161,
    'lambda_l1': 5.8556814218284175e-08,
    'lambda_l2': 1.588639761237067e-05,
    'max_depth': 5,
    'num_leaves': 30,
    'subsample': 0.8,
    'early_stopping_rounds': 20,
    'learning_rate': 0.1,
    'metric': "rmse",
    'boosting_type': 'gbdt',
}

CatBoost_params = {
    'loss_function': 'RMSE',
    'eval_metric': 'RMSE',
    'iterations': 1000,
    # 'learning_rate': 0.03,
    # 'bagging_temperature': 0.2,
    'od_type': 'Iter',
    'od_wait': 20,
    'depth': 9,
    'boosting_type': 'Ordered',
    'bootstrap_type': 'MVS',
    'colsample_bylevel': 0.0955740495101605,
}

if GPUtil.getAvailable():
    XGBoost_params['tree_method'] = 'gpu_hist'
    CatBoost_params['task_type'] = 'GPU'
    LightGBM_params['device'] = 'gpu'
