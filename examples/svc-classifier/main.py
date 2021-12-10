import os
import sys
import promote
import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.datasets import load_iris

def irisClassifier(data):
    prediction = clf.predict(pd.DataFrame(data))
    species = ['setosa', 'versicolor', 'virginica']
    result = [species[i] for i in prediction]
    return result

iris = load_iris()
clf = SVC()
X = pd.DataFrame(iris.data, columns=iris.feature_names)
y = pd.DataFrame(iris.target, columns=["flower_types"])
clf.fit(X, y["flower_types"])

TESTDATA = pd.DataFrame(iris.data[:1])
print("Data to test:", TESTDATA.to_json())
print("Local Prediction: ", irisClassifier(TESTDATA))

USERNAME = "USERNAME"
API_KEY = "APIKEY"
PROMOTE_URL = "https://promote.c.yhat.com/"

p = promote.Promote(USERNAME, API_KEY, PROMOTE_URL)
# add metadata
p.metadata['intercept'] = list(np.around(clf.intercept_,3))
p.metadata['n_support'] = [int(n) for n in list(clf.n_support_)]

if 'ipy' not in os.path.realpath(sys.argv[0]):
    p.deploy("IrisSVC", irisClassifier, TESTDATA, confirm=False)
