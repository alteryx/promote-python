import requests
import os

def request_weather(apikey, lat, lon):
    url = 'https://api.darksky.net/forecast/' + apikey + '/' + lat + ',' + lon
    r = requests.get(url)
    r.json().get('currently')['apparentTemperature']
    return r.json().get('currently')['apparentTemperature']