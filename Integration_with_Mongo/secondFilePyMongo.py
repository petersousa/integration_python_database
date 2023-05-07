import pprint

import pymongo
import pymongo as pyM

client = pyM.MongoClient("mongodb+srv://pymongo:rago1987@cluster0.ipklph5.mongodb.net/?retryWrites=true&w=majority")
db = client.test
posts = db.posts

for post in posts.find():
    pprint.pprint(post)

print(posts.count_documents({})) #mostra a quabtidade de documentos no banco de dados
print(posts.count_documents({"name":"Mike"}))
print(posts.count_documents({"agencia":"0001"}))

pprint.pprint(posts.find_one({"cpf":"021553689"}))

print("\nRecuperando info da coleção post de maneira ordenada")
for post in posts.find({}).sort("date"):
    pprint.pprint(post)

result = db.profiles.create_index([('author', pymongo.ASCENDING)], unique=True)

print(sorted(list(db.profiles.index_information())))

user_profile_user = [
    {'user_id': 211, 'name': 'Luke'},
    {'user_id': 212, 'name': 'Joao'}
]
result = db.profile_user.insert_many(user_profile_user)

print("\nColeções armazenadas no mongoDB")
collections = db.list_collection_names()
for collection in collections:
    print(collection)

#Apagando uma coleção
#db['profiles'].drop()

for collection in collections:
    print(collection)

#db.profiles.drop()

#print(posts.delete_one({"autor": "Mike"})) #Apaga o documento com as especificações

#print(db.profile_user.drop())

client.drop_database('test')
print(db.list_collection_names())