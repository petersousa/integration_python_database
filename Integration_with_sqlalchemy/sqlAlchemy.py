"""
    Primeiro programa de integração com banco de dados
    utilizando SQLAlchemy e modelo ORM
"""
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DECIMAL

Base = declarative_base()


class Client(Base):
    """
        Esta classe representa a tabela client dentro
        do SQlite.
    """
    __tablename__ = "client"
    # atributos
    id = Column(Integer, primary_key=True)
    nome= Column(String)
    cpf = Column(String(9))
    endereco = Column(String)

    user = relationship(
        "Count", back_populates="conta", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Client(id={self.id}, nome={self.nome}, cpf={self.cpf}), endereco = {self.endereco}"


class Count(Base):
    """
        Esta classe representa a tabela count dentro
        do SQlite.
    """
    __tablename__ = "count"
    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    agencia = Column(String)
    num_conta = Column(Integer, nullable=False)
    saldo = Column(DECIMAL)
    id_cliente = Column(Integer, ForeignKey("client.id"), nullable=False)

    conta = relationship(
        "Client", back_populates="user")


    def __repr__(self):
        return f"Count(id={self.id}, num_conta={self.num_conta}, tipo={self.tipo}, agencia={self.agencia}, saldo={self.saldo})"


print(Client.__tablename__)
print(Count.__tablename__)


# conexão com o banco de dados
engine = create_engine("sqlite://")

# criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

# depreciado - será removido em futuro release
# print(engine.table_names())

# investiga o esquema de banco de dados
inspetor_engine = inspect(engine)
print(inspetor_engine.has_table("client"))
print(inspetor_engine.get_table_names())
print(inspetor_engine.default_schema_name)

with Session(engine) as session:
    juliana = Client(
        nome ='Juliana Mascarenhas',
        cpf = '123456789',
        endereco = 'Rua 1',
        user=[Count(num_conta='123459'),
              Count(num_conta='100025',
                    tipo='conta_corrente', agencia='0001', saldo=1200)]

    )

    sandy = Client (
        nome='Sandy Cardoso',
        cpf='127624125',
        endereco='Rua 2',
        user=[Count(num_conta='12020',tipo='conta_corrente', agencia='0001', saldo=150.50),
                Count(num_conta='10200', tipo='poupanca', agencia='0001', saldo=16214)]
    )

    patrick = Client (
        nome='Patrick Cardoso',
        cpf = '065978987',
        endereco = 'Rua 5',
    )

    # enviando para o BD (persitência de dados)
    session.add_all([juliana, sandy, patrick])

    session.commit()


stmt = select(Client).where(Client.nome.in_(['Juliana Mascarenhas', 'Sandy Cardoso']))
print('Recuperando usuários a partir de condição de filtragem')
for client in session.scalars(stmt):
    print(client)


stmt_address = select(Client).where(Client.endereco.in_([2]))
print('\nRecuperando as contas de Sandy')
for address in session.scalars(stmt_address):
    print(address)


stmt_order = select(Client).order_by(Client.nome.desc())
print("\nRecuperando info de maneira ordenada")
for result in session.scalars(stmt_order):
    print(result)

stmt_join = select(Client.nome, Count.num_conta).join_from(Count, Client)
print("\n")
for result in session.scalars(stmt_join):
    print(result)

print(select(Client.nome, Count.tipo).join_from(Count, Client))

connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
print("\nExecutando statement a partir da connection")
for result in results:
    print(result)

stmt_count = select(func.count('*')).select_from(Client)
print('\nTotal de instâncias em Client')
for result in session.scalars(stmt_count):
    print(result)

print(client.__repr__())

# encerrando de fato a session
session.close()


