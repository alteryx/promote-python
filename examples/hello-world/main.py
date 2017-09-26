import promote
from schema import Schema, And

# schema is optional
@promote.validate_json(Schema({'name': And(str, len)}))
def promoteModel(data):
    return data

USERNAME = 'austin'
API_KEY = '9a9773e8e8946c651c86fa6c651c86fa'
PROMOTE_URL = "https://sandbox.c.yhat.com/"

p = promote.Promote(USERNAME, API_KEY, PROMOTE_URL)

# test data
TESTDATA = {'name': 'austin'}

# test model locally
promoteModel(TESTDATA)

# 1. test that TESTDATA is valid json
# 2. THERE IS test data, run promoteModel(TESTDATA) before deployment

p.deploy("HelloModel1", TESTDATA, verbose=2)
# p.deploy("HelloModel", testdata, confirm=True, dry_run=False, verbose=0)

