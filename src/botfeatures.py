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
    geocode = geocodeForward(location)
    locInfo = getLocationInfo(geocode)
    timeInfo = getTimeInfo(locInfo)
    return (timeInfo,locInfo["locationName"])

def getWeather(location):
    
    geocode = geocodeForward(location)
    locInfo = getLocationInfo(geocode)

    currentWeather = getCurrentWeather(locInfo['lon'], locInfo['lat'])
    currentWeather['location'] = locInfo['locationName']

    return currentWeather

def diffTime(initLoc, targetLoc):
    timeInfo1, locName1 = getTime(initLoc)
    timeInfo2, locName2 = getTime(targetLoc)
    #get Timezone at Coords
    time1 = timeInfo1["UTCOffsetHrs"]
    time2 = timeInfo2["UTCOffsetHrs"]

    if(time1 < time2):
        message = (f'{locName1} is behind {locName2}'
                   f' by {time2 - time1} hour(s)')
    else:
       message = (f'{locName1} is ahead {locName2}'
                   f' by {time1 - time2} hour(s)')

    
    return message , timeInfo1["currentTime"], timeInfo2["currentTime"]

def timeAt(time,timezone,location):
    """Get time at location converted to target loc

    Args:
        time (_type_): _description_
        timezone (_type_): _description_
        location (_type_): _description_

    Returns:
        _type_: _description_
    """

    #parse initial date/time
    initTime = datetime.strptime(parser.parse(time).strftime(FORMAT),FORMAT)



    if timezone in pytz.all_timezones:
        initTz = timezone
        initTz = getTimeInfo(timezone)
        initLocName = timezone
    else:
        initTz = geocodeForward(timezone)
        initLocTz = getLocationInfo(initTz)
        initLocName = initLocTz["locationName"]
        initTz = getTimeInfo(initLocTz)


    initHRDiff = initTz["UTCOffsetHrs"]
    print(initHRDiff)
    timeUTC = initTime + timedelta(hours=-(initHRDiff) if initHRDiff > 0 else initHRDiff)

    targetLocInfo = getLocationInfo(geocodeForward(location))
    targetLoc = getTimeInfo(targetLocInfo)
    targetHRDiff = targetLoc["UTCOffsetHrs"]
    targetTime = timeUTC + timedelta(hours=targetHRDiff)

    return initTime, targetTime, initLocName, targetLocInfo["locationName"]

#print(timeAt("9:09","GMT","UK"))