"""Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем должность) с сайтов HH(обязательно) и/или Superjob(по желанию). Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:

    Наименование вакансии.
    Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
    Ссылку на саму вакансию.
    Сайт, откуда собрана вакансия.

По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение). Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv."""

import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import pandas as pd

url = 'https://hh.ru'

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
#можно использовать инпут для выбора вакансии, но я решила сама задать
#keywords = input("введите интересующую вакансию")
keywords = 'kurer'

params = {'?page': 0}


vacancy_list = []
while params['?page'] < 40:
    response = requests.get(url + '/vacancies/' + keywords, params=params, headers=headers)
    soup = bs(response.text, 'html.parser')
    vacancies = soup.find_all('div', {'class': 'vacancy-serp-item'})
    vacancy_list = vacancy_list
#    print(len(vacancy_list))
    for vacance in vacancies:
        vacancies_data = {}
        name_vacancy = vacance.find('a', {'class': 'bloko-link'}).text
        employer = vacance.find('a', {'class': 'bloko-link_secondary'}).text
        url_vacancy = vacance.find("a", attrs={"class": "bloko-link"}).get("href")
        try:
            salary = vacance.find('div', {'class': "vacancy-serp-item__sidebar"}).text.split(' ')

            if salary[0] == 'от':
                salary_min = None
            else:
                if salary[0] == 'до':
                    salary_max = salary[1]
                    salary_currency = salary[2]

                else:
                    salary_min = salary[0]
                    salary_max = salary[2]
                    salary_currency = salary[3]

        except:
#            print('1') - использовалось для проверки
            salary_min = None
            salary_max = None
            salary_currency = None
            continue
        vacancies_data['name_vacancy'] = name_vacancy
        vacancies_data['salary_min'] = salary_min
        vacancies_data['salary_max'] = salary_max
        vacancies_data['salary_currency'] = salary_currency
        vacancies_data['url_vacancy'] = url_vacancy
        vacancies_data['source'] = 'https://hh.ru'

        vacancy_list.append(vacancies_data)

    params['?page'] += 1
#    print(params['?page'])  - использовалось для проверки

#pprint(vacancy_list)  - использовалось для проверки
#pprint(len(vacancy_list))  - использовалось для проверки

#вывод данных через DataFrame
df = pd.DataFrame(vacancy_list)
df.to_csv('vacancy_list.csv', encoding='utf-8-sig')
print(f'Finished')
