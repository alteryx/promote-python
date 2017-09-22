import promote
from schema import Schema  # https://pypi.python.org/pypi/schema

from helpers import dbconn

# instanciate the Promote class with our API information
p = promote.Promote("colin", "789asdf879h789a79f79sf79s",
                    "https://sandbox.c.yhat.com/")

# validate that we only process data that has ints and floats
# @promote.validate_json(Schema([[int, float]]))


def promoteModel(data):
    user_info = dbconn.get_db_data(data.get('user_id'))
    # do things with the result of our DB query here:
    #
    return {"user_profile": user_info}


# some test data
testdata = {'user_id': '3ghj4l5j1'}
print(promoteModel(testdata))

# name and deploy our model
# p.deploy("UserDBLookup", promoteModel, testdata=testdata, confirm=True, dry_run=True, verbose=0)

# once our model is deployed and online, we can send data and recieve predictions
# p.predict("UserDBLookup", testdata)

# example result
#('f9471423-7537-4e03-949b', 'colin', 'd580d451-06b9-4c10-a73f-523adca5f48c',
#'$2a$10$I5fhBD03FvNpRhpI63T4ced09PaFYmN31WOjVro7ywTiwUK', 'admin', 
# datetime.datetime(2017, 8, 14, 21, 34, 43, 255000, 
# tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=0, name=None)))]
