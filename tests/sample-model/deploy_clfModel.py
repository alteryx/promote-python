import helpers
import promote
import joblib
from schema import Schema

#optional for decorator

p = promote.Promote("colin", "789asdf879h789a79f79sf79s", "https://sandbox.c.yhat.com/")

# load model weights (must be relative path to 'pickles')
# clf = joblib.load(
#     '/Users/glamp/workspace/github.com/alteryx/promote-python-client/tests/sample-model/pickles/model_weights.pkl')
rng = joblib.load('/Users/glamp/workspace/github.com/alteryx/promote-python-client/tests/sample-model/pickles/rng.pkl')

# schema is optional
@promote.validate_json(Schema([{'name': And(str, len)}]))
def promoteModel(data):
    print(rng)
    prediction = helpers.punctuation.cleanName(str(data))
    if 'thing' not in prediction:
        return 'error'
    else:
        return prediction

# test data
testdata = {'name': 'greg'}

# test model locally
promoteModel(testdata)

# 1. test that testdata is valid json
# 2. THERE IS test data, run promoteModel(testdata) before deployment

p.deploy("HelloModel", promoteModel, testdata, verbose=2)
# p.deploy("HelloModel", promoteModel, testdata, confirm=True, dry_run=False, verbose=0)
# p.predict("HelloModel", testdata)
