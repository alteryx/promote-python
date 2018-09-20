import promote
from schema import Schema #https://pypi.python.org/pypi/schema
import pyodbc

# instanciate the Promote class with our API information
USERNAME = "USERNAME"
API_KEY = "APIKEY"
PROMOTE_URL = "http://promoteurl.com/"

p = promote.Promote(USERNAME, API_KEY, PROMOTE_URL)

#validate that we only process data that has ints and floats
@promote.validate_json(Schema([[int, float]]))
def connectToDB(data):
    # build our query
    query = "Select * FROM my_table WHERE value={:s}".format(data['value'])
    
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=testdb;UID=me;PWD=pass')
    cnxn = pyodbc.connect('DSN=test;PWD=password')
    cursor = cnxn.cursor()

    # execute our query and return row
    cursor.execute(query)
    row = cursor.fetchone()

    return {"prediction": row}

TESTDATA = {"value": 10}

# name and deploy our model
p.deploy("DBConector", connectToDB, TESTDATA, confirm=True, dry_run=False, verbose=2)