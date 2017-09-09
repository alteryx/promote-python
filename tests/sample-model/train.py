from sklearn import svm
from sklearn import datasets
clf = svm.SVC()
iris = datasets.load_iris()
X, y = iris.data, iris.target
clf.fit(X, y)  

from sklearn.externals import joblib
joblib.dump(clf, './pickles/model_weights.pkl')


class foo:
    def hi():
        pass

        