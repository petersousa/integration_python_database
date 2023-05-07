import datetime
import pprint

import pymongo as pyM

client = pyM.MongoClient("mongodb+srv://pymongo:rago1987@cluster0.ipklph5.mongodb.net/?retryWrites=true&w=majority")

db = client.test
collection = db.test_collection
print(db.test_collection)

# definição de infor para compor o doc
post = {
    "nome":"Mike",
    "cpf":"123456789",
    "endereco":"Rua 1",
    "tipo":"conta_corrente",
    "agencia":"0001",
    "num_conta":"102251",
    "saldo":"1520,00",
    "date": datetime.datetime.utcnow()
}

# preparando para submeter as infos
posts = db.posts
post_id = posts.insert_one(post).inserted_id
print(post_id)

print(db.posts)

print(db.list_collection_names()) # mostra o nome da coleção

print(db,posts.find_one()) # mostra o documento procurado (a primeira menção ao requisitado

pprint.pprint(db.posts.find_one()) # mostra o documento procurado com a formatação de criação

#bulk inserts
new_posts = [{
    "nome":"João",
    "cpf":"021553689",
    "endereco":"Rua X",
    "tipo":"conta_corrente",
    "agencia":"0003",
    "num_conta":"001251",
    "saldo":"17855,50",
    "date": datetime.datetime.utcnow()
    },
    {
    "nome": "Miguel",
    "cpf": "000248693",
    "endereco": "Rua Alfa",
    "tipo": "poupanca",
    "agencia": "0001",
    "num_conta": "000001",
    "saldo": "25601,00",
    "date": datetime.datetime.utcnow()
    }]

result = posts.insert_many(new_posts)
print(result.inserted_ids)

print("\nRecuperação final")
pprint.pprint(db.posts.find_one({"nome": "Mike"}))

print("\nDocumentos presentes na coleção posts")
for post in posts.find():
    pprint.pprint(post)