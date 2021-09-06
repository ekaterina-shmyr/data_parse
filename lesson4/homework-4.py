"""
Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости. Для парсинга использовать XPath. Структура данных должна содержать:
    название источника;
    наименование новости;
    ссылку на новость;
    дата публикации.
Сложить собранные данные в БД
"""
#Сделала сбор новостей по lenta.ru и news.mail.ru

from lxml import html
from pprint import pprint
import requests
from pymongo import MongoClient

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}

client = MongoClient('127.0.0.1', 27017)
db = client['news_092021']

#Lenta.ru

url = 'https://lenta.ru'
responce = requests.get(url, headers=headers)

dom = html.fromstring(responce.text)
news = dom.xpath('//div[@class="item"]')

news_list = db.news_list
for item in news:
    news_data = {}
    names = str(item.xpath('./a/text()')).replace('\\xa0', '')
    links = str(item.xpath('./a/@href')).replace("['", '')

#часть главных новостей была без даты, поэтому поставила там значения None
    try:
        data = item.xpath('.//time[@class="g-time"]/@datetime')
    except:
        data = None

    news_data['names'] = names
    news_data['links'] = (url + links).replace("']", '')
    news_data['data'] = data
    news_data['source'] = url

    news_list.update_one({'links': news_data['links']}, {'$set': news_data}, upsert=True)

#news.mail.ru

url_2 = 'https://news.mail.ru'

responce_2 = requests.get(url_2, headers=headers)

dom = html.fromstring(responce_2.text)
links_main = dom.xpath('.//td[contains(@class, "daynews")]/div/a/@href')
links_item = dom.xpath('.//li[@class="list__item"][position()<=6]/a/@href')

mail_links = links_main + links_item


for item in mail_links:
    responce_links = requests.get(item, headers=headers)
    dom_links = html.fromstring(responce_links.text)
    news_data = {}
    names = str(dom_links.xpath('.//h1[@class="hdr__inner"]/text()')).replace('\\xa0', '')
    links = item
    data = dom_links.xpath('.//span[@class="note"]/span/@datetime')
    source = dom_links.xpath('.//span[@class="note"]/a/@href')

    news_data['names'] = names
    news_data['links'] = links
    news_data['data'] = data
    news_data['source'] = source

    news_list.update_one({'links': news_data['links']}, {'$set': news_data}, upsert=True)
