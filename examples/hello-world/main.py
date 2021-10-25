import promote
from schema import Schema, And

# schema is optional https://pypi.python.org/pypi/schema
@promote.validate_json(Schema({'name': And(str, lambda s: len(s) > 1)}))
def helloWorld(data):
    import sys
    import requests
    return {'response': 'Hello ' + data['name'] + '!',
            'Python_version': sys.version,
            'requests_version': requests.__version__}

USERNAME = 'username'
API_KEY = 'your_api_key'
PROMOTE_URL = 'http://www.promote_url.com'

p = promote.Promote(USERNAME, API_KEY, PROMOTE_URL)

# test data
TESTDATA = {'name': 'austin'}

# test model locally
print(helloWorld(TESTDATA))

# 1. test that TESTDATA is valid json
# 2. THERE IS test data, run helloWorld(TESTDATA) before deployment
p.deploy("HelloModel", helloWorld, TESTDATA, confirm=True, dry_run=False, verbose=1)

