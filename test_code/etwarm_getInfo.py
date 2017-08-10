import requests
import time
import json
from bs4 import BeautifulSoup

# ----- Crawler Information ----- #
# [東森房屋租屋] http://www.etwarm.com.tw/rent/object_list

# [流程]
# 取得每個房屋物件的連結
    # 迭代進入每個連結，取得房屋物件的內容
# ------------------------------- #


# Read Data List
def readDataList(fileName):
    try:
        with open(fileName, "rt", encoding="utf-8") as f:
            data = f.read().lstrip('{\'').rstrip('\'}').split('\', \'')
            f.close()
            return data
    except FileNotFoundError as e:
        print(e)


href_list = readDataList("etwarm_set.txt")
print(href_list)

# Get HTML and System time
try:
    for href in href_list:
        res = requests.get(href)
        with open('./etwarm_html/%s.html' % href[-6:], 'w', encoding='utf-8') as f:
            f.write(res.text)
    time.sleep(3)
finally:
    pass


# -------------------------------------------------- #

# Write JSON
def saveJson(data, filename):
    with open(filename, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False)

# saveJson(job_lists_dict, "Job_104_" + str(jobcat) + ".json")

# Get object information
def getInfo(href):
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


# try:
#     for href in href_list:
#         res = requests.get(href)
#         soup = BeautifulSoup(res.text, "lxml")
#         rent_info(href)
#         print()
#
#     time.sleep(3)
# finally:
#     pass
