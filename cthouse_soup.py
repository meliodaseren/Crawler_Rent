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

for i in range(0, len(cthouse0)):

    try:
        data = readData(cthouse0[i])

        soup = BeautifulSoup(readData(cthouse0[i])["html"], "lxml")

        json_data = {
            "id": "NA",
            "cityID": postalCode[],
            "url": data["url"],
            "title": "",
            "address": "",
            "pattern": "NA",
            "floor": 0,
            "stories": 0,
            "label": 0,
            "rent": 0,
            "lat": 0,
            "lng": 0,
            "sex": "NA",
            "space": 0,
            "smoke": "NA",
            "pet": 0,
            "cook": 0,
            "updateDate": data["update"],
            "landlord": "",
            "description": "",
            "temp": 0
        }

    except IndexError as e:
        print(e)
        print(data["url"])

    except ValueError as e:
        print(e)
        print(data["url"])

    finally:
        saveJson(json_data, "./cthouse_json2/%s" % cthouse0[i])
        pass
