import json
import requests
from pathlib import Path

strIdUrl = None
p = Path("kyiv_districts.GeoJSON")
if not p.exists():
    raise SystemExit(f"File not found: {p}")

with p.open("r", encoding="utf-8") as f:
    data = json.load(f)

addresses = []
streetIds = []

for f in data["features"]:
    p = f.get("properties", {})
    street = p.get("addr:street")
    number = p.get("addr:housenumber")

    if street and number:
        strIdUrl = 'https://app.yasno.ua/api/blackout-service/public/shutdowns/addresses/v2/streets?regionId=25&query=вул.+' + street + '&dsoId=902'
        try:
            response = requests.get(strIdUrl)
        except Exception as e:
            print('Error occurred while sending request to ' + strIdUrl)

        print(response.ok)

        addresses.append({
            "street": street,
            "number": number,
            "id": p.get("@id")
        })

# with open("addresses.txt", "w", encoding="utf-8") as f:
#     for addr in addresses:
#         f.write(str(addr) + '\n')



print("Найдено адресов:", len(addresses))