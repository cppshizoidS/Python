import requests
import random
from bs4 import BeautifulSoup

class Anime:

    def __init__(self, name, url, image):
        self.name = name
        self.url = url
        self.image = image

class Anime_data:

    def __init__(self):
        self.data = None
        self.seasons = None
        self.series = None
        self.season = None
        self.seria = None

    def set_name(self, name):
        self.name = name

    def set_data(self, data):
        self.data = data
        self.seasons = [*self.data]

    def select_season(self, name):
        if name not in self.seasons:
            return False
        self.season = name
        self.series = [*self.data[self.season]]
        return True

    def select_seria(self, name):
        if name not in self.series:
            return False
        self.seria = name
        return True

    def url(self):
        return self.data[self.season][self.seria]

class Jutsu:

    def __init__(self):
        self.url = 'https://jut.su'
        self.headers = [
            {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0'},
            {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'},
            {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0 Waterfox/91.10.0'},
            {'user-agent': 'Defined'}
        ]

    def get_all(self):
        html_text = requests.get(self.url + '/' + 'anime', headers=self.headers[3]).text
        soup = BeautifulSoup(html_text, "html.parser")
        all_anime = []
        for i in soup.find_all(class_='all_anime_global'):
            name = i.find(class_='aaname').text
            url = self.url + i.find('a', href=True)['href']
            image_string = i.find(class_='all_anime_image')['style']
            image = image_string[image_string.find('\'') + 1 : image_string.rfind('\'')]
            all_anime.append(Anime(name, url, image))
        while soup.find(class_='vnright'):
            next = self.url + soup.find(class_='vnright')['href']
            html_text = requests.get(next, headers=self.headers[random.randint(0, 2)]).text
            soup = BeautifulSoup(html_text, "html.parser")
            for i in soup.find_all(class_='all_anime_global'):
                name = i.find(class_='aaname').text
                url = self.url + i.find('a', href=True)['href']
                image_string = i.find(class_='all_anime_image')['style']
                image = image_string[image_string.find('\'') + 1 : image_string.rfind('\'')]
                all_anime.append(Anime(name, url, image))
        return all_anime

    def get_data(self, url):
        html_text = requests.get(url, headers=self.headers[3]).text
        soup = BeautifulSoup(html_text, "html.parser")
        if not soup.find('h1', class_='header_video'):
            return None
        data = {}
        for i in soup.find_all(class_='short-btn'):
            text = i.text.split()
            for j in range(len(text) - 1):
                if text[j].isnumeric() and text[j + 1] == 'сезон':
                    index = text[j] + ' ' + text[j + 1]
                    if not data.get(index):
                        data[index] = {}
                    subindex = text[j + 2] + ' ' + text[j + 3]
                    data[index][subindex] = self.url + i['href']
                    break
                elif text[j].isnumeric() and text[j + 1] == 'фильм':
                    if not data.get('Фильмы'):
                        data['Фильмы'] = {}
                    subindex = text[j] + ' ' + text[j + 1]
                    data['Фильмы'][subindex] = self.url + i['href']
                    break
                elif text[j].isnumeric() and text[j + 1] == 'серия':
                    if not data.get('Серии'):
                        data['Серии'] = {}
                    subindex = text[j] + ' ' + text[j + 1]
                    data['Серии'][subindex] = self.url + i['href']
                    break
        return data
