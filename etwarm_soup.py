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
etwarm = glob.glob('./etwarm_json/*.json')

# Extend file names to List
etwarm0 = re.findall('\.\/etwarm_json\\\\(\w+\.json)', etwarm[0])
for i in range(1, len(etwarm)):
    etwarm0.extend(re.findall('\.\/etwarm_json\\\\(\w+\.json)', etwarm[i]))

for i in range(0, len(etwarm0)):
    soup = BeautifulSoup(readData(etwarm0[i])["html"], "lxml")



