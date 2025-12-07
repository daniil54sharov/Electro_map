import requests
import json
from datetime import timedelta
import time

base_url = 'https://app.yasno.ua/api/blackout-service/public/shutdowns/addresses/v2/group'
regionId = '?regionId=25&'
dsoId = '&dsoId=902'

with open('kyiv_districts.GeoJSON', 'r') as file:
    kyiv_districts_json = json.load(file)

def minutes_to_hhmm(minutes: int) -> str:
    hours, mins = divmod(minutes, 60)
    return f"{hours:02d}:{mins:02d}"

counter = 1
for feature in kyiv_districts_json['features']:
    props = feature.get('properties', {})
    yasnoStreetData = props.get('yasnoStreetData', {})
    yasnoStreetId = yasnoStreetData.get('id')
    yasnoHouseData = props.get('yasnoHouseData', {})
    yasnoHouseId = yasnoHouseData.get('id')
    streetId = '&streetId=' + str(yasnoStreetId) + '&'
    houseId = 'houseId=' + str(yasnoHouseId) + '&'

    if yasnoHouseData and yasnoStreetData:
        url = base_url + regionId + streetId + houseId + dsoId
        try:
            response = requests.get(url)
        except Exception as e:
            print('Error occurred while sending request to ' + url)

        if response.ok:
            response_json = json.loads(response.text, timeout=5)
            if response_json:
                    props['yasnoGroupData'] = {
                        'group': response_json['group'],
                        'subgroup': response_json['subgroup'],
                        'value': str(response_json['group']) + '.' + str(response_json['subgroup'])
                    }
                    print(counter, response_json)
                    counter += 1
            time.sleep(0.2)

with open('kyiv_districts.GeoJSON', 'w', encoding="utf-8") as file:
    json.dump(kyiv_districts_json, file, ensure_ascii=False, indent=2)

