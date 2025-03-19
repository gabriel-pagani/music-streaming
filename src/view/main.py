from os import system
from re import search, match
from pyodbc import Error
from utils.conection import server_request
from utils.hash import generate_hash, verify_hash


def exibir_titulo(titulo):
    print('=' * 50)
    print(f'{titulo:^50}')
    print('=' * 50)


def validar_email(email):
    return bool(match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))


def validar_senha(password):
    return (len(password) >= 8 and
            search(r'[A-Z]', password) and
            search(r'[a-z]', password) and
            search(r'[0-9]', password) and
            search(r'[!@#$%^&*(),.?":{}|<>]', password))


def mostrar_erro(mensagem):
    system('cls')
    print(f'\033[31m{mensagem}\033[m')
    print('=' * 50)


def mostrar_aviso(mensagem):
    system('cls')
    print(f'\033[93m{mensagem}\033[m')
    print('=' * 50)


def fazer_login():
    system('cls')
    exibir_titulo('Login')
    email = str(input('Email: '))
    password = str(input('Senha: '))

    if not validar_email(email):
        mostrar_aviso("Formato de email inválido!")
        return [False, None, None]

    try:
        response = server_request(
            query=f"SELECT hash_senha, nome FROM usuarios WHERE email = '{email}'"
        )
        hash_senha = response['data'][0][0]
        nome = response['data'][0][1]

        if not response or 'data' not in response or not response['data']:
            mostrar_aviso("Usuário inexistente!")
            return [False, None, None]

        if verify_hash(string=password, hash=hash_senha):
            system('cls')
            print('\033[32mLogin efetuado com sucesso!\033[m')
            print('=' * 50)
            return [True, email, nome]

        else:
            mostrar_aviso("Usuário e/ou senha incorretos!")
            return [False, None, None]

    except Error as e:
        mostrar_erro(f"Erro na conexão com o banco: {e}")
        return [False, None, None]


def criar_conta():
    system('cls')
    exibir_titulo('Cadastro')
    nome = str(input('Nome: '))
    email = str(input('Email: '))
    password = str(input('Senha: '))

    if not (nome and password and email):
        mostrar_aviso("Todos os campos são obrigatórios!")
        return False

    if not validar_email(email):
        mostrar_aviso("E-mail inválido! \nPor favor insira um e-mail válido.")
        return False

    if not validar_senha(password):
        mostrar_aviso("Senha fraca! \nA senha deve conter pelo menos 8 caracteres, \n"
                      "uma letra maiúscula, uma letra minúscula, \n"
                      "um número e um caractere especial.")
        return False

    try:
        response = server_request(
            query=f"SELECT COUNT(*) AS count FROM usuarios WHERE email = '{email}'"
        )

        if response and 'data' in response and response['data'] and response['data'][0][0]:
            mostrar_aviso("Este email já está cadastrado!")
            return False

        server_request(
            query=f"INSERT INTO usuarios (email, hash_senha, nome) VALUES ('{email}', '{generate_hash(password)}', '{nome}')"
        )

        system('cls')
        print('\033[32mCadastro efetuado com sucesso!\033[m')
        print('=' * 50)
        return True

    except Error as e:
        mostrar_erro(f"Erro na conexão com o banco: {e}")
        return False


def main():
    exibir_titulo('IMPREXTAE')
    login = False
    user = None
    nome = None

    while not login:
        try:
            print('1 - Fazer login\n2 - Criar conta\n3 - Sair')
            print('=' * 50)
            escolhido = int(input('Escolha uma opção: '))

            if escolhido == 1:
                retorno = fazer_login()
                login = retorno[0]
                user = retorno[1]
                nome = retorno[2]

            elif escolhido == 2:
                criar_conta()

            elif escolhido == 3:
                system('cls')
                print("Obrigado por usar nosso sistema!")
                return

            else:
                mostrar_aviso("Opção inválida, escolha novamente!")

        except ValueError:
            mostrar_aviso("Opção inválida, escolha novamente!")

    system('cls')
    exibir_titulo(f"Bem-vindo, {nome}!")


if __name__ == "__main__":
    main()
