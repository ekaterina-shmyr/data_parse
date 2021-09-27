# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst   # Подключаемые обработчики

def process_price(value):          # Функция для обработки цен
    value = value.replace('\xa0', '')
    try:
        return int(value)
    except:
        return value

class AvitoparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())           # Теперь у поля есть обработчики
    price = scrapy.Field(input_processor=MapCompose(process_price), output_processor=TakeFirst())
    photos = scrapy.Field()
    url = scrapy.Field()
