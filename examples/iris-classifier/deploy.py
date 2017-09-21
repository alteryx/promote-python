import promote
from schema import Schema #https://pypi.python.org/pypi/schema
import json

import helpers
# load in our saved model weights
from sklearn.externals import joblib
weights = joblib.load('./objects/model_weights.pkl')

# instanciate the Promote class with our API information
p = promote.Promote("colin", "789asdf879h789a79f79sf79s", "https://sandbox.c.yhat.com/")

#validate that we only process data that has ints and floats
@promote.validate_json(Schema([[int, float]]))
def promoteModel(data):
    # print(weights)
    prediction = helpers.getclass.get_classname(weights.predict(data).tolist())
    return {"prediction": prediction}
    
# some test data
testdata = [[5.1, 3.5, 1.4, 0.2], [ 6.7,  3.1,  5.6,  2.4]]
promoteModel(testdata)

# name and deploy our model
p.deploy("HelloModel", promoteModel, testdata=testdata, confirm=True, dry_run=True, verbose=0)

# once our model is deployed and online, we can send data and recieve predictions
# p.predict("HelloModel", testdata)