from scrapy.crawler import CrawlerProcess #
from scrapy.settings import Settings

from lesson6.jobparser import settings
from lesson6.jobparser.spiders.hhru import HhruSpider
from lesson6.jobparser.spiders.superjobru import SuperjobruSpider

if __name__ == '__main__':
    crawles_settings = Settings()
    crawles_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawles_settings)
    process.crawl(HhruSpider)
    process.crawl(SuperjobruSpider)

    process.start()