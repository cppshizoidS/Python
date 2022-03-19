import requests
from bs4 import BeautifulSoup as BS

page = 1

while True:
    r = requests.get("https://stopgame.ru/review/new/izumitelno/p1" + str(page))
    html = BS(r.content, 'html.parser')
    items = html.select(".items > .article-summary")

    if (len(items)):
        for el in items:
            title = el.select('.caption > a')
            print(title[0].text)
        page += 1
    else:
        break
