import requests
import math
import time
import json
import datetime
from bs4 import BeautifulSoup

# ----- Crawler Information ----- #
# [東森房屋租屋] http://www.etwarm.com.tw/rent/object_list
# Area: 台北市、新北市
# Keyword: 套房、雅房
# ------------------------------- #


# Write JSON
def saveJson(data, filename):
    with open(filename, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False)


# Get total pages
def getTotalPages(href):
    res = requests.get(href)
    soup = BeautifulSoup(res.text, "lxml")
    totalPieces = int(soup.select('div[class="object_mode"]')[0].select('span')[0].text)
    res.close()
    # 10 house objects in each page
    totalPages = math.ceil(totalPieces / 10)
    return totalPieces, totalPages    # return tuple


area_list = ["台北市", "新北市"]
keyword_list = ["套房", "雅房"]

# Count all objects and pages
totalPieces_all = 0
totalPages_all = 0

try:
    for area in area_list:
        for keyword in keyword_list:
            index = "http://www.etwarm.com.tw/rent/object_list?area={x}&keyword={y}&page=1"\
                    .format(x=area, y=keyword)

            print("--" * 20)
            print(str(area) + str(keyword))
            totalPieces, totalPages = getTotalPages(index)
            print("Total Pages: " + str(totalPages))
            print("--" * 20)

            totalPieces_all += totalPieces
            totalPages_all += totalPages

            try:
                for page in range(1, int(totalPages) + 1):
                    indexf = index[:-1] + "{}"
                    href = indexf.format(page)
                    res = requests.get(href)
                    soup = BeautifulSoup(res.text, "lxml")

                    # Dynamic get objects in each page
                    obj_info = soup.select('div[class="obj_info"]')
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

                        saveJson(obj_dict, "./etwarm_json/%s.json" % obj_href[-6:])

                        count += 1

                        # Check Crawler
                        print("Scraping: " + str(count) + " (" + str(page) +
                              " / " + str(totalPages) + " Pages)")

                    time.sleep(5)
            finally:
                pass
finally:
    pass


# Check Crawler
print(str(totalPieces_all) + " Objects, " + str(totalPages_all) + " Pages Done.")
