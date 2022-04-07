import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

NUM_SAMPLE = 50
GLOBAL_SIGMA = 500
data = [('Naive', 'LightGBM', 38000, 300), ('Naive', 'XGBoost', 39000, 300), ('Naive', 'CatBoost', 37000, 200),
        ('Box cox transformation', 'LightGBM', 34000, 200), ('Box cox transformation', 'XGBoost', 35000, 200),
        ('Box cox transformation', 'CatBoost', 33000, 200),
        ('Standardization', 'LightGBM', 32000, 200), ('Standardization', 'XGBoost', 33000, 200),
        ('Standardization', 'CatBoost', 31000, 200),
        ('Generated feature', 'LightGBM', 30000, 200), ('Generated feature', 'XGBoost', 31000, 200),
        ('Generated feature', 'CatBoost', 29500, 200),
        ('KFold training', 'LightGBM', 28000, 300), ('KFold training', 'XGBoost', 29000, 300),
        ('KFold training', 'CatBoost', 28000, 200),
        ('Retraining', 'LightGBM', 26000, 300), ('Retraining', 'XGBoost', 26500, 300),
        ('Retraining', 'CatBoost', 25500, 200),
        ('Ensemble', '(LightGBM + XGBoost + CatBoost)', 23000, 200),
        ]

if __name__ == '__main__':
    sns.set()
    methods, models, rmse = [], [], []
    for method, model, mu, sigma in data:
        methods += [method] * NUM_SAMPLE
        models += [model] * NUM_SAMPLE
        rmse += np.random.normal(mu, GLOBAL_SIGMA, NUM_SAMPLE).tolist()
    source_dic = {
        'method': methods,
        'model': models,
        'rmse': rmse
    }
    source_df = pd.DataFrame(source_dic)
    sns.boxplot(data=source_df,
                x='method',
                y='rmse',
                hue='model')
    plt.show()
