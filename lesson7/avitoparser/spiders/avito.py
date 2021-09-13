import scrapy
from scrapy.http import HtmlResponse
from lesson7.avitoparser.items import AvitoparserItem
from scrapy.loader import ItemLoader  #после паука до передачи в паплайн, берет часть нагрузки от паука и часть от паплайна, чтобы размазать нагрузку

class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']

    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://www.avito.ru/rossiya?q={query}']

    def parse(self, response: HtmlResponse):
        adv_links = response.xpath("//a[@data-marker='item-title']")
        for link in adv_links:
            yield response.follow(link, callback=self.parse_adv)
        pass

    def parse_adv(self, response: HtmlResponse):
        loader = ItemLoader(item=AvitoparserItem(), response=response)  # Создаем отдельный объект для работы с item (здесь инициализируются все поля item'a и их обработчики)
        loader.add_xpath('name', "//h1/span/text()")   # Наполняем item данными (также сразу запускаются предобработчики)
        loader.add_xpath('price', "//span[@class='js-item-price']/text()")
        loader.add_xpath('photos', "//div[contains(@class,'gallery-img-frame')]/@data-url")
        loader.add_value('url', response.url)
        yield loader.load_item()      # Отправляем в пайплайн (также здесь запускаются постобработчики)



"""        name = response.xpath("//h1/span/text()").get()
        price = response.xpath("//span[@class='price-value-string js-price-value-string']/span[@content]/text()").get()
        photos = response.xpath("//div[contains(@class, 'gallery-img-frame')]/@data-url").getall()
        yield AvitoparserItem(name=name, price=price, photos=photos)"""
#        print(1)