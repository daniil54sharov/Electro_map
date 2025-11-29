import requests
import json
from datetime import timedelta

url = 'https://app.yasno.ua/api/blackout-service/public/shutdowns/regions/25/dsos/902/planned-outages'
blackout_schedule = [[0 for _ in range(24)] for _ in range(12)]

def minutes_to_hhmm(minutes: int) -> str:
    hours, mins = divmod(minutes, 60)
    return f"{hours:02d}:{mins:02d}"


try:
    response = requests.get(url)
except Exception as e:
    print('Error occurred while sending request to ' + url)
slots_index = 0

if response.ok:
    data = json.loads(response.text)
    for group in data:
        for slots_items in data[str(group)]['today']['slots']:
            start_time = data[str(group)]['today']['slots'][slots_index]['start']
            end_time = data[str(group)]['today']['slots'][slots_index]['end']
            type = data[str(group)]['today']['slots'][slots_index]['type']
            print(group,
            'start : ', minutes_to_hhmm(minutes=start_time), ',',
            'end : ', minutes_to_hhmm(minutes=end_time), ',',
            'type : ', type)
            if slots_index < len(data[str(group)]['today']['slots']):
                slots_index += 1
        print('\n')
        slots_index = 0

