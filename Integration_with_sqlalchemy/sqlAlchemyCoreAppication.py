from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import text
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy import DECIMAL
from sqlalchemy.sql.ddl import CreateSchema

engine = create_engine('sqlite://')


metadata_obj = MetaData()
client = Table(
    'client', metadata_obj,
    Column('client_id', Integer, primary_key=True),
    Column('client_name', String(40), nullable=False),
    Column('cpf', String(9), nullable=False),
    Column('endereço', String(50), nullable=False)
)

count = Table(
    'count', metadata_obj,
    Column('id_count', Integer, primary_key=True),
    Column('id_client', Integer, ForeignKey("client.client_id"),nullable=False),
    Column('coubt_name', String(40), nullable=False),
    Column('count_saldo', DECIMAL, nullable=False),
    Column('count_agencia', String, nullable=False),
    Column('count_tipo', String, nullable=False),
    Column('count_num', String, nullable=False)
)

print('\nInfo da tabela client')
print(client.primary_key)
print(client.constraints)

print('\n')
print(metadata_obj.tables)

for table in metadata_obj.sorted_tables:
    print(table)


metadata_obj.create_all(engine)

metadata_db_obj = MetaData(schema='bank')
financial_info = Table(
    'financial_info',
    metadata_db_obj,
    Column('id', Integer, primary_key=True),
    Column('value', String(100), nullable=False),
)

# inserindo info na tabela
sql_insert = text("insert into client values(2,'julia','233456748','Rua QJ')")
engine.execute(sql_insert)

print('\nInfo da tabela finalcial_info')
print(financial_info.primary_key)
print(financial_info.constraints)

print('\nExecutando statement sql')
sql = text('select * from client')
result = engine.execute(sql)

for row in result:
    print(row)


