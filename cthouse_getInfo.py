import requests
import time
import json
import re
from bs4 import BeautifulSoup

# ----- Crawler Information ----- #
# [中信房屋好神租] http://rent.cthouse.com.tw/
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


href_list = readDataList("cthouse_set.txt")
print(href_list)

# Get HTML and System time
try:
    for href in href_list:
        res = requests.get(href)
        objId = str(re.findall('(\w\d{7})', href)).lstrip('[\'').rstrip('\']')
        with open('./cthouse_html/%s.html' % objId, 'w', encoding='utf-8') as f:
            f.write(res.text)
    time.sleep(3)
finally:
    pass


# Write JSON
def saveJson(data, filename):
    with open(filename, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False)

# saveJson(job_lists_dict, "Job_104_" + str(jobcat) + ".json")
