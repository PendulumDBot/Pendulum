import pytest
from src.botfeatures import getTime, getWeather, diffTime, timeAt

def test_getTime(mocker) -> None:
    geo_code_mock = {"place_id": 307842104,
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
    get_time_info_mock = {
        "tzName" : 'Europe/Brussels',
        "currentTime" : '2023-Apr-25 12:28:11',
        "UTCOffset" : '+0200',
        "UTCOffsetHrs" : 2
        }
    mocker.patch(
        'src.botfeatures.geocodeForward',
        return_value = geo_code_mock
    )
    mocker.patch(
        'src.botfeatures.getTimeInfo',
        return_value = get_time_info_mock
    )
    expected = ('2023-Apr-25 12:28:11','België / Belgique / Belgien')
    assert getTime('Belgium') == expected

@pytest.mark.skip()
def test_getWeather() -> None:
    pass

@pytest.mark.skip()
def test_diffTime() -> None:
    pass

@pytest.mark.skip()
def test_timeAt() -> None:
    pass