from datetime import datetime
import json
from .feature import geocodeForward, getLocationInfo
from timezonefinder import TimezoneFinder
import pytz
from time import perf_counter
import requests

global TF
TF = TimezoneFinder()
format = "%Y-%b-%d %X"

def getTime(location):
    tstart = perf_counter()
    geocode = geocodeForward(location)
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


def diffTime(initLoc, targetLoc):
    timeLoc1 = geocodeForward(initLoc)
    timeLoc2 = geocodeForward(targetLoc)

    locInfo1 = getLocationInfo(timeLoc1)
    locInfo2 = getLocationInfo(timeLoc2)

    tz1 = TF.timezone_at(lng=locInfo1["lon"], lat=locInfo1["lat"])
    tz2 = TF.timezone_at(lng=locInfo2["lon"], lat=locInfo2["lat"])
    
    time1 = int(datetime.now(pytz.timezone(tz1)).strftime('%z'))//100
    time2 = int(datetime.now(pytz.timezone(tz2)).strftime('%z'))//100

    if(time1 < time2):
        message = (f'{locInfo1["LocationName"]} is behind {locInfo2["LocationName"]}'
                   f'by {time2 - time1} hour(s)')
    else:
       message = (f'{locInfo1["LocationName"]} is ahead {locInfo2["LocationName"]}'
                   f' by {time1 - time2} hour(s)')
    
    return message
    
print(diffTime("penang", "bkk"))

