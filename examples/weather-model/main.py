import promote
from schema import Schema  # https://pypi.python.org/pypi/schema

import os
from helpers import tempdesc
from helpers import get_weather

# instanciate the Promote class with our API information
USERNAME = 'username'
API_KEY = 'your_api_key'
PROMOTE_URL = 'http://www.promote_url.com'
DARKSKY_API_KEY = os.environ['DARKSKY_API_KEY'] # get a darksky api key: https://darksky.net/dev
p = promote.Promote(USERNAME, API_KEY, PROMOTE_URL)

# validate that we only process data that has ints and floats
@promote.validate_json(Schema({'lat': str, 'lon': str}))
def weatherModel(data):
    lat = data.get('lat')
    lon = data.get('lon')
    temp = get_weather.request_weather(DARKSKY_API_KEY, lat, lon)
    desc = tempdesc.lookup(temp)
    return {"tempature": temp, "feels": desc}

# some test data
TESTDATA = {'lat':'37', 'lon':'-122'}
print(weatherModel(TESTDATA))

# name and deploy our model
p.deploy("WeatherModel", weatherModel, TESTDATA, confirm=True, dry_run=True)

# once our model is deployed and online, we can send data and recieve predictions
# p.predict("UserDBLookup", TESTDATA)

# example result
# {
#     "tempature": 73.67, 
#     "feels": "Warm"
# }
