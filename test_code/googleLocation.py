import requests

api_url= "https://maps.googleapis.com/maps/api/geocode/json?address={}&key="

def getLocation(address):
    url = api_url.format(address)
    res = requests.get(url)
    location_dict = res.json()
    lat = location_dict['results'][0]['geometry']['location']['lat']
    lng = location_dict['results'][0]['geometry']['location']['lng']
    cityID = location_dict['results'][0]['address_components'][-1]['short_name']
    res.close()
    return lat, lng, cityID

lat, lng, cityID = getLocation("新北市三重區介壽路39巷")

print(lat)
print(lng)
print(cityID)

postalCode = {
    "中正區": 100, "大同區": 103, "中山區": 104, "松山區": 105, "大安區": 106, "萬華區": 108, "信義區": 110,
    "士林區": 111, "北投區": 112, "內湖區": 114, "南港區": 115, "文山區": 116, "萬里區": 207, "金山區": 208,
    "板橋區": 220, "汐止區": 221, "深坑區": 222, "石碇區": 223, "瑞芳區": 224, "平溪區": 226, "雙溪區": 227,
    "貢寮區": 228, "新店區": 231, "坪林區": 232, "烏來區": 233, "永和區": 234, "中和區": 235, "土城區": 236,
    "三峽區": 237, "樹林區": 238, "鶯歌區": 239, "三重區": 241, "新莊區": 242, "泰山區": 243, "林口區": 244,
    "蘆洲區": 247, "五股區": 248, "八里區": 249, "淡水區": 251, "三芝區": 252, "石門區": 253
}
