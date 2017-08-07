import requests
import math
import time
from bs4 import BeautifulSoup

# ----- Crawler Information ----- #
# [中信房屋好神租] http://rent.cthouse.com.tw/
# Area: 台北市、新北市
# Type: 獨立套房、分租套房、雅房
    # [台北市套房] http://rent.cthouse.com.tw/area/臺北市-city/獨立套房-分租套房-雅房-use/
    # [新北市套房] http://rent.cthouse.com.tw/area/新北市-city/獨立套房-分租套房-雅房-use/
# ------------------------------- #


# Read Data, and convert list of string to list to set
def readData(filename):
    try:
        with open(filename, "rt", encoding="utf-8") as f:
            data = set(f.read().lstrip('{\'').rstrip('\'}').split('\', \''))
            f.close()
            return data
    except FileNotFoundError as e:
        # If file not found, return empty set
        data = set()
        return data


# Get total pages
def getTotalPages(href):
    res = requests.get(href)
    soup = BeautifulSoup(res.text, "lxml")
    totalPieces = int(soup.select('div[class="searchResult__num"]')[0].select('b')[0].text)
    res.close()
    # 20 house objects in each page
    totalPages = math.ceil(totalPieces / 20)
    return totalPieces, totalPages    # return tuple


href_set = readData("cthouse_set.txt")

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
            href = obj_info[objName].select('a')[0]['href']

            count += 1

            # Check Crawler
            print("Scraping: " + str(count) + " (" + "1" +
                  " / " + str(totalPages) + " Pages)")

            # Check if url exists in set
            if href in href_set:
                print("Pass: " + href + "\n")
                pass
            else:
                print("Update: " + href + "\n")
                href_set.add(href)

        time.sleep(5)
finally:
    pass


# Write Data
def saveData(data, filename):
    with open(filename, "w") as f:
        f.write(data)

# print(href_list)
saveData(str(href_set), "cthouse_set.txt")

# Check Crawler
print(str(totalPieces_all) + " Objects, " + str(totalPages_all) + " Pages Done.")
