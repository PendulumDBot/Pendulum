import json
from timezonefinder import TimezoneFinder
from pytz import timezone, all_timezones
import requests
from datetime import datetime
from .weathercodes import weatherCodes
import logging

#Constants
FORMAT = "%Y-%b-%d %X"
tf = TimezoneFinder()

def geocodeForward(location):
    """ Converts string into usable location info

    Args:
        location (string): Address,Country,State of the target Location

    Returns:
        JSON : Response
    """
    params = {'q': location,'format':'json'}

    try:    #Timeout Exception
        response = requests.get(f'https://nominatim.openstreetmap.org/search', params = params, timeout=10)
    except requests.exceptions.Timeout as err:
        logging.error(err, exc_info = True)
        return {'displayName':'Not Found','lat':0.0,'lon':0.0}
    except requests.exceptions.ConnectionError as err:
        logging.error(err, exc_info = True)
        return {'displayName':'Not Found','lat':0.0,'lon':0.0}
    except requests.exceptions.RequestException as err:
        logging.error(f'Critical Error has occurred')
        logging.error(err, exc_info = True)
        return {'displayName':'Not Found','lat':0.0,'lon':0.0}

    return json.loads(response.text)[0]

def getLocationInfo(location):
    """Retrieves needed JSON Info from JSON response

    Args:
        location (JSON String): String retrieved from geocodeForward 

    Returns:
        dict: Location Name, Latitude, Longitude
    """
    return { "locationName" : location.get("display_name"),
                 "lat" : float(location.get("lat")),
                 "lon" : float(location.get("lon"))
                 }

def findTimezone(location):
    """gets timezone from longitude and latitude

    Args:
        location (dict): dict with lattitude, and longitude

    Returns:
         str: timezone
    """
    if location not in all_timezones:
        longitude = location["lon"]
        latitude = location["lat"]
        return tf.timezone_at(lng=longitude,lat=latitude)
    else: 
       return location

def getTimeInfo(location):
    """gets timezone, currentime, UTCOffset and Hours 

    Args:
        location (str): target location

    Returns:
        dict: with required info
    """
    tzLocation = findTimezone(location)
    timeNow = datetime.now(timezone(tzLocation))
    timeInfo = {"tzName" : tzLocation,
                "currentTime" : datetime.now(timezone(findTimezone(location))).strftime(FORMAT),
                "UTCOffset" : timeNow.strftime('%z'),
                "UTCOffsetHrs" :  int(timeNow.strftime('%z'))//100}

    return timeInfo

def getCurrentWeather(lon, lat):
    """get current liveweather from API

    Args:
        lon (float): longititude of target location
        lat (float): latitutde of target location

    Returns:
        dict: of weather information
    """

    params = {
        'latitude': lat,
        'longitude': lon,
        'current_weather': True
    }

    try:
        response = requests.get('https://api.open-meteo.com/v1/forecast', params = params, timeout = 10)
    except requests.exceptions.Timeout as err:
        logging.error(f'Request timed out')
        logging.error(err,exc_info = True)
        response = None
    except requests.exceptions.ConnectionError as err:
        logging.error(f'Connection Error occurred')
        logging.error(err, exc_info = True)
        response = None
    except requests.exceptions.RequestException as err:
        logging.error(f'Critical Error occurred')
        logging.error(err,exc_info = True)
        response = None

    if response is None:
        return {
            'temp': None,
            'windspeed': None,
            'winddirection': None,
            'arrow': None,
            'weathercode': None,
        } 

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
    """switch case for displaying arrows with respect to wind angle

    Args:
        direction (float): wind direction in degress

    Returns:
        string: direction symbol
    """
    
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

