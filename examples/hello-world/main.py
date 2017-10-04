import promote
from schema import Schema, And

# schema is optional https://pypi.python.org/pypi/schema
@promote.validate_json(Schema({'name': And(str, lambda s: len(s) > 1)}))
def promoteModel(data):
    return {'response': 'Hello ' + data['name'] + '!'}

USERNAME = 'colin'
API_KEY = 'd580d451-06b9-4c10-a73f-523adca5f48c'
PROMOTE_URL = "http://54.201.55.134:3001/"

p = promote.Promote(USERNAME, API_KEY, PROMOTE_URL)

# test data
TESTDATA = {'name': 'austin'}

# test model locally
print(promoteModel(TESTDATA))

# 1. test that TESTDATA is valid json
# 2. THERE IS test data, run promoteModel(TESTDATA) before deployment
# p.deploy("HelloModel", promoteModel, TESTDATA, True, False)