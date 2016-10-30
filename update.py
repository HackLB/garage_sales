#!/usr/bin/env python
import os, sys
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import simplejson as json
import hashlib


url = 'https://wwwbitprod1.longbeach.gov/GarageSalePermit/SearchByDate.aspx'


def getmd5(message):    
    """
    Returns MD5 hash of string passed to it.
    """
    return hashlib.md5(message.encode('utf-8')).hexdigest()


def scrape_records():
    """
    Extracts garage sale records from the city garage sale Web page,
    then puts each record into a dictionary and returns a list of dictionaries.
    """
    print('Getting garage sales data...')
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    rows = soup.find('table', {'class': 'DataWebControlStyle'}).find_all('tr')
    records = []
    for row in rows[1:]:
        cells = row.find_all('td')
        location = cells[0].string.strip()
        dates = [cells[1].string.strip()]

        record = {'location': location, 'dates': dates}
        records.append(record)
        pprint(record)

    return records


def get_subdirectory(base_name):
    """
    Takes the base filename and returns a path to a subdirectory, creating it if needed.
    """
    sub_dir = os.path.join(data_path, base_name[-8:-6], base_name[-6:-4], base_name[-4:-2])
    os.makedirs(sub_dir, exist_ok=True)
    return sub_dir


def save_records(records):
    """
    Saves records to invidual JSON files.
    Records are per-address. Each new garage sale for 
    a given address gets appended to its existing file.
    Files are named and organized based on an MD5 of 
    the address.
    """
    print('Saving garage sales data...')
    for record in records:

        location_hash = getmd5(record['location'])
        file_name = '{}.json'.format(location_hash)
        directory = get_subdirectory(location_hash)

        path = os.path.join(directory, file_name)

        if os.path.exists(path):
            with open(path) as f:    
                existing_data = json.load(f)

            if record['dates'][0] not in existing_data['dates']:
                existing_data['dates'].extend(record['dates'])
            save_data = existing_data

        else:
            save_data = record
            
        with open(path, 'w') as f:
            json.dump(save_data, f, indent=4, ensure_ascii=False, sort_keys=True)



if __name__ == "__main__":
    repo_path = os.path.dirname(os.path.realpath(sys.argv[0])) # Path to current directory
    data_path = os.path.join(repo_path, '_data')               # Root path for record data
    os.makedirs(data_path, exist_ok=True)

    records = scrape_records()                  # Scrape garage sale records...
    save_records(records)                       # Save the scraped records to JSON files...

