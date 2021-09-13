#код с урока

import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import json

url = 'https://rootstore.ru/'

response = requests.get(url)

#прогоним весь код через bs4, html.parser - помогает распарсить html страницы
soup = bs(response.text, 'html.parser')

#pprint(soup.prettify()) #prettify() используется для отступов

tag_a = soup.find_all('a')
pprint(tag_a[1]) #покажет только 2й
pprint(tag_a) #покажет все теги а

tag_a = soup.find('a')
div = tag_a.parent.parent
pprint(list(div.findChildren())) #возвращает всех потомков не только детей
pprint(list(div.findChildren(recursive=False))) #выключили рекурсивный обход, чтобы получить только детей

all_div_children = list(div.findChildren(recursive=False))
pprint(all_div_children[0].findNextSibling)

p = soup.find('p', attrs={'id': 'clickable'})
pprint(p)

all_p = soup.find_all('p', {'class': 'news__date'}) #при поиске 2х классов ищется только 100% совпадение
#возможен поиск по нескольким элементам, для этого перечисляем в качестве списка - .find_all('p', {'class': ['red', 'paragraph']})
pprint(all_p)

#можно искать по тексту
sixth = soup.find(text='О компании')
pprint(sixth.parent) #ищет тег через родителя текста

#сайт кинопоиска

url = 'https://www.kinopoisk.ru'
headers = {'User_agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) "
        "Gecko/20100101 Firefox/88.0"
    }
params = {'page': 1, 'quick_filters': 'serials', 'tab': 'all'}

serials_list = []
while params['page'] < 8:
    response = requests.get(url + '/popular/films', params=params, headers=headers)
    soup = bs(response.text, 'html.parser')
    serials = soup.find_all('div', {'class': 'desktop-rating-selection-film-item'})
#    pprint(len(serials))

    serials_list = serials_list
    for serial in serials:
        serial_data = {}
        info = serial.find('p', {'class': 'selection-film-item-meta__name'})
        name_serial = info.text
        url_serial = url + info.parent["href"]  # можно заменить info.parent.get('href')
        genre_serial = serial.find('span', {
            'class': 'selection-film-item-meta__meta-additional-item'}).nextSibling.text  # выбор второго такого же тега с жарном, а не страной
        # проверим значения, где нет рейтинга:
        try:
            rating_serial = float(serial.find('span', {'class': 'rating__value'}).text)
        except:
            rating_serial = None

        serial_data['name'] = name_serial
        serial_data['url'] = url_serial
        serial_data['genre'] = genre_serial
        serial_data['rating'] = rating_serial

        serials_list.append(serial_data)
        continue
    params['page'] += 1

#pprint(serials_list)
print(len(serials_list))

with open('kinopoisk.json', 'w', encoding='utf-8-sig') as f:
    json.dump(serials_list, f)