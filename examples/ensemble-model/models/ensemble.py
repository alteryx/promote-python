import joblib
from sklearn import datasets
from sklearn.ensemble import VotingClassifier

model1 = joblib.load('./objects/decision_tree.pkl')
model2 = joblib.load('./objects/knn.pkl')
model3 = joblib.load('./objects/svc.pkl')

iris = datasets.load_iris()
X = iris.data[:, [0,2]]
y = iris.target

# Training classifiers
eclf = VotingClassifier(estimators=[(
    'dt', model1), ('knn', model2), ('svc', model3)], voting='soft', weights=[2, 1, 2])

eclf = eclf.fit(X, y)

# from sklearn.externals import joblib
joblib.dump(eclf, './objects/ensemble.pkl')
