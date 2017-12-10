import promote
from schema import Schema, And

# schema is optional https://pypi.python.org/pypi/schema
# @promote.validate_json(Schema({'name': And(str, lambda s: len(s) > 1)}))
# def helloWorld(data):
#     return {'response': 'Hello ' + data['name'] + '!'}


def helloWorldVec(data):
    return [
        {
            "id": i["id"],
            "greeting": 'Hello ' + i['name'] + '!'
        } for i in data]


USERNAME = 'ross'
API_KEY = '2dcf2d39-0d4a-4d4b-b79d-7b7033e0532f'
PROMOTE_URL = "http://promote.x.yhat.com/"

p = promote.Promote(USERNAME, API_KEY, PROMOTE_URL)

# test data
TESTDATA = [{"id": 1, "name": "Colin"}, {"id": 2, "name": "Ross"}]

# 1. test that TESTDATA is valid json
# 2. THERE IS test data, run helloWorld(TESTDATA) before deployment
print(helloWorldVec(TESTDATA))

p.deploy("HelloModelVec", helloWorldVec, TESTDATA,
         confirm=False, dry_run=True, verbose=1)
