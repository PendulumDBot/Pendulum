import json
from pytz import timezone
import requests
from datetime import datetime

FORMAT = "%Y-%b-%d %X"

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
    mode = 0
    lng = location["lon"]
    lat = location["lat"]
    response = requests.get(f"http://timezonefinder.michelfe.it/api/{mode}_{lng}_{lat}")
    return json.loads(response.text)["tz_name"]

def getTimeInfo(location):
    tzLocation = findTimezone(location)
    timeNow = datetime.now(timezone(tzLocation))
    timeInfo = {"tzName" : tzLocation,
                "currentTime" : datetime.now(timezone(findTimezone(location))).strftime(FORMAT),
                "UTCOffset" : timeNow.strftime('%z')}

    return timeInfo

print(getTimeInfo(getLocationInfo(geocodeForward("penang"))))

