import glob
import json
import re
import requests
from bs4 import BeautifulSoup

''' Warning: Need to Refactor a Code '''

# Read Data List
def readData(fileName):
    try:
        with open('./cthouse_json/' + fileName, "rt", encoding="utf-8") as f:
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
cthouse = glob.glob('./cthouse_json/*.json')

# Extend file names to List
cthouse0 = re.findall('\.\/cthouse_json\\\\(\w+\.json)', cthouse[0])
for i in range(1, len(cthouse)):
    cthouse0.extend(re.findall('\.\/cthouse_json\\\\(\w+\.json)', cthouse[i]))

# booleanDict = {
#     "可以": "Y", "不可以": "N", "無": "N"
# }

for i in range(0, len(cthouse0)):

    try:
        data = readData(cthouse0[i])
        soup = BeautifulSoup(readData(cthouse0[i])["html"], "lxml")

        address = soup.select('p[class="house__add"]')[0].text
        cityID, lat, lng = getLocation(address)

        house__introRow = soup.select('div[class="house__introRow"]')[0].text
        # space = float(str(re.findall('(\d+.?\d*)\s坪', house__introRow)).lstrip('[\'').rstrip('\']'))
        space = float(''.join(re.findall('(\d+.?\d*)\s坪', house__introRow)))

        json_data = {
            "cityID": cityID,
            "url": data["url"],
            "title": soup.select('h2[class="house__id"]')[0].text,
            "address": address,
            "pattern": "水泥",
            "floor": "NA",
            "stories": "NA",
            "label": "套",
            "rent": int(soup.select('div[class="item__td"]')[0]
                            .select('span[class="txt1"]')[0]
                            .text.replace(',', '')),
            "lat": lat,
            "lng": lng,
            "sex": "A",
            "space": space,
            "smoke": "N",
            "pet": "N",
            "cook": "N",
            "update": data["update"],
            "landlord": "NA",
            "description": str(''.join(soup.select('div[class="detail__foreword"]')[0]
                                       .text.split())),
            "temp": "NA"
        }

        saveJson(json_data, "./cthouse_json2/%s" % cthouse0[i])

    except IndexError as e:
        print(e)
        print(cthouse0[i])

    except ValueError as e:
        print(e)
        print(cthouse0[i])
