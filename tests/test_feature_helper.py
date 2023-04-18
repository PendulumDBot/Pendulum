import pytest
from src.featurehelper import geocodeForward, getLocationInfo, findTimezone, getTimeInfo, arrowFromWindDirection

arrowList = [
    (275,'→'),(23,'↓'),(270,'→'),(120,'←'),
    (55,'↙'),(65,'↙'),(150,'↖'),(200,'↑'),
    (235,'↗'),(320,'↘'),(100,'←')
    ]

@pytest.mark.parametrize("input, out", arrowList)
def test_arrowFromWindDirection(input, out) -> None:
    assert arrowFromWindDirection(input) == out

def test_geocodeForward() -> None:
    pass