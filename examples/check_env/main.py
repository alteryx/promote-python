import sys
import requests
import promote


def check_env(TESTDATA):
    return {'response': 'Env info',
            'Python_version': sys.version,
            'requests_version': requests.__version__}

# instanciate the Promote class with our API information
USERNAME = 'username'
API_KEY = 'your_api_key'
PROMOTE_URL = 'http://www.promote_url.com'

p = promote.Promote(USERNAME, API_KEY, PROMOTE_URL)

# test data
TESTDATA = {'name': 'austin'}

# test model locally
print(check_env(TESTDATA))

# 1. test that TESTDATA is valid json
# 2. THERE IS test data, run helloWorld(TESTDATA) before deployment
p.deploy("CheckEnv", check_env, TESTDATA, confirm=True, dry_run=False, verbose=1)

