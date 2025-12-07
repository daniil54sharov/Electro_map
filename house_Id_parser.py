import json
import requests
import re
import time

baseUrl = 'https://app.yasno.ua/api/blackout-service/public/shutdowns/addresses/v2/houses'
regionId = '?regionId=25&'
dsoId = '&dsoId=902'

with open('kyiv_districts.GeoJSON', 'r') as file:
    kyiv_districts_json = json.load(file)

def prepare_housenumber(housenumber: str) -> str:
    s = housenumber.upper().strip()
    return s.replace('-', '')

counter = 1
for feature in kyiv_districts_json['features']:
    props = feature.get('properties', {})
    yasnoData = props.get('yasnoStreetData', {})
    yasnoStreetId = yasnoData.get('id')
    houseNumber = props.get('addr:housenumber')
    streetId = '&streetId=' + str(yasnoStreetId) + '&'

    if houseNumber and yasnoStreetId:
        url = baseUrl + regionId + streetId + 'query=' + prepare_housenumber(houseNumber) + dsoId
        try:
            response = requests.get(url, timeout=5)
        except Exception as e:
            print('Error occurred while sending request to ' + url)
        if response.ok:
            response_json = json.loads(response.text)
            if response_json:
                    props['yasnoHouseData'] = {
                        'id': response_json[0]['id'],
                        'value': response_json[0]['value']
                    }
                    print(counter, response_json)
                    counter += 1
    time.sleep(0.2)
with open('kyiv_districts.GeoJSON', 'w', encoding="utf-8") as file:
    json.dump(kyiv_districts_json, file, ensure_ascii=False, indent=2)