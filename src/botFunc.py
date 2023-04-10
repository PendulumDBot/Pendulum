from datetime import datetime
import json
from timezonefinder import TimezoneFinder
import pytz
from time import perf_counter
import requests

global TF
TF = TimezoneFinder()

def getTime(location):
    tstart = perf_counter()
    params = {'q': location,'format':'json'}
    response = requests.get(f'https://nominatim.openstreetmap.org/search', params = params, timeout=30)
    geocode = json.loads(response.text)[0]

    #print(json.dumps(geocode, indent = 2, sort_keys=True))
    locationName = geocode.get("display_name")

    lat = float(geocode.get("lat"))
    lon = float(geocode.get("lon"))

    tz = TF.timezone_at(lng=lon, lat=lat)
    tend = perf_counter()
    timeAt = datetime.now(pytz.timezone(tz)).strftime("%Y-%b-%d %X")

    print(tend-tstart)
    return (timeAt,locationName)

def getWeather(location):
    response = requests.get(f'http://wttr.in/{location}', params={'format': '3'}, timeout=30)
    return response.text
