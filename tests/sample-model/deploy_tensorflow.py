import helpers

from sklearn.externals import joblib

clf = joblib.load('./pickles/model_weights.pkl')

with tf as tensorflow:
    tf.session()
    tf.load('./pickles/model_weights.pkl')

t = [1,2,3,4,5]

import promote

p = promote.Promote("colin", "789asdf879h789a79f79sf79s", "https://sandbox.c.yhat.com/")

# schema is optional
@schema(Schema([{'name': And(str, len)}]))
def promoteModel(data):
    tf.evaluate(testdata)
    if prediction not in t:
        return 'error'
    else:
        return prediction

# testdata is optional
testdata = {'name': 'greg'}

promoteModel(testdata)

p.deploy("HelloModel", promoteModel, testdata=testdata, confirm=True, dry_run=False, verbose=0)
p.predict("HelloModel", testdata)