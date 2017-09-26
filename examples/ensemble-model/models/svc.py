from sklearn import datasets
from sklearn.svm import SVC

iris = datasets.load_iris()
X = iris.data[:, [0,2]]
y = iris.target

clf3 = SVC(kernel='rbf', probability=True)
clf3 = clf3.fit(X,y)

from sklearn.externals import joblib
joblib.dump(clf3, './objects/svc.pkl')
