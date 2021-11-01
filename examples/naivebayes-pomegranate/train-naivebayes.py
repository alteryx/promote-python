import numpy as np

from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from pomegranate import NaiveBayes, NormalDistribution

n, d, m = 50000, 5, 10
X, y = make_blobs(n, d, m, cluster_std=10)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

n_unlabeled = int(X_train.shape[0] * 0.999)
idxs = np.random.choice(X_train.shape[0], size=n_unlabeled)
y_train[idxs] = -1

model = NaiveBayes.from_samples(NormalDistribution, X_train, y_train, verbose=True)

import json
with open('objects/naive_weights.pomo', 'w') as outfile:
    json.dump(model.to_json(), outfile)
