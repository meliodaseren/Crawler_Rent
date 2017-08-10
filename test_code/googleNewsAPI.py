import requests
from bs4 import BeautifulSoup

# key = 'cac37ef210cc434c9bfaa39c502a6a68'

res = requests.get('https://newsapi.org/v1/articles?source=google-news&sortBy=top&apiKey=cac37ef210cc434c9bfaa39c502a6a68')
soup = BeautifulSoup(res.text, "lxml")

print(res.text)

print("--" * 50)

print(soup)