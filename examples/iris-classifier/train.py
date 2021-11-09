import joblib
from sklearn.neighbors import KNeighborsClassifier
from sklearn import datasets

iris = datasets.load_iris()

X = iris.data
y = iris.target

# Create and fit a nearest-neighbor classifier
knn = KNeighborsClassifier()
knn.fit(X, y)
KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski',
                     metric_params=None, n_jobs=1, n_neighbors=5, p=2,
                     weights='uniform')

# save our trained model to a pickle file so we can use it later
joblib.dump(knn, './objects/model_weights.pkl')
