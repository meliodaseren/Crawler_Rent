import glob
import json
import re
import requests
from bs4 import BeautifulSoup


# Read Data List
def readData(fileName):
    try:
        with open("./etwarm_json/" + fileName, "rt", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except FileNotFoundError as e:
        print(e)


# Write JSON
def saveJson(data, filename):
    with open(filename, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False)


# Use Google API to get postal code, lat, lng
api_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key="

def getLocation(address):
    url = api_url.format(address)
    res = requests.get(url)
    location_dict = res.json()
    cityID = location_dict['results'][0]['address_components'][-1]['short_name']
    lat = location_dict['results'][0]['geometry']['location']['lat']
    lng = location_dict['results'][0]['geometry']['location']['lng']
    res.close()
    return cityID, lat, lng


# File list
etwarm = glob.glob("./etwarm_json/*.json")

# Extend file names to List
etwarm0 = re.findall("\.\/etwarm_json\\\\(\w+\.json)", etwarm[0])
for i in range(1, len(etwarm)):
    etwarm0.extend(re.findall("\.\/etwarm_json\\\\(\w+\.json)", etwarm[i]))

booleanDict = {
    "可以": "Y", "不可以": "N", "無": "N"
}

for i in range(0, len(etwarm0)):

    try:
        data = readData(etwarm0[i])
        soup = BeautifulSoup(data["html"], "lxml")

        obj_data_route = soup.select('div[class="obj_data_route"]')[0]\
                             .select('a')[2].text.lstrip().rstrip()
        data_basic = soup.select('ul[class="data_basic"]')[0].findAll('li')

        address = str(re.findall('<li>地址 : (\w+)<\/li>', str(data_basic))).lstrip("\'\[").rstrip("\'\]")
        cityID, lat, lng = getLocation(address)

        try:
            space = float(''.join(re.findall('<span class="space">(\w+)坪</span>', str(data_basic))))
        except:
            "NA"

        try:
            landlord = soup.select('section[id="obj_characteristic"]')[0].text
        except:
            "NA"

        try:
            description = soup.select('section[id="obj_characteristic"]')[0].text
        except:
            "NA"

        json_data = {
            "id": "NA",
            "cityID": cityID,
            "url": data["url"],
            "title":
                soup.select('div[class="obj_data_basic"]')[0].select('h1')[0].text,
            "address": address,
            "pattern": "NA",
            "floor": 0,
            "stories": 0,
            "label": 0,
            "rent": 0,
            "lat": lat,
            "lng": lng,
            "sex": "A",
            "space": space,
            "smoke": "NA",
            "pet": "N",
            "cook": "N",
            "updateDate": data["update"],
            "landlord": landlord,
            "description": description,
            "temp": "Y"
        }

        saveJson(json_data, "./etwarm_json2/%s" % etwarm0[i])

    except IndexError as e:
        print(e)
        print(etwarm0[i])

    except ValueError as e:
        print(e)
        print(etwarm0[i])
