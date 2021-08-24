#код с урока

from pprint import pprint #работа с коллекциями - структурирует  ответы, каждый элемент быдет выводить с новой строки
import requests

response = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Moscow&appid=e5e4cd692a72b0b66ea0a6b80255d1c3')

# response.headers.get('Content-Type')
# if response.status_code == 200:
#     print()
# response.text
# response.content

if response.ok:
    # pprint(response.text.get('weather')) - неверный вариант, выходит ошибка
    j_data = response.json()
    pprint(j_data)
    print(f"В городе {j_data.get('name')} температура {round(j_data.get('main').get('temp') - 273.15, 2)} градусов")


city = 'Sochi'
my_params = {'q': city,
             'appid': 'e5e4cd692a72b0b66ea0a6b80255d1c3'}

my_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) "
        "Gecko/20100101 Firefox/88.0"
    }
response = requests.get('http://api.openweathermap.org/data/2.5/weather', params=my_params, headers=my_headers)

if response.ok:
    # pprint(response.text)
    j_data = response.json()

    print(f"В городе {j_data.get('name')} температура {round(j_data.get('main').get('temp') - 273.15, 2)} градусов")