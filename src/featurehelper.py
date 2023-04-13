import json
from timezonefinder import TimezoneFinder
from pytz import timezone, all_timezones
import requests
from datetime import datetime

FORMAT = "%Y-%b-%d %X"
tf = TimezoneFinder()

def geocodeForward(location):
    params = {'q': location,'format':'json'}
    response = requests.get(f'https://nominatim.openstreetmap.org/search', params = params, timeout=30)
    return json.loads(response.text)[0]

def getLocationInfo(location):
    return { "locationName" : location.get("display_name"),
                 "lat" : float(location.get("lat")),
                 "lon" : float(location.get("lon"))
                 }

def findTimezone(location):
    if location not in all_timezones:
        longitude = location["lon"]
        latitude = location["lat"]
        return tf.timezone_at(lng=longitude,lat=latitude)
    else: 
       return location

def getTimeInfo(location):
    tzLocation = findTimezone(location)
    timeNow = datetime.now(timezone(tzLocation))
    timeInfo = {"tzName" : tzLocation,
                "currentTime" : datetime.now(timezone(findTimezone(location))).strftime(FORMAT),
                "UTCOffset" : timeNow.strftime('%z'),
                "UTCOffsetHrs" :  int(timeNow.strftime('%z'))//100}

    return timeInfo

#print(getTimeInfo(getLocationInfo(geocodeForward("penang"))))
#print(all_timezones)

