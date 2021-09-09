"""Написать программу, которая собирает «Новинки» с сайта техники mvideo и складывает данные в БД. Сайт можно выбрать и свой. Главный критерий выбора: динамически загружаемые товары"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
import json


client = MongoClient('127.0.0.1', 27017)
db = client['mvideo']
mvideo = db.mvideo

chrome_options = Options()
chrome_options.add_argument('--start-maximized')
driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)

driver.get('https://www.mvideo.ru/')
page = driver.find_element_by_tag_name('html')
page.send_keys(Keys.END)

new_items = driver.find_element_by_xpath('//div[@class = "gallery-title-wrapper"]/h2[contains(text(), "Новинки")]/../../..//ul')
button = new_items.find_element_by_xpath('//div[@class = "gallery-title-wrapper"]/h2[contains(text(), "Новинки")]/../../..//ul/../../a[contains(@class, "next-btn")]')

while 'disabled' not in button.get_attribute('class'):
    driver.implicitly_wait(10)
    driver.execute_script("arguments[0].click();", button)

mvideo_items = driver.find_elements_by_xpath('//div[@class = "gallery-title-wrapper"]/h2[contains(text(), "Новинки")]/../../..//ul/li[@class = "gallery-list-item"]')

for item in mvideo_items:
    mvideo_item = {}
    name = item.find_element_by_tag_name('a').get_attribute('data-track-label')
    url = item.find_element_by_tag_name('a').get_attribute('href')
    price = float(json.loads(item.find_element_by_tag_name('a').get_attribute('data-product-info'))['productPriceLocal'])

    mvideo_item['name'] = name
    mvideo_item['url'] = url
    mvideo_item['price'] = price

    mvideo.update_one({'url': url}, {'$set': mvideo_item}, upsert=True)
driver.quit()
print(f'Завершено')