#1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.

import requests
import json

my_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) "
        "Gecko/20100101 Firefox/88.0"
    }
my_params = {'token': 'OAUTH-TOKEN'}
user = 'ekaterina-shmyr'
response = requests.get('https://api.github.com/users/'+user+'/repos', params=my_params, headers=my_headers).json()

repo = {}
for i in response:
    repo.update({i['name']:i['html_url']})

print(f'List repos by', user, repo)

with open('data.json', 'w') as f:
    json.dump(repo, f)
