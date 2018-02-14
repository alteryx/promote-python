import promote
from schema import Schema  # https://pypi.python.org/pypi/schema

from helpers import dbconn

# instanciate the Promote class with our API information
USERNAME = "colin"
API_KEY = "your_api_key"
PROMOTE_URL = "https://promote.c.yhat.com/"

p = promote.Promote(USERNAME, API_KEY, PROMOTE_URL)

# validate that we only process data that has ints and floats
@promote.validate_json(Schema({'id': str}))
def promoteModel(data):
    user_info = dbconn.get_db_data(data.get('id'))
    # do things with the result of our DB query here:
    #
    return {"user_profile": user_info}


# some test data
TESTDATA = {"id": "f9471423-7537-4e03-949b-1fb521cfffd1"}
print(promoteModel(TESTDATA))

# name and deploy our model
# p.deploy("UserDBLookup", promoteModel, TESTDATA, confirm=True, dry_run=True, verbose=0)

# once our model is deployed and online, we can send data and recieve predictions
# p.predict("UserDBLookup", TESTDATA)

# example result
#   {
#     "id": "f9471423-7537-4e03-949b-1fb521cfffd1",
#     "username": "greg",
#     "favoritefood": "pizza-bagels",
#     "favoritesport": "baseball"
#   }
