from selenium import webdriver
from bs4 import BeautifulSoup
from selenium import webdriver

list_of_animals = []

driver = webdriver.Firefox()
driver.get(
    "https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&pageuntil=%D0%90%D0%B7%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F+%D0%BF%D1%83%D0%B3%D0%BE%D0%BB%D0%BE%D0%B2%D0%BA%D0%B0#mw-pages")
page = driver.page_source
h3 = BeautifulSoup(page, 'html.parser').find('div', class_='mw-category-group').find('h3').text
try:
    while h3 != 'Я':
        driver.find_element_by_partial_link_text("Следующая страница").click()
        page = driver.page_source
        h3 = BeautifulSoup(page, 'html.parser').find('div', class_='mw-category-group').find('h3').text
        for word in BeautifulSoup(page, 'html.parser').find('div', class_='mw-category-group').findAll('li'):
            list_of_animals.append(word.text)

except:
    pass

word_count = {k: 0 for k in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ'}
for name in list_of_animals:
    word_count[name[0]] += 1

print(word_count)
