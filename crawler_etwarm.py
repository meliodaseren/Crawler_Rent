import requests
import math
import time
import json
from bs4 import BeautifulSoup

# ----- Crawler Information ----- #
# [東森房屋 - 租屋] http://www.etwarm.com.tw/rent/object_list
# Area: 台北市、新北市
# Type: 套房 (無雅房類型)
    # 依房屋類型結果搜尋不佳，改用關鍵字(套房、雅房)
# Keyword: 套房、雅房
    # [台北市套房: 22筆] http://www.etwarm.com.tw/rent/object_list?area=台北市&keyword=套房&page=1
    # [新北市套房: 7筆] http://www.etwarm.com.tw/rent/object_list?area=新北市&keyword=套房&page=1
    # [台北市雅房: 1筆] http://www.etwarm.com.tw/rent/object_list?area=台北市&keyword=雅房&page=1
    # [新北市雅房: 2筆] http://www.etwarm.com.tw/rent/object_list?area=新北市&keyword=雅房&page=1

# index page
area_list = ['台北市', '新北市']
keyword_list = ['套房', '雅房']
index = "http://www.etwarm.com.tw/rent/object_list?area=台北市&keyword=套房&page=1"

# [流程]
# 取得總筆數 (計算頁數以便迭代)
# 取得每個房屋物件的標題 (以便除錯)
# 取得每個房屋物件的連結
    # 迭代進入每個連結，取得房屋物件的內容
# ------------------------------- #

print("--" * 20)

# Get total pages
def getTotalPages(href):
    res = requests.get(href)
    soup = BeautifulSoup(res.text, "lxml")
    totalPieces = int(soup.select('div[class="object_mode"]')[0].select('span')[0].text)
    res.close()
    # 10 house objects in each page
    totalPages = math.ceil(totalPieces / 10)
    return totalPieces, totalPages    # return tuple

totalPieces, totalPages = getTotalPages(index)
print("Total Pages: " + str(totalPages))

print("--" * 20)


# Get object information
def rent_info(href):
    try:
        time.sleep(3)
        res = requests.get(href)
        soup = BeautifulSoup(res.text, "lxml")

        data_basic = soup.select('ul[class="data_basic"] > li')
        data_len = len(data_basic)

        print("".join(data_basic[0].text.split()))

        for data in range(1, data_len - 1):
            print(data_basic[data].text.split(":")[0])
            print(data_basic[data].text.split(":")[1])

    except IndexError as e:
        print(e, href)

    finally:
        pass


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
            title = obj_info[objName].select('a')[0].text.split()
            title = str(title).lstrip('[\'').rstrip('\']')
            href = obj_info[objName].select('a')[0]['href']

            count += 1
            # Check Crawler
            print("Scraping: " + str(count) + " (" + str(page) +
                  " / " + str(totalPages) + " Pages)" + "\n")

            print(title)
            print(href)

            rent_info(href)

        time.sleep(5)

finally:
    pass


# Write JSON
def saveJson(data, fileName):
    with open(fileName, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False)


# saveJson(job_lists_dict, "Job_104_" + str(jobcat) + ".json")

# Check Crawler
print(str(totalPieces) + " Objects, " + str(totalPages) + " Pages Done.")
