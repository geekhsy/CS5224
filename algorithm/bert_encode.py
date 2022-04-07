import os

import numpy as np
import pandas as pd
from bert_serving.client import BertClient

TEXT_COLUMN = ['accessories', 'features', 'description']
BATCH_SIZE = 256
FEATURE_DIC = './bert_feature'


def get_text_data(df: pd.DataFrame) -> pd.DataFrame:
    text_df = df[TEXT_COLUMN]
    for col in TEXT_COLUMN:
        text_df[col].fillna('Empty', inplace=True)
        text_df[col] = text_df[col].str.lower()
    return text_df


def encode(text_df: pd.DataFrame, suffix: str):
    bc = BertClient()
    print('Server connected')
    if not os.path.exists(FEATURE_DIC):
        os.mkdir(FEATURE_DIC)

    for col in TEXT_COLUMN:
        text_list = text_df[col].tolist()
        output_file = os.path.join(FEATURE_DIC, f'{col}_{suffix}.npy')

        if os.path.exists(output_file):
            old_data = smart_batch_processing(bc, text_list, output_file, np.load(output_file))
        else:
            old_data = smart_batch_processing(bc, text_list, output_file, None)
        while len(old_data) < len(text_list):
            old_data = smart_batch_processing(bc, text_list, output_file, old_data)
            print(
                f'{suffix}_{col}: {len(old_data) / len(text_list) * 100}% ({len(old_data)}/{len(text_list)})')


def smart_batch_processing(bc, text_list, save_path, old_data=None):
    if old_data is None:
        new_data = bc.encode(text_list[:BATCH_SIZE])
        np.save(save_path, new_data)
        return new_data

    new_data = bc.encode(text_list[len(old_data):min(len(old_data) + BATCH_SIZE, len(text_list))])
    cat_data = np.concatenate([old_data, new_data], axis=0)
    np.save(save_path, cat_data)
    return cat_data


if __name__ == '__main__':
    train_df, test_df, build_df = pd.read_csv('original_data/train.csv'), pd.read_csv(
        'original_data/test.csv'), pd.read_csv('original_data/extra_train.csv')
    train_text, test_text, build_text = get_text_data(train_df), get_text_data(test_df), get_text_data(build_df)
    # encode(train_text, 'train')
    # encode(test_text, 'test')
    encode(build_text, 'extra_train')
