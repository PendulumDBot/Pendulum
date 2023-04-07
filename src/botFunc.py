from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

global TF
TF = TimezoneFinder()

def getTime(location):
    geolocator = Nominatim(user_agent="pendulum")
    coords = geolocator.geocode(location)
    tz = TF.timezone_at(lng=coords.longitude, lat=coords.latitude)
    return datetime.now(pytz.timezone(tz))
   
