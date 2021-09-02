#код с урока
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)

db = client['user_2308']

users = db.users
books = db.books

#добавление 1 элемента
users.insert_one({"_id": 3541643516541654,
                        "author": "Peter2",
                        "age": '38',
                        "text": "is cool! Wildberry",
                        "tags": ['cool', 'hot', 'ice'],
                        "date": '14.06.1983'})

#добавление многих элементов
users.insert_many([{"author": "John",
               "age" : 29,
               "text": "Too bad! Strawberry",
               "tags": 'ice',
               "date": '04.08.1971'},
                    { "_id": 123,
                        "author": "Anna",
               "age" : 36,
               "title": "Hot Cool!!!",
               "text": "easy too!",
               "date": '26.01.1995'},
                   {"author": "Jane",
               "age" : 43,
               "title": "Nice book",
               "text": "Pretty text not long",
               "date": '08.08.1975',
               "tags":['fantastic', 'criminal']}
      ])

#id = hashlib.sha1(vacance)

#поиск документов

for user in users.find({'author': 'Peter2', 'age':38}):
    pprint(user)

for user in users.find({'$or': [{'author': 'Peter2'}, {'age': 43}]}):
    pprint(user)

for user in users.find({'age': {'$gt': 35}}):
    pprint(user)

for user in users.find({'age': {'$in': ['38', 35]}}):
    if user['age'] == type(int):
        continue
    else:
        print(user)


doc = {
    "author": "Andrey",
               "age" : 28,
               "text": "is hot!",
               "date": '11.09.1991'}

#обновление документов
users.update_one({'author': 'Peter'}, {'$set': doc}, upsert=True)
users.update_many({'author': 'Peter2'}, {'$set': {'author': 'Peter'}})
users.replace_one({'author': 'Peter'}, doc)

#удаление
users.delete_one({'author': 'Andrey'})
users.delete_many({})

for item in users.find({}):
    pprint(item)
