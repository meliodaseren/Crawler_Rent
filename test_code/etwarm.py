import requests
import math
import time
import json
from bs4 import BeautifulSoup

# ----- Crawler Information ----- #
# [東森房屋 - 租屋] http://www.etwarm.com.tw/rent/object_list

# [流程]
# 取得每個房屋物件的連結
    # 迭代進入每個連結，取得房屋物件的內容
# ------------------------------- #


# Get total pages
def getTotalPages(href):
    res = requests.get(href)
    soup = BeautifulSoup(res.text, "lxml")
    totalPieces = int(soup.select('div[class="object_mode"]')[0].select('span')[0].text)
    res.close()
    # 10 house objects in each page
    totalPages = math.ceil(totalPieces / 10)
    return totalPieces, totalPages    # return tuple


# Get object information
def rent_info(href):
    try:
        time.sleep(3)
        res = requests.get(href)
        soup = BeautifulSoup(res.text, "lxml")

        data_basic = soup.select('ul[class="data_basic"] > li')
        data_len = len(data_basic)

        print("租金 : " + "".join(data_basic[0].text.split()))

        for data in range(1, data_len - 1):
            print(data_basic[data].text.split(":")[0] + ":" +
                  data_basic[data].text.split(":")[1])

    except IndexError as e:
        print(e, href)

    finally:
        pass


area_list = ["台北市", "新北市"]
keyword_list = ["套房", "雅房"]

try:
    for area in area_list:
        for keyword in keyword_list:
            index = "http://www.etwarm.com.tw/rent/object_list?area={x}&keyword={y}&page=1"\
                    .format(x=area, y=keyword)

            print("--" * 20)
            print(str(area) + str(keyword))
            totalPieces, totalPages = getTotalPages(index)
            print("Total Pages: " + str(totalPages))
            print("--" * 20 + "\n")

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
                              " / " + str(totalPages) + " Pages)")
                        print(title)
                        print(href)

                        rent_info(href)
                        print()

                    time.sleep(5)
            finally:
                pass
finally:
    pass


# Write JSON
def saveJson(data, fileName):
    with open(fileName, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False)

# saveJson(job_lists_dict, "Job_104_" + str(jobcat) + ".json")

# Check Crawler
print(str(totalPieces) + " Objects, " + str(totalPages) + " Pages Done.")
