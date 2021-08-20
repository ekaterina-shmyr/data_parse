#2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis). Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

import requests
import json
from pprint import pprint

user_id = '000000'
token = '0000000000000000000000000000000000000000000000000000'


response = requests.get(f'https://api.vk.com/method/groups.get?user_id={user_id}&access_token={token}&v=5.52').json()
pprint(response)

with open('gpoups_vk.json', 'w') as f:
    json.dump(response, f)

"""
Сначала выбрала себе https://www.yelp.com/developers/documentation/v3/get_started, но не справилась, не подключается. Но нашла в интернете такой код (добавила свой ключ) и он работает : curl -X GET "https://api.yelp.com/v3/businesses/matches\
?name=Sushi%20Damo&address1=330%20W%2058th%20St&city=New%20York&state=NY\
&country=US&limit=1" \
    -H "Authorization: Bearer aQmGDRCmxh0EwYhgYjHYcjUALaSaZ2-k2K7szxfalEsebntQG3V16Sbfo6QHeERU9fbeC1P8ZJEnme4kf0VCCarYFGEQVQgV-Z3v2fPcLb417M-cnR-NNNI1K3wfYXYx"

Может сможете помочь разобраться, чтоже все таки не так:

import requests
from pprint import pprint

my_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) "
        "Gecko/20100101 Firefox/88.0"
    }
url = 'https://api.yelp.com/v3/businesses/matches/'
key = {'Authorization': 'Bearer aQmGDRCmxh0EwYhgYjHYcjUALaSaZ2-k2K7szxfalEsebntQG3V16Sbfo6QHeERU9fbeC1P8ZJEnme4kf0VCCarYFGEQVQgV-Z3v2fPcLb417M-cnR-NNNI1K3wfYXYx'}
my_params = {
    "Content-type": "application/json",
    'name': "Sushi Damo",
    'address1': "330 W 58th St",
    'city': "New York",
    'state': "NY",
    'country': "US"
}

response = requests.get('https://api.yelp.com/v3/businesses/search/', headers=key, params=my_params).json()


pprint(response)
"""