import warnings

import matplotlib.pyplot as plt
import seaborn as sns

from constant import TEXT_FEA_DIC, ORIGINAL_DATA_DIC, TRAIN_FILE, TEST_FILE, NUMERICAL_COLUMN
from preprocessing import load_data

warnings.filterwarnings("ignore")
fig_size_factor = 4
K = 2


def find_best_subplot_size(total: int) -> (int, int):
    col = int(total ** 0.5)
    row = col + 1
    if row * col < total:
        col += 1
    return row, col


if __name__ == '__main__':
    sns.set()
    # load original_data
    X_train, X_holdout, X_test, Y_train, Y_holdout, price_encoder = load_data(ORIGINAL_DATA_DIC, TRAIN_FILE, TEST_FILE,
                                                                              TEXT_FEA_DIC)

    print('-' * 50)
    print('Plotting')

    # target distribution plot
    sns.distplot(Y_train)
    plt.show()

    # feature distribution plot
    row, col = find_best_subplot_size(len(NUMERICAL_COLUMN))
    fig, ax = plt.subplots(row, col, figsize=(row * fig_size_factor, col * fig_size_factor), dpi=200)
    for i in range(len(NUMERICAL_COLUMN)):
        sns.distplot(X_test[NUMERICAL_COLUMN[i]], ax=ax[i // col][i % col])
    plt.show()

    # correlation heatmap
    sns.heatmap(X_test[NUMERICAL_COLUMN].corr())
    plt.show()

    # PCA
    sns.scatterplot(x='pca_fea_0', y='pca_fea_1', hue='k_means_fea', data=X_train)
    plt.show()

    # tsne
    sns.scatterplot(x='tsne_fea_0', y='tsne_fea_1', hue='k_means_fea', data=X_train)
    plt.show()