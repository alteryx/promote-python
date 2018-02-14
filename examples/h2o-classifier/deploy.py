import promote
import h2o
import os

h2o.init()

model_path = os.path.abspath('./objects/DRF_model_python_1512530312673_3')
model = h2o.load_model(model_path)

def helloh2o(data):
    # first transfrom our JSON into an H2OFrame
    h2o_data = h2o.H2OFrame(data)
    # Predict!
    res = model.predict(h2o_data).as_data_frame().to_dict()
    return {'response': res}

USERNAME = 'ross'
API_KEY = 'your_api_key'
PROMOTE_URL = "https://promote.c.yhat.com/"


p = promote.Promote(USERNAME, API_KEY, PROMOTE_URL)

# test data
TESTDATA = {"C1":4.9,"C2":3,"C3":1.4,"C4":0.2}

# test model locally
print(helloh2o(TESTDATA))

# test that TESTDATA is valid json
p.deploy("helloh2o", helloh2o, TESTDATA, confirm=True, dry_run=False, verbose=1)