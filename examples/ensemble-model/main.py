import promote
import joblib
from schema import Schema

USERNAME = "colin"
API_KEY = "your_api_key"
PROMOTE_URL = "https://promote.c.yhat.com/"

p = promote.Promote(USERNAME, API_KEY, PROMOTE_URL)

# load our ensemble model weights
ENSEMBLE = joblib.load('./objects/ensemble.pkl')

# add metadata
p.metadata["voting"] = ENSEMBLE.voting
p.metadata["weights"] = dict(zip([e[0] for e in ENSEMBLE.estimators],ENSEMBLE.weights))

# ensure that data sent to our model is only ints or floats
@promote.validate_json(Schema([[int, float]]))
def ensembleModel(data):
    preds = ENSEMBLE.predict_proba(data).tolist()
    res = []
    for i in preds:
        res.append({"predicted": i})
    return res


TESTDATA = [[5.1, 3.5], [6.7, 3.1]]
ensembleModel(TESTDATA)

# name and deploy our model
p.deploy("EnsembleClassifier", ensembleModel, TESTDATA, confirm=True, dry_run=False, verbose=1)

# once our model is deployed and online, we can send data and recieve predictions
# p.predict("EnsembleClassifier", TESTDATA)