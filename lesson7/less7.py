#скачивание файла
import requests
url = 'https://cdn.sibkray.ru/upload/iblock/c3a/c3adab15807174f2d20fe8e3ae19747c.jpg'

response = requests.get(url)
with open('sea.jpg', 'wb') as f:
    f.write(response.content)

import wget
wget.download(url)
