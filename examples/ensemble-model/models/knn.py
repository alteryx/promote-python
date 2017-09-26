from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier

iris = datasets.load_iris()
X = iris.data[:, [0,2]]
y = iris.target

clf2 = KNeighborsClassifier(n_neighbors=7)
clf2 = clf2.fit(X,y)

from sklearn.externals import joblib
joblib.dump(clf2, './objects/knn.pkl')
