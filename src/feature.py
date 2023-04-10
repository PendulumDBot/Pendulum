import json
import requests

def geocodeForward(location):
    params = {'q': location,'format':'json'}
    response = requests.get(f'https://nominatim.openstreetmap.org/search', params = params, timeout=30)
    return json.loads(response.text)[0]

def getLocationInfo(location):
    return { "LocationName" : location.get("display_name"),
                 "lat" : float(location.get("lat")),
                 "lon" : float(location.get("lon"))}

