"""
Esta é uma aplicação com o framework pyMongo.
OBS: É necessário ter o framework instalado em seu projeto.
Caso não tenha, pesquise no site oficial.
"""

import pprint
from pymongo import MongoClient

cliente = MongoClient("Coloque o link do MongoDB Atlas Aqui")
db = cliente.Banco
collection = db.conta_de_banco


def cadastra_cliente(db):
    nome = input("Digite o nome do cliente: ")
    cpf = int(input("Digite o CPF do cliente: "))
    endereco = input("Digite o endereço do cliente: ")
    tipo_conta = input("Digite o tipo de conta: ")
    agencia = input("Digite a agência: ")
    numero = input("Digite o número da conta: ")
    saldo = input("Digite o saldo: ")

    informacoes_cliente = {
        "nome": nome,
        "cpf": cpf,
        "endereco": endereco,
        "tipo_conta": tipo_conta,
        "agencia": agencia,
        "numero": numero,
        "saldo": saldo
    }

    informacoes_clientes = db.informacoes_clientes
    id = informacoes_clientes.insert_one(informacoes_cliente).inserted_id
    print(f"Cliente cadastrado com ID: {id}")


def buscar_contas_clientes(db):
    cpf = int(input("Digite o CPF: "))
    resultados = db.informacoes_clientes.find({"cpf": cpf})
    clientes_encontrados = False

    for resultado in resultados:
        clientes_encontrados = True
        pprint.pprint(resultado)

    if not clientes_encontrados:
        print("Cliente não encontrado.")


def excluir_cliente(db):
    cpf = int(input("Digite o CPF do cliente a ser excluído: "))
    resultados = db.informacoes_clientes.find({"cpf": cpf})

    if resultados.count() > 0:
        for cliente in resultados:
            db.informacoes_clientes.delete_one({"_id": cliente["_id"]})
        print("Todos os clientes com o CPF fornecido foram excluídos com sucesso.")
    else:
        print("Cliente não encontrado.")



def main():
    while True:
        print("\nEscolha uma opção:")
        print("1. Cadastrar cliente")
        print("2. Buscar contas de clientes")
        print("3. Excluir cliente")
        print("4. Sair")

        opcao = input("Digite a opção desejada: ")

        if opcao == '1':
            cadastra_cliente(db)
        elif opcao == '2':
            buscar_contas_clientes(db)
        elif opcao == '3':
            excluir_cliente(db)
        elif opcao == '4':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
