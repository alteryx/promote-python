import promote

def helloWorldVec(data):
    return [
        {
            "id": i["id"],
            "greeting": 'Hello ' + i['name'] + '!'
        } for i in data]


USERNAME = 'ross'
API_KEY = 'your_api_key'
PROMOTE_URL = "https://promote.c.yhat.com/"

p = promote.Promote(USERNAME, API_KEY, PROMOTE_URL)

# test data
TESTDATA = [{"id": 1, "name": "Colin"}, {"id": 2, "name": "Ross"}]

# 1. test that TESTDATA is valid json
# 2. THERE IS test data, run helloWorld(TESTDATA) before deployment
print(helloWorldVec(TESTDATA))

p.deploy("HelloModelVec", helloWorldVec, TESTDATA,
         confirm=False, dry_run=False, verbose=1)
