from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lesson7.avitoparser.spiders.avito import AvitoSpider
from lesson7.avitoparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    # query = input('') #можно передавать параметр
    process.crawl(AvitoSpider, query='квартиры купить')
    process.start()