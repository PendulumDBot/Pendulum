from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
from time import perf_counter

global TF
TF = TimezoneFinder()

def getTime(location):
    tstart = perf_counter()
    geolocator = Nominatim(user_agent="pendulum")
    coords = geolocator.geocode(location)
    tz = TF.timezone_at(lng=coords.longitude, lat=coords.latitude)
    tend = perf_counter()
    print(tend-tstart)
    return (datetime.now(pytz.timezone(tz)),coords)


    
   
