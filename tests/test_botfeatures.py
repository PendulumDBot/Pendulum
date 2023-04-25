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
    expected = ({
        "tzName" : 'Europe/Brussels',
        "currentTime" : '2023-Apr-25 12:28:11',
        "UTCOffset" : '+0200',
        "UTCOffsetHrs" : 2
        },
        'België / Belgique / Belgien'
        )
    assert getTime('Belgium') == expected

@pytest.mark.skip()
def test_getWeather() -> None:
    pass

def test_diffTime(mocker,geo_code_mock_belgium,get_time_info_mock_belgium) -> None:
    expected_message = f'België / Belgique / Belgien is behind Россия by 5 hour(s)'
    result1 = diffTime('Belgium','Russia')[0]
    assert result1 == expected_message

@pytest.mark.skip()
def test_timeAt() -> None:
    pass