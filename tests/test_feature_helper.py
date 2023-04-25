import pytest
import sys
from src.featurehelper import geocodeForward, getLocationInfo, findTimezone, getTimeInfo, arrowFromWindDirection

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

#Pass 'Beligium' then check response off predetermined 
def test_geocodeForward() -> None:
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
    assert geocodeForward('Belgium') == expected

@pytest.mark.skipif(sys.version_info < (3, 11), reason='StrEnum is only available in python 3.11 and later versions')
def test_getCurrentWeather() -> None:
    pass

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