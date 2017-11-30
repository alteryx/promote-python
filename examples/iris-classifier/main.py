import promote
from schema import Schema #https://pypi.python.org/pypi/schema

from helpers import getclass
# load in our saved model weights
from sklearn.externals import joblib
WEIGHTS = joblib.load('./objects/model_weights.pkl')

# instanciate the Promote class with our API information
USERNAME = "colin"
API_KEY = "789asdf879h789a79f79sf79s"
PROMOTE_URL = "https://sandbox.c.yhat.com/"

p = promote.Promote(USERNAME, API_KEY, PROMOTE_URL)

#validate that we only process data that has ints and floats
@promote.validate_json(Schema([[int, float]]))
def irisClassifier(data):
    prediction = getclass.get_classname(WEIGHTS.predict(data).tolist())
    return {"prediction": prediction}

# Add two flowers as test data
TESTDATA = [[5.1, 3.5, 1.4, 0.2], [6.7, 3.1, 5.6, 2.4]]
print(irisClassifier(TESTDATA))

# name and deploy our model
bundle = p.deploy("IrisClassifier", irisClassifier, TESTDATA, confirm=True, dry_run=True, verbose=2)
print(bundle)

# once our model is deployed and online, we can send data and recieve predictions
# p.predict("IrisClassifier", TESTDATA)
