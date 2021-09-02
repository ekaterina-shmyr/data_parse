#код с урока
from lxml import html
from pprint import pprint
import requests

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}

responce = requests.get('https://ru.ebay.com/b/Fishing-Equipment-Supplies/1492/bn_1851047', headers=headers)

dom = html.fromstring(responce.text)

items = dom.xpath('//li[contains(@class, "s-item")]')

item_list = []
for item in items:
    items_data = {}
    names = item.xpath('.//h3[@class="s-item__title"]/text()') #получаем названия в текущей директории
    links = item.xpath('.//h3[@class="s-item__title"]/../@href') #получаем ссылки
    prices = str(item.xpath('.//span[@class="s-item__price"]//text()')).replace('\\xa0', '')  #проверим все вложенные элементы
    info = item.xpath('.//span[contains(@class, "s-item__hotness")]//text()')

    items_data['names'] = names
    items_data['links'] = links
    items_data['prices'] = prices
    items_data['info'] = info

    item_list.append(items_data)

pprint(item_list)