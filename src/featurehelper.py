import json
from timezonefinder import TimezoneFinder
from pytz import timezone, all_timezones
import requests
from datetime import datetime
from .weathercodes import weatherCodes
import logging

FORMAT = "%Y-%b-%d %X"
tf = TimezoneFinder()

def geocodeForward(location):
    params = {'q': location,'format':'json'}

    try:    #Timeout Exception
        response = requests.get(f'https://nominatim.openstreetmap.org/search', params = params, timeout=10)
    except requests.Timeout as err:
        logging.error({'message':err.message},exc_info=True)
    except requests.exceptions.RequestException:
        logging.error(f'Critical Error has occurred')
        logging.error({'message':err.message},exc_info=True)

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

def getCurrentWeather(lon, lat):

    params = {
        'latitude': lat,
        'longitude': lon,
        'current_weather': True
    }

    try:    #Timeout Exception
        response = requests.get('https://api.open-meteo.com/v1/forecast', params = params, timeout = 10)
    except requests.Timeout as err:
        logging.error(f'Request timed out')
        logging.error({'message':err.message},exc_info=True)
    except requests.exceptions.RequestException as err:
        logging.error(f'Critical Error occurred')
        logging.error({'message':err.message},exc_info=True)


    responseDictionary = json.loads(response.text)
    currentWeather = responseDictionary['current_weather']

    weatherCodeToTranslate = currentWeather['weathercode']

    arrow = arrowFromWindDirection(currentWeather['winddirection'])

    weatherInfo = {
        'temp': currentWeather['temperature'],
        'windspeed': currentWeather['windspeed'],
        'winddirection': currentWeather['winddirection'],
        'arrow': arrow,
        'weathercode': weatherCodes[f's{weatherCodeToTranslate}'],
    }

    return weatherInfo

def arrowFromWindDirection(direction):
    
    num = int(direction)//45
    
    match num:
        case 0:
            return '↓'
        case 1:
            return '↙'
        case 2:
            return '←'
        case 3:
            return '↖'
        case 4:
            return '↑'
        case 5:
            return '↗'
        case 6:
            return '→'
        case 7:
            return '↘'
        case _:
            return 'Invalid wind direction'
        

#print(getTimeInfo(getLocationInfo(geocodeForward("penang"))))
#print(all_timezones)

