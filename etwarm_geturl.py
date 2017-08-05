import requests
import math
import time
from bs4 import BeautifulSoup

# ----- Crawler Information ----- #
# [東森房屋 - 租屋] http://www.etwarm.com.tw/rent/object_list
# Area: 台北市、新北市
# Type: 套房 (無雅房類型)
    # 依房屋類型結果搜尋不佳，改用關鍵字(套房、雅房)
# Keyword: 套房、雅房

# [流程]
# 取得總筆數 (計算頁數以便迭代)
# 取得每個房屋物件的標題 (以便除錯)
# 取得每個房屋物件的連結
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
    totalPieces = int(soup.select('div[class="object_mode"]')[0].select('span')[0].text)
    res.close()
    # 10 house objects in each page
    totalPages = math.ceil(totalPieces / 10)
    return totalPieces, totalPages    # return tuple


href_set = readData("etwarm_set.txt")

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
                        href = obj_info[objName].select('a')[0]['href']

                        count += 1

                        # Check Crawler
                        print("Scraping: " + str(count) + " (" + str(page) +
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
finally:
    pass


# Write Data
def saveData(data, filename):
    with open(filename, "w") as f:
        f.write(data)

# print(href_list)
saveData(str(href_set), "etwarm_set.txt")

# Check Crawler
print(str(totalPieces_all) + " Objects, " + str(totalPages_all) + " Pages Done.")
