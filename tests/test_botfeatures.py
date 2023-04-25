import pytest
from unittest.mock import MagicMock
from src.botfeatures import getTime, getWeather, diffTime, timeAt

@pytest.fixture(scope = 'module')
def geo_code_mock_belgium():
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

@pytest.fixture(scope = 'module')
def get_time_info_mock_belgium():
    return {
        "tzName" : 'Europe/Brussels',
        "currentTime" : '2023-Apr-25 12:28:11',
        "UTCOffset" : '+0200',
        "UTCOffsetHrs" : 2
        }

def test_getTime(mocker,geo_code_mock_belgium,get_time_info_mock_belgium) -> None:
    mocker.patch(
        'src.botfeatures.geocodeForward',
        return_value = geo_code_mock_belgium
    )
    mocker.patch(
        'src.botfeatures.getTimeInfo',
        return_value = get_time_info_mock_belgium
    )
    expected = ('2023-Apr-25 12:28:11','België / Belgique / Belgien')
    assert getTime('Belgium') == expected

@pytest.mark.skip()
def test_getWeather() -> None:
    pass


def test_diffTime(mocker,geo_code_mock_belgium,get_time_info_mock_belgium) -> None:
    geo_code_mock_russia = {
        "place_id": 307593314,
        "licence": "Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
        "osm_type": "relation",
        "osm_id": 60189,
        "boundingbox": [
        "41.1850968",
        "82.0586232",
        "-180",
        "180"
        ],
        "lat": "64.6863136",
        "lon": "97.7453061",
        "display_name": "Россия",
        "class": "boundary",
        "type": "administrative",
        "importance": 0.852192362078589,
        "icon": "https://nominatim.openstreetmap.org/ui/mapicons/poi_boundary_administrative.p.20.png"
    }

    get_time_info_mock_russia = {
        "tzName" : 'Asia/Krasnoyarsk',
        "currentTime" : '2023-Apr-25 17:51:42',
        "UTCOffset" : '+0700',
        "UTCOffsetHrs" :  7
    }

    get_geocodeForward = MagicMock()
    get_geocodeForward.side_effect = [geo_code_mock_belgium,geo_code_mock_russia]

    get_getTimeInfo = MagicMock()
    get_getTimeInfo.side_effect = [get_time_info_mock_belgium,get_time_info_mock_russia]

    expected_message = f'België / Belgique / Belgien is behind Россия by 5 hour(s)'
    expected = (expected_message,'2023-Apr-25 12:28:11','2023-Apr-25 17:51:42')
    result1, result2, result3 = diffTime('Belgium','Russia')
    final_result = (result1, result2, result3)
    print(final_result,'printed statement')
    assert final_result == expected

@pytest.mark.skip()
def test_timeAt() -> None:
    pass