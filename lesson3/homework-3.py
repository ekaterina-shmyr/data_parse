#выполнено задание 1:
#Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, записывающую собранные вакансии в созданную БД.
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
from pymongo import MongoClient

url = 'https://hh.ru'

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
#можно использовать инпут для выбора вакансии, но я решила сама задать
#keywords = input("введите интересующую вакансию")
keywords = 'kurer'
params = {'page': 0}
client = MongoClient('127.0.0.1', 27017)
db = client['vacancy_list_1']
vacancy_list = db.vacancy_list

while True:
    response = requests.get(url + '/vacancies/' + keywords, params=params, headers=headers)
    soup = bs(response.text, 'html.parser')
    vacancies = soup.find_all('div', {'class': 'vacancy-serp-item'})
    vacancy_list = vacancy_list

    for vacance in vacancies:
        vacancies_data = {}
        name_vacancy = vacance.find('a', {'class': 'bloko-link'}).text
        try:
            employer = vacance.find('div', {'class': 'vacancy-serp-item__meta-info-company'}).text
        except:
            print(vacance.find("a", attrs={"class": "bloko-link"}).get("href"))
        url_vacancy = vacance.find("a", attrs={"class": "bloko-link"}).get("href")
        try:
            salary = vacance.find('div', {'class': "vacancy-serp-item__sidebar"}).text.split(' ')
            if salary[0] == 'от':
                salary_min = int(salary[1].replace('\u202f', ''))
                salary_max = None
                salary_currency = salary[2]
            elif salary[0] == 'до':
                salary_min = None
                salary_max = int(salary[1].replace('\u202f', ''))
                salary_currency = salary[2]
            else:
                salary_min = int(salary[0].replace('\u202f', ''))
                salary_max = int(salary[2].replace('\u202f', ''))
                salary_currency = salary[3]
        except:
            #            print('1') #использовалось для проверки
            salary_min = None
            salary_max = None
            salary_currency = None
            continue
        vacancies_data['name_vacancy'] = name_vacancy
        vacancies_data['salary_min'] = salary_min
        vacancies_data['salary_max'] = salary_max
        vacancies_data['employer'] = employer
        vacancies_data['salary_currency'] = salary_currency
        vacancies_data['url_vacancy'] = url_vacancy
        vacancies_data['source'] = 'https://hh.ru'
#выполнено задание 3:
#Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.
        vacancy_list.update_one({'url_vacancy': vacancies_data['url_vacancy']}, {'$set': vacancies_data}, upsert=True)


    params['page'] += 1 #использовалось для проверки
    print(params['page']) #использовалось для проверки

    if not soup.find('span', {'class': 'bloko-form-spacer'}):
        break

#выполнено задание 2:
#Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы (необходимо анализировать оба поля зарплаты). Для тех, кто выполнил задание с Росконтролем - напишите запрос для поиска продуктов с рейтингом не ниже введенного или качеством не ниже введенного (то есть цифра вводится одна, а запрос проверяет оба поля)
search = int(input("Enter min salary: "))

for item in vacancy_list.find(
        {'$or': [{'salary_min': {'$gte': search}}, {'salary_max': {'$gte': search}}]}):  # ищет документы
    pprint(item)