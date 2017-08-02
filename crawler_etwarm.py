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


# create dictionary to export JSON
# job_lists_dict = {
#     "lists_url": index,
#     "total_pages": totalPages,
#     "lists_title": pageTitle,
#     "job_lists": []
# }


# The function to get job information
# def job_info(href):
#     try:
#         time.sleep(3)
#         res = requests.get(href)
#         soup = BeautifulSoup(res.text, "html5lib")  # Error lxml, html.parser

#         if soup.select('head > title') != "104人力銀行─錯誤頁":
#             job_company = soup.select('a')[1].text
#             job_content = soup.select('div[class="content"] > p')[0].text
#             job_uptime = soup.select('time[class="update"]')[0].text

#             reqs = soup.find_all(['dt', 'dd'])
#             job_tools = ""
#             job_skills = ""
#             other_con = ""

#             for i in range(0, len(reqs) - 1):
#                 if "擅長工具" in reqs[i].text:
#                     job_tools += reqs[i + 1].text
#                 elif "工作技能" in reqs[i].text:
#                     job_skills += reqs[i + 1].text
#                 elif "其他條件" in reqs[i].text:
#                     other_con += reqs[i + 1].text

#             job_info_dict = {
#                 "company": job_company,
#                 "content": job_content,
#                 "tools": job_tools,
#                 "skills": job_skills,
#                 "post_date": job_uptime,
#                 "other_condition": other_con
#             }

#             return job_info_dict

#         else:
#             print("404 Not Found")

#     except IndexError as e:
#         print(e, href)

#     else:
#         print("Other Exception: " + href)

#     finally:
#         pass

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

            print(title)
            print(href)

            count += 1
            # Check Crawler
            print("Scraping: " + str(count) + " (" + str(page) +
                  " / " + str(totalPages) + " Pages)" + "\n")

        time.sleep(5)

finally:
    pass


# The function to write JSON data
# def saveJson(data, fileName):
#     with open(fileName, "w", encoding="utf8") as f:
#         json.dump(data, f, ensure_ascii=False)
#
#
# saveJson(job_lists_dict, "Job_104_" + str(jobcat) + ".json")

# Check Crawler
print(str(totalPieces) + " Objects / " + str(totalPages) + " Pages Done.")
