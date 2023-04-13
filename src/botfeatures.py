from datetime import datetime
import json
from .featurehelper import geocodeForward, getLocationInfo, getTimeInfo
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
    locInfo = getLocationInfo(geocode)
    timeInfo = getTimeInfo(locInfo)
    tend = perf_counter()
    print(tend-tstart)
    return (timeInfo["currentTime"],locInfo["locationName"])

def getWeather(location):
    response = requests.get(f'http://wttr.in/{location}', params={'format': '3'}, timeout=30)
    return response.text

def diffTime(initLoc, targetLoc):
    Loc1 = geocodeForward(initLoc)
    Loc2 = geocodeForward(targetLoc)

    #get json info
    locInfo1 = getLocationInfo(Loc1)
    locInfo2 = getLocationInfo(Loc2)

    #get Timezone at Coords
    time1 = getTimeInfo(locInfo1)["UTCOffsetHrs"]
    time2 = getTimeInfo(locInfo2)["UTCOffsetHrs"]

    if(time1 < time2):
        message = (f'{locInfo1["locationName"]} is behind {locInfo2["locationName"]}'
                   f'by {time2 - time1} hour(s)')
    else:
       message = (f'{locInfo1["locationName"]} is ahead {locInfo2["locationName"]}'
                   f' by {time1 - time2} hour(s)')

    
    return message , getTimeInfo(locInfo1)["currentTime"], getTimeInfo(locInfo2)["currentTime"]
    