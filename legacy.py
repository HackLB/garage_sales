#!/usr/bin/env python
import os, sys
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import simplejson as json
import hashlib

from geopy.geocoders import Nominatim, GoogleV3
from geopy.exc import GeocoderTimedOut


with open('../secrets.json') as f:    
    secrets = json.load(f)

geolocator = GoogleV3(api_key=secrets['google_api_key'])

url = 'https://wwwbitprod1.longbeach.gov/GarageSalePermit/SearchByDate.aspx'


def geocode(address):
    try:
        location = geolocator.geocode(address, timeout=2)
        if location:
            data = {"latitude": location.latitude, "longitude": location.longitude, "address": location.address}
            print(data)
            return data
        else:
            return None
    except GeocoderTimedOut:
        return geocode(address)
        

def geocode_old_record(path):
    if os.path.exists(path):
        with open(path) as f:    
            data = json.load(f)

        address = '{}, Long Beach, CA'.format(data['location'])

        geocoded_location = geocode(address)
        data['coordinates'] = geocoded_location
        pprint(data)
        with open(path, 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False, sort_keys=True)
        return True

    else:
        return False


if __name__ == "__main__":
    repo_path = os.path.dirname(os.path.realpath(sys.argv[0])) # Path to current directory
    data_path = os.path.join(repo_path, '_data')               # Root path for record data
    
    for directory, directories, files in os.walk(data_path, topdown=False):
        for name in files:
            if name.endswith('.json'):
                path = os.path.join(directory, name)
                geocode_old_record(path)

