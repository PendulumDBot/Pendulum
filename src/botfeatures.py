from datetime import datetime, timedelta
from dateutil import parser
import json
from .featurehelper import geocodeForward, getLocationInfo, getTimeInfo, getCurrentWeather
from timezonefinder import TimezoneFinder
import pytz
from time import perf_counter
import requests

global TF, FORMAT
TF = TimezoneFinder()
FORMAT = "%Y-%b-%d %X"

def getTime(location):
    tstart = perf_counter()
    geocode = geocodeForward(location)
    locInfo = getLocationInfo(geocode)
    timeInfo = getTimeInfo(locInfo)
    tend = perf_counter()
    print(tend-tstart)
    return (timeInfo["currentTime"],locInfo["locationName"])

def getWeather(location):
    
    geocode = geocodeForward(location)
    locInfo = getLocationInfo(geocode)

    currentWeather = getCurrentWeather(locInfo['lon'], locInfo['lat'])
    currentWeather['location'] = locInfo['locationName']

    return currentWeather

def diffTime(initLoc, targetLoc):
    Loc1 = geocodeForward(initLoc)
    Loc2 = geocodeForward(targetLoc)

    #get json info
    locInfo1 = getLocationInfo(Loc1)
    locInfo2 = getLocationInfo(Loc2)

    #get Timezone at Coords
    time1 = getTimeInfo(locInfo1)["UTCOffsetHrs"]
    time2 = getTimeInfo(locInfo2)["UTCOffsetHrs"]
    print(time1,time2)

    if(time1 < time2):
        message = (f'{locInfo1["locationName"]} is behind {locInfo2["locationName"]}'
                   f' by {time2 - time1} hour(s)')
    else:
       message = (f'{locInfo1["locationName"]} is ahead {locInfo2["locationName"]}'
                   f' by {time1 - time2} hour(s)')

    
    return message , getTimeInfo(locInfo1)["currentTime"], getTimeInfo(locInfo2)["currentTime"]

def timeAt(time,timezone,location):
    #parse initial date/time
    initTime = datetime.strptime(parser.parse(time).strftime(FORMAT),FORMAT)
    print(initTime)
    if timezone in pytz.all_timezones:
        initTz = timezone
        initTz = getTimeInfo(timezone)
    else:
        initTz = geocodeForward(timezone)
        initTz = getTimeInfo(getLocationInfo(initTz))

   
    initHRDiff = initTz["UTCOffsetHrs"]
    print(initHRDiff)
    timeUTC = initTime + timedelta(hours=-(initHRDiff) if initHRDiff > 0 else initHRDiff)

    targetLoc = getTimeInfo(getLocationInfo(geocodeForward(location)))
    targetHRDiff = targetLoc["UTCOffsetHrs"]
    targetTime = timeUTC + timedelta(hours=targetHRDiff)

    return targetTime

print(diffTime("BKK","Malaysia"))
print(timeAt("9:09 pm","GMT","UK"))