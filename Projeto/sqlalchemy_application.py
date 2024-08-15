"""
Este pequeno programa demonstra aplicações com o framework SQLAlchemy.
OBS: É necessário ter o framework instalado em seu projeto.
Caso não tenha, pesquise no site oficial.
"""

from sqlalchemy.orm import (declarative_base, relationship, Session)
from sqlalchemy import Integer, String, Column, ForeignKey, create_engine, select

# Criação da Base
Base = declarative_base()

class Cliente(Base):
    """
    Esta classe cria a tabela 'cliente' no banco de dados.
    """
    __tablename__ = "cliente"

    cliente_id = Column(Integer, primary_key=True)
    nome = Column(String(30), nullable=False)
    cpf = Column(String(9), nullable=False)
    endereco = Column(String(9), nullable=False)

    conta = relationship(
        'Conta',
        back_populates='cliente',
        cascade='all, delete-orphan'
    )

class Conta(Base):
    """
    Esta classe cria a tabela 'conta' no banco de dados.
    """
    __tablename__ = "conta"

    conta_id = Column(Integer, primary_key=True)
    tipo_de_conta = Column(String(10), nullable=False)
    agencia = Column(String(10), nullable=False)
    numero = Column(Integer, nullable=False)
    cliente_id = Column(Integer, ForeignKey("cliente.cliente_id"), nullable=False)

    cliente = relationship('Cliente', back_populates='conta')

# Criando conexão com o banco de dados MySQL
usuario = 'digite o usuario do banco'
senha = 'digite a senha do banco'
host = 'digite o host'
porta = 'digite a porta'
banco_de_dados = 'digite o nome do banco'
engine = create_engine(f'mysql+pymysql://{usuario}:{senha}@{host}:{porta}/{banco_de_dados}')

# Criando as tabelas no banco
Base.metadata.create_all(engine)

def cadastrar_cliente(session):
    digitar_cliente_id = int(input("Digite o ID do cliente: "))
    digitar_nome = input("Digite o nome do cliente: ")
    digitar_cpf = input("Digite o CPF do cliente: ")
    digitar_endereco = input("Digite o endereço do cliente: ")

    inserir_na_tabela_cliente = Cliente.__table__.insert().values(cliente_id=digitar_cliente_id, nome=digitar_nome,
                                                                  cpf=digitar_cpf, endereco=digitar_endereco)

    session.connection().execute(inserir_na_tabela_cliente)
    session.commit()
    print("Cliente cadastrado com sucesso!")

def cadastrar_conta(session):
    digitar_conta_id = int(input("Digite o ID da conta: "))
    digitar_tipo_de_conta = input("Digite o tipo de conta: ")
    digitar_agencia = input("Digite a agencia: ")
    digitar_numero = int(input("Numero da agencia: "))
    id_cliente = int(input("Digite o id do cliente: "))

    inserir_na_tabela_contas = Conta.__table__.insert().values(conta_id=digitar_conta_id,
                                                               tipo_de_conta=digitar_tipo_de_conta,
                                                               agencia=digitar_agencia,
                                                               numero=digitar_numero,
                                                               cliente_id=id_cliente)

    session.connection().execute(inserir_na_tabela_contas)
    session.commit()
    print("Conta cadastrada com sucesso!")

def pesquisar_cliente(session):
    Id_pesquisar = int(input("Digite o ID do cliente: "))

    query = Cliente.__table__.select().where(Cliente.__table__.c.cliente_id == Id_pesquisar)
    resultado = session.connection().execute(query).fetchone()

    if resultado:
        print(f"ID: {resultado.cliente_id}\nNome: {resultado.nome}\nCPF: {resultado.cpf}\nEndereço: {resultado.endereco}")
    else:
        print("Cliente não encontrado")

def listar_todos_clientes(session):
    query_todos_clientes = Cliente.__table__.select()
    resultado_todos = session.connection().execute(query_todos_clientes)

    print("Todos os clientes:")
    for cliente in resultado_todos:
        print(f"ID: {cliente.cliente_id}\nNome: {cliente.nome}\nCPF: {cliente.cpf}\nEndereço: {cliente.endereco}")

def listar_contas_cliente(session):
    cliente_id = int(input("Digite o ID do cliente para listar as contas: "))

    query = Conta.__table__.select().where(Conta.__table__.c.cliente_id == cliente_id)
    resultado = session.connection().execute(query).fetchall()

    if resultado:
        print(f"Contas do cliente com ID {cliente_id}:")
        for conta in resultado:
            print(f"Conta ID: {conta.conta_id}, Tipo: {conta.tipo_de_conta}, Agência: {conta.agencia}, Número: {conta.numero}")
    else:
        print("Nenhuma conta encontrada para este cliente.")


def remover_cliente(session):
    Id_deletar = int(input("Digite o ID do cliente que deseja remover: "))

    # Busque o cliente pelo ID
    cliente = session.get(Cliente, Id_deletar)

    if cliente:
        # Remova o cliente
        session.delete(cliente)
        session.commit()
        print(f"Cliente removido com sucesso.")
    else:
        print(f"Cliente não encontrado.")


def menu():
    with Session(engine) as session:
        while True:
            print("\nMenu de Opções:")
            print("1. Cadastrar Cliente")
            print("2. Cadastrar Conta")
            print("3. Pesquisar Cliente")
            print("4. Listar Todos os Clientes")
            print("5. Listar Contas do Cliente")
            print("6. Remover Cliente")
            print("7. Sair")

            opcao = int(input("Escolha uma opção: "))

            if opcao == 1:
                cadastrar_cliente(session)
            elif opcao == 2:
                cadastrar_conta(session)
            elif opcao == 3:
                pesquisar_cliente(session)
            elif opcao == 4:
                listar_todos_clientes(session)
            elif opcao == 5:
                listar_contas_cliente(session)
            elif opcao == 6:
                remover_cliente(session)
            elif opcao == 7:
                print("Saindo...")
                break
            else:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
