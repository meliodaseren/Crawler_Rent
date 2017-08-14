import glob
import json
import re
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


# File list
etwarm = glob.glob("./etwarm_json/*.json")

# Extend file names to List
etwarm0 = re.findall("\.\/etwarm_json\\\\(\w+\.json)", etwarm[0])
for i in range(1, len(etwarm)):
    etwarm0.extend(re.findall("\.\/etwarm_json\\\\(\w+\.json)", etwarm[i]))

postalCode = {
    "中正區": 100, "大同區": 103, "中山區": 104, "松山區": 105, "大安區": 106, "萬華區": 108, "信義區": 110,
    "士林區": 111, "北投區": 112, "內湖區": 114, "南港區": 115, "文山區": 116, "萬里區": 207, "金山區": 208,
    "板橋區": 220, "汐止區": 221, "深坑區": 222, "石碇區": 223, "瑞芳區": 224, "平溪區": 226, "雙溪區": 227,
    "貢寮區": 228, "新店區": 231, "坪林區": 232, "烏來區": 233, "永和區": 234, "中和區": 235, "土城區": 236,
    "三峽區": 237, "樹林區": 238, "鶯歌區": 239, "三重區": 241, "新莊區": 242, "泰山區": 243, "林口區": 244,
    "蘆洲區": 247, "五股區": 248, "八里區": 249, "淡水區": 251, "三芝區": 252, "石門區": 253
}

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

        json_data = {
            "id": "NA",
            "cityID": postalCode[obj_data_route],
            "url": data["url"],
            "title":
                soup.select('div[class="obj_data_basic"]')[0].select('h1')[0].text,
            "address":
                str(re.findall('<li>地址 : (\w+)<\/li>', str(data_basic)))\
                    .lstrip("\'\[").rstrip("\'\]"),
            "pattern": "NA",
            "floor": 0,
            "stories": 0,
            "label": 0,
            "rent": 0,
            "lat": 0,
            "lng": 0,
            "sex": "NA",
            "space":
                int(''.join(re.findall('<span class="space">(\w+)坪</span>', str(data_basic)))),
            "smoke": "NA",
            "pet": 0,
            "cook": 0,
            "updateDate": data["update"],
            "landlord": "".join(soup.select('div[class="data_store"]')[0].text.split()),
            "description": soup.select('section[id="obj_characteristic"]')[0].text,
            # "description": "",
            "temp": 0
        }

    except IndexError as e:
        print(e)
        print(data["url"])

    except ValueError as e:
        print(e)
        print(data["url"])

    finally:
        saveJson(json_data, "./etwarm_json2/%s" % etwarm0[i])
        pass
