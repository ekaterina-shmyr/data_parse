#2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis). Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

#вариант с вк
import requests
import json
from pprint import pprint

user_id = '000000'
token = '0000000000000000000000000000000000000000000000000000'


response = requests.get(f'https://api.vk.com/method/groups.get?user_id={user_id}&access_token={token}&v=5.52').json()
pprint(response)

with open('gpoups_vk.json', 'w') as f:
    json.dump(response, f)

#вариант с yeld

import requests
from pprint import pprint

token = '0000000000000000000000000000000000000000000000000000'

my_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) "
        "Gecko/20100101 Firefox/88.0"
    }
url = 'https://api.yelp.com/v3/businesses/matches'
key = {'Authorization': 'Bearer {token}'}
my_params = {
    'name': "Sushi Damo",
    'address1': "330 W 58th St",
    'city': "New York",
    'state': "NY",
    'country': "US"
}

response = requests.get(url, headers=key, params=my_params)

pprint(response.json())

