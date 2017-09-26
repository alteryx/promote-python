from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier

# Loading some example data
iris = datasets.load_iris()
X = iris.data[:, [0,2]]
y = iris.target

clf1 = DecisionTreeClassifier(max_depth=4)
clf1 = clf1.fit(X,y)
# save our trained model to a pickle file so we can use it later
from sklearn.externals import joblib
joblib.dump(clf1, './objects/decision_tree.pkl')
