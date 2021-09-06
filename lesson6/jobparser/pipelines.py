# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy0209

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['salary_min'], item['salary_max'], item['currency'] = self.process_salary_hh(item['salary'])
        if spider.name == 'superjobru':
            item['salary_min'], item['salary_max'], item['currency'] = self.process_salary_sj(item['salary'])
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        #        collection.update_one({'url': item['url']}, {'$set': item}, upsert=True)
        return item

    def process_salary_hh(self, salary):
        salary = salary.split(' ')

        if salary[0] == 'от':
            salary_min = int(salary[1].replace('\xa0', ''))
            if salary[2] == 'до':
                salary_max = int(salary[3].replace('\xa0', ''))
                currency = salary[4]
            else:
                salary_max = None
                currency = salary[2]
        elif salary[0] == 'з/п':
            salary_min = None
            salary_max = None
            currency = None
        else:
            salary_min = None
            salary_max = int(salary[1].replace('\xa0', ''))
            currency = salary[2]

        return salary_min, salary_max, currency

    def process_salary_sj(self, salary):


        if salary[0] == 'от':
            salary_info = salary[2].split('\xa0')
            salary_min = int(salary_info[0]+salary_info[1])
            salary_max = None
            currency = salary_info[2]
        elif salary[0] == 'до':
            salary_min = None
            salary_info = salary[2].split('\xa0')
            salary_max = int(salary_info[0]+salary_info[1])
            currency = salary_info[2]
        elif salary[0] == 'По договорённости':
            salary_min = None
            salary_max = None
            currency = None
        else:
            salary_min = int(salary[0].replace('\xa0', ''))
            try:
                salary_max = int(salary[1].replace('\xa0', ''))
                currency = salary[3]
            except:
                salary_max = None
                currency = salary[2]


        return salary_min, salary_max, currency

