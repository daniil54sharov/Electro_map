import json
import requests
import re
import time

baseUrl = 'https://app.yasno.ua/api/blackout-service/public/shutdowns/addresses/v2/streets'
regionId = '?regionId=25&'
dsoId = '&dsoId=902'

with open('kyiv_districts.GeoJSON', 'r') as file:
    kyiv_districts_json = json.load(file)

def prepare_address(address: str) -> str:
    s = address.lower().strip()
    s = re.sub(r'\b(вулиця|вул\.?|шосе|проспект|пр-т|просп\.?|провулок|пров\.?)\b', '', s)
    s = re.sub(r'\b\d+[-–]?[а-яіїєґA-Za-z]*\b', '', s)
    s = re.sub(r'[+\-_\.]', ' ', s)
    s = " ".join(s.split())

    return s.replace(' ', '+')

counter = 1
for feature in kyiv_districts_json['features']:
    props = feature.get('properties', {})
    street = props.get('addr:street')

    if street:
        url = baseUrl + regionId + 'query=' + prepare_address(street) + dsoId
        try:
            response = requests.get(url, timeout=5)
        except Exception as e:
            print('Error occurred while sending request to ' + url)
        if response.ok:
            response_json = json.loads(response.text)
            if response_json:
                props['yasnoStreetData'] = {
                    'id': response_json[0]['id'],
                    'value': response_json[0]['value']
                }
                print(counter, response_json)
                counter += 1
        time.sleep(0.5)
with open('kyiv_districts.GeoJSON', 'w', encoding="utf-8") as file:
    json.dump(kyiv_districts_json, file, ensure_ascii=False, indent=2)