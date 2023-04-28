import pytest
import sys
import json
import requests
from mockito import when, mock, unstub
from src.featurehelper import geocodeForward, getLocationInfo, \
                            findTimezone, getTimeInfo, \
                            arrowFromWindDirection, getCurrentWeather

arrowList = [
    (275,'→'),(23,'↓'),(270,'→'),(120,'←'),
    (55,'↙'),(65,'↙'),(150,'↖'),(200,'↑'),
    (235,'↗'),(320,'↘'),(100,'←')
    ]

@pytest.fixture()
def geo_code_response():
    return {"place_id": 307842104,
            "licence": "Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
            "osm_type": "relation",
            "osm_id": 52411,
            "boundingbox": [
            "49.4969821",
            "51.550781",
            "2.3889137",
            "6.408097"
            ],
            "lat": "50.6402809",
            "lon": "4.6667145",
            "display_name": "België / Belgique / Belgien",
            "class": "boundary",
            "type": "administrative",
            "importance": 0.8190605523573009,
            "icon": "https://nominatim.openstreetmap.org/ui/mapicons/poi_boundary_administrative.p.20.png"
            }

@pytest.fixture()
def loc_info():
    return {'locationName' : "België / Belgique / Belgien",
                'lat' : 50.6402809,
                'lon' : 4.6667145}

@pytest.fixture(scope="module")
def time_info():
    return getTimeInfo({'locationName' : "België / Belgique / Belgien",
                'lat' : 50.6402809,
                'lon' : 4.6667145})

@pytest.mark.parametrize("input, out", arrowList)
def test_arrowFromWindDirection(input, out) -> None:
    assert arrowFromWindDirection(input) == out

def test_arrowFromWindDirection_invalid() -> None:
    assert arrowFromWindDirection(370) == 'Invalid wind direction'

check_list = ['lat','lon','display_name',]

@pytest.mark.parametrize('key',check_list)
def test_geocodeForward(key) -> None:
    expected = {"place_id": 307842104,
                "licence": "Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
                "osm_type": "relation",
                "osm_id": 52411,
                "boundingbox": [
                "49.4969821",
                "51.550781",
                "2.3889137",
                "6.408097"
                ],
                "lat": "50.6402809",
                "lon": "4.6667145",
                "display_name": "België / Belgique / Belgien",
                "class": "boundary",
                "type": "administrative",
                "importance": 0.8190605523573009,
                "icon": "https://nominatim.openstreetmap.org/ui/mapicons/poi_boundary_administrative.p.20.png"
            }
    assert geocodeForward('Belgium')[key] == expected[key]

exception_list = [requests.Timeout,requests.exceptions.ConnectionError,requests.exceptions.RequestException]

@pytest.mark.parametrize('exception_error',exception_list)
def test_geocodeForward_exception(exception_error) -> None:

    params = {'q': 'Belgium','format':'json'}
        
    when(requests).get(f'https://nominatim.openstreetmap.org/search', params = params, timeout=10).thenRaise(exception_error)

    assert geocodeForward('Belgium') == {'displayName':'Not Found','lat':0.0,'lon':0.0}

@pytest.mark.skipif(sys.version_info < (3, 11), reason='StrEnum is only available in python 3.11 and later versions')
def test_getCurrentWeather() -> None:
    params = {
        'latitude': 50.6402809,
        'longitude': 4.6667145,
        'current_weather': True
    }
    response_dict = {
            "latitude": 50.64,
            "longitude": 4.6599994,
            "generationtime_ms": 0.1360177993774414,
            "utc_offset_seconds": 0,
            "timezone": "GMT",
            "timezone_abbreviation": "GMT",
            "elevation": 139.0,
            "current_weather": {
                "temperature": 8.7,
                "windspeed": 15.5,
                "winddirection": 338.0,
                "weathercode": 3,
                "is_day": 1,
                "time": "2023-04-25T15:00"
            }
        }
    mock_response = mock({
        'status_code': 200,
        'text': json.dumps(response_dict)
    }, spec=requests.Response)
    
    when(requests).get('https://api.open-meteo.com/v1/forecast', params = params, timeout = 10).thenReturn(mock_response)

    expected = {
        'temp': 8.7,
        'windspeed': 15.5,
        'winddirection': 338.0,
        'arrow': '↘',
        'weathercode': 'Overcast :cloud:',
    }

    assert getCurrentWeather(4.6667145,50.6402809) == expected
    unstub()

@pytest.mark.parametrize('exception_error',exception_list)
def test_getCurrentWeather_exception(exception_error) -> None:

    params = {
        'latitude': 50.6402809,
        'longitude': 4.6667145,
        'current_weather': True
    }
        
    when(requests).get('https://api.open-meteo.com/v1/forecast', params = params, timeout = 10).thenRaise(exception_error)
    
    expected = {
            'temp': None,
            'windspeed': None,
            'winddirection': None,
            'arrow': None,
            'weathercode': None,
        } 
    
    assert getCurrentWeather(4.6667145,50.6402809) == expected

def test_getLocationInfo(geo_code_response) -> None:
    expected = {'locationName' : "België / Belgique / Belgien",
                'lat' : 50.6402809,
                'lon' : 4.6667145}
    assert getLocationInfo(geo_code_response) == expected

def test_findTimezone_valid(loc_info) -> None:
    assert findTimezone(loc_info) == 'Europe/Brussels'

def test_findTimezone_invalid() -> None:
    assert findTimezone('Africa/Bamako') == 'Africa/Bamako'

def test_getTimeInfo_name(time_info) -> None:
    assert time_info.get('tzName') == 'Europe/Brussels'

@pytest.mark.skip(reason='Test not completed')
def test_getTimeInfo_currentTime_format(time_info) -> None:
    pass

def test_getTimeInfo_utc_offset(time_info) -> None:
    assert time_info.get('UTCOffset') == '+0200'

def test_getTimeInfo_utc_offset_hours(time_info) -> None:
    assert time_info.get('UTCOffsetHrs') == 2