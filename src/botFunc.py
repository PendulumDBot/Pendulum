from datetime import datetime
import json
import feature
from timezonefinder import TimezoneFinder
import pytz
from time import perf_counter
import requests

global TF
TF = TimezoneFinder()

def getTime(location):
    tstart = perf_counter()
    geocode = feature.geocodeFoward(location)
    #print(json.dumps(geocode, indent = 2, sort_keys=True))
    locationName = geocode.get("display_name")

    lat = float(geocode.get("lat"))
    lon = float(geocode.get("lon"))

    tz = TF.timezone_at(lng=lon, lat=lat)
    tend = perf_counter()

    print(tend-tstart)
    return (datetime.now(pytz.timezone(tz)),locationName)

def getWeather(location):
    response = requests.get(f'http://wttr.in/{location}', params={'format': '3'}, timeout=30)
    return response.text


