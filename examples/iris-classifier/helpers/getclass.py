from sklearn import datasets

iris = datasets.load_iris()

def get_classname(data):
    return iris.target_names[data].tolist()
