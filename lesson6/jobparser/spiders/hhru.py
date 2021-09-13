import scrapy
from scrapy.http import HtmlResponse
from lesson6.jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=Python&from=suggest_post']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()
        #links = response.css()
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for link in links:
            yield response.follow(link, callback=self.parse_vacancy)

    def parse_vacancy(self, response: HtmlResponse): #сбор данных по вакансии
        vac_name = response.xpath("//h1/text()").get()
        vac_salary = response.xpath("//p[@class='vacancy-salary']/span/text()").get()
        vac_url = response.url
        vac_source = "https://hh.ru"
        #структурируем данные items
        yield JobparserItem(name=vac_name, salary=vac_salary, url=vac_url, source=vac_source)

