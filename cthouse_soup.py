import glob
import json
import re
from bs4 import BeautifulSoup

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


# File list
cthouse = glob.glob('./cthouse_json/*.json')

# Extend file names to List
cthouse0 = re.findall('\.\/cthouse_json\\\\(\w+\.json)', cthouse[0])
for i in range(1, len(cthouse)):
    cthouse0.extend(re.findall('\.\/cthouse_json\\\\(\w+\.json)', cthouse[i]))

for i in range(0, len(cthouse0)):
    soup = BeautifulSoup(readData(cthouse0[i])["html"], "lxml")

json_data = {
    "id": ,
    "cityID": ,
    "url": ,
    "title": ,
    "address": ,
    "pattern": ,
    "floor": ,
    "stories": ,
    "label": ,
    "rent": ,
    "lat": ,
    "lng": ,
    "sex": ,
    "space": ,
    "smoke": ,
    "pet": ,
    "cook": ,
    "updateDate": ,
    "landlord": ,
    "description": ,
    "temp":
}
