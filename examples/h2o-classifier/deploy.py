import promote
import h2o
import os

# Alteryx recommends limiting the amount of memory that h2o can consume with the `max_mem_size` flag.
# the defualt is 4gb, which is likely more than you need!
h2o.init(max_mem_size='100m')

model_path = os.path.abspath('./objects/h2o_rf_model')
model = h2o.load_model(model_path)

def helloh2o(data):
    # first transfrom our JSON into an H2OFrame
    h2o_data = h2o.H2OFrame(data)
    # Predict!
    prediction = model.predict(h2o_data)
    model_response = prediction.as_data_frame().to_dict()

    # h2o will automatically hold on to the prediction data, which is a feature we don't need in promote
    # you must use h2o.remove() to remove this prediction from memory, otherwise you will eventually run
    # out of memory for your model.
    # http://docs.h2o.ai/h2o/latest-stable/h2o-py/docs/h2o.html?highlight=remove#h2o.remove
    h2o.remove(h2o_data)
    h2o.remove(prediction)

    # Return the result as our response.
    return {'response': model_response}

USERNAME = 'username'
API_KEY = 'your_api_key'
PROMOTE_URL = 'http://www.promote_url.com'

p = promote.Promote(USERNAME, API_KEY, PROMOTE_URL)

# add metadata
p.metadata.logloss = float("{0:.5f}".format(model.logloss()))

# test data
TESTDATA = {"C1":4.9,"C2":3,"C3":1.4,"C4":0.2}

# test model locally
print(helloh2o(TESTDATA))

# test that TESTDATA is valid json
p.deploy("helloh2o", helloh2o, TESTDATA, confirm=True, dry_run=False, verbose=1)
