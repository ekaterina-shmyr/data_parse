from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

#driver = webdriver.Chrome()

chrome_options = Options()
#chrome_options.add_argument('--start-maximized') - откроет на полный экран
chrome_options.add_argument('--window-size=760,1248')

driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
#сайт гб
driver.get('https://gb.ru/login')

elem = driver.find_element_by_id("user_email")
elem.send_keys('study.ai_172@mail.ru')

elem = driver.find_element_by_id("user_password")
elem.send_keys('Password172')

elem.send_keys(Keys.ENTER)

time.sleep(0.5)
menu = driver.find_element_by_xpath("//span[text()='меню']")
menu.click()

menu = driver.find_element_by_xpath("//button[@data-test-id='user_dropdown_menu']")
menu.click()

link = driver.find_element_by_xpath("//li/a[contains(@href,'/users/')]")
driver.get(link.get_attribute('href'))


#сайт пятерки

from selenium.webdriver.support.ui import WebDriverWait #на основании этого класса создается объект ожидания
from selenium.webdriver.support import expected_conditions as EC #модуль событий
from selenium.webdriver.common.by import By #содержит методы поиска в нутри WebDriverWait
import selenium.common.exceptions as s_exceptions

chrome_options = Options()
chrome_options.add_argument('--start-maximized')
driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
driver.get('https://5ka.ru/special_offers/')

driver.implicitly_wait(10) #будет ждать 10 сек пока не появится элемент на странице, не явная задержка, кот влияет на все элементы

city = driver.find_element_by_class_name('location__select-city')
city.click()

city = driver.find_element_by_xpath("//span[text()='г.Санкт-Петербург']")
city.click()

while True:
    try:
        wait = WebDriverWait(driver, 10)
        button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'special-offers__more-btn'))) #пишем чего ждем из модуля ЕС
        # button = driver.find_element_by_class_name('special-offers__more-btn')
        button.click()
    except s_exceptions.TimeoutException:
        print('раскрытие страниц закончено')
        break

goods = driver.find_elements_by_class_name('sale-card')
for good in goods[:-3]:
    print(good.find_element_by_class_name('sale-card__title').text)

#сайт пикабу
from selenium.webdriver.common.action_chains import ActionChains


chrome_options = Options()
chrome_options.add_argument('--start-maximized')

driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)

driver.get('https://pikabu.ru/')

for i in range(5):
    articles = driver.find_elements_by_tag_name('article')
    actions = ActionChains(driver)
    # actions.key_down(Keys.CONTROL).key_down(Keys.ENTER)
    actions.move_to_element(articles[-1])
    actions.perform()
    time.sleep(3)
