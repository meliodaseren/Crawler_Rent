import requests
import math
import time
import json
import re
import datetime
from bs4 import BeautifulSoup

# ----- Crawler Information ----- #
# [中信房屋好神租] http://rent.cthouse.com.tw/
# Area: 台北市、新北市
# Type: 獨立套房、分租套房、雅房
# ------------------------------- #


# Write JSON
def saveJson(data, filename):
    with open(filename, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False)


# Get total pages
def getTotalPages(href):
    res = requests.get(href)
    soup = BeautifulSoup(res.text, "lxml")
    totalPieces = int(soup.select('div[class="searchResult__num"]')[0].select('b')[0].text)
    res.close()
    # 10 house objects in each page
    totalPages = math.ceil(totalPieces / 20)
    return totalPieces, totalPages    # return tuple


area_list = ["臺北市", "新北市"]

# Count all objects and pages
totalPieces_all = 0
totalPages_all = 0

try:
    for area in area_list:
        index = "http://rent.cthouse.com.tw/area/{x}-city/獨立套房-分租套房-雅房-use/"\
                .format(x=area)

        print("--" * 20)
        print(str(area))
        totalPieces, totalPages = getTotalPages(index)
        print("Total Pages: " + str(totalPages))
        print("--" * 20)

        totalPieces_all += totalPieces
        totalPages_all += totalPages

        res = requests.get(index)
        soup = BeautifulSoup(res.text, "lxml")

        # Dynamic get objects in each page
        obj_info = soup.select('div[class="item__intro"]')
        totalObj = len(obj_info)

        count = 0

        for objName in range(0, totalObj):
            # title = obj_info[objName].select('a')[0].text.split()
            # title = str(title).lstrip('[\'').rstrip('\']')
            obj_href = obj_info[objName].select('a')[0]['href']

            # create dictionary to export JSON
            obj_dict = {
                "url": obj_href,
                "html": requests.get(obj_href).text,
                "update": datetime.datetime.now().strftime("%Y-%m-%d"),
            }

            objId = str(re.findall('(\w\d{7})', obj_href)).lstrip('[\'').rstrip('\']')
            saveJson(obj_dict, "./cthouse_json/%s.json" % objId)

            count += 1

            # Check Crawler
            print("Scraping: " + str(count) + " (" + "1" +
                  " / " + str(totalPages) + " Pages)")

        time.sleep(5)
finally:
    pass


# Check Crawler
print(str(totalPieces_all) + " Objects, " + str(totalPages_all) + " Pages Done.")
