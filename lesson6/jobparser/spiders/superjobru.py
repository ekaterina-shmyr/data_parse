import scrapy
from scrapy.http import HtmlResponse
from lesson6.jobparser.items import JobparserItem

class SuperjobruSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']


    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[contains(@class, 'icMQ_ _6AfZ9')]/@href").getall()
        #links = response.css()
        next_page = response.xpath("//a[@rel='next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for link in links:
            yield response.follow(link, callback=self.parse_vacancy)

    def parse_vacancy(self, response: HtmlResponse): #сбор данных по вакансии
        vac_name = response.xpath("//h1/text()").get()
        vac_salary = response.xpath("//span[@class='_1h3Zg _2Wp8I _2rfUm _2hCDz']/text()").getall()
        vac_url = response.url
        vac_source = "https://superjob.ru"
        #структурируем данные items
        yield JobparserItem(name=vac_name, salary=vac_salary, url=vac_url, source=vac_source)