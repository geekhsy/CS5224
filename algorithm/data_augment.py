import os

import numpy as np
import pandas as pd

from constant import ORIGINAL_DATA_DIC


def data_augment_csv():
    # load csv file
    train_path, build_path = os.path.join(ORIGINAL_DATA_DIC, 'train.csv'), os.path.join(ORIGINAL_DATA_DIC,
                                                                                        'extra_data.csv')
    train_df, build_df = pd.read_csv(train_path), pd.read_csv(build_path)
    extra_train_df = build_df[~np.isnan(build_df['price'])]
    extra_train_df.to_csv(os.path.join(ORIGINAL_DATA_DIC, 'extra_train.csv'))
    augment_train_df = pd.concat([train_df, extra_train_df])
    augment_train_df.to_csv(os.path.join(ORIGINAL_DATA_DIC, 'aug_train.csv'))


def data_augment_npy():
    for col in ['accessories', 'features', 'description']:
        ori_data, extra_data = np.load(f'./bert_feature/{col}_train.npy'), np.load(
            f'./bert_feature/{col}_extra_train.npy')
        aug_data = np.concatenate([ori_data, extra_data], axis=0)
        np.save(f'./bert_feature/{col}_aug_train.npy', aug_data)


if __name__ == '__main__':
    # data_augment_csv()
    data_augment_npy()
