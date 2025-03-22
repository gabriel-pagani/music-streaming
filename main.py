from os import system, name
from re import search, match
import logging
from src.utils.connection import server_request, close_connection
from src.utils.hash import generate_hash, verify_hash


logging.basicConfig(filename='main.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s')


def limpar_tela():
    """Limpa a tela de forma compatível com diferentes sistemas operacionais."""
    system('cls' if name == 'nt' else 'clear')


def exibir_titulo(titulo):
    print('=' * 50)
    print(f'{titulo:^50}')
    print('=' * 50)


def validar_email(email):
    """Valida o formato do email."""
    return bool(match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))


def validar_senha(password):
    """Valida a força da senha."""
    return bool(search(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$', password))


def mostrar_erro(mensagem):
    limpar_tela()
    print(f'\033[31m{mensagem}\033[m')
    print('=' * 50)


def mostrar_aviso(mensagem):
    limpar_tela()
    print(f'\033[93m{mensagem}\033[m')
    print('=' * 50)


def fazer_login():
    limpar_tela()
    exibir_titulo('Login')
    while True:
        email = str(input('Email: ')).lower().strip()
        if not validar_email(email):
            mostrar_aviso("Email inválido, tente novamente!")
        else:
            break
    password = str(input('Senha: '))

    try:
        response = server_request(
            query="SELECT hash_senha, nome, tipo, id FROM usuarios WHERE email = ?",
            params=(email,)
        )

        if not response or 'data' not in response or not response['data']:
            mostrar_aviso("Usuário inexistente!")

        hash_senha = response['data'][0]['hash_senha']
        nome = response['data'][0]['nome']
        tipo = response['data'][0]['tipo']
        id = response['data'][0]['id']

        if verify_hash(string=password, hash=hash_senha):
            limpar_tela()
            print('\033[32mLogin efetuado com sucesso!\033[m')
            print('=' * 50)
            return [True, id, nome, tipo]
        else:
            mostrar_aviso("Usuário e/ou senha incorretos!")

    except Exception as e:
        logging.error(f"Erro ao fazer login: {e}")
        mostrar_erro("Ocorreu um erro ao tentar fazer login. Tente novamente.")


def criar_conta():
    limpar_tela()
    exibir_titulo('Cadastro')
    while True:
        nome = str(input('Nome: ')).lower().strip()
        if not nome:
            mostrar_aviso("O campo de nome é obrigatório!")
        else:
            break
    while True:
        email = str(input('Email: ')).lower().strip()
        if not validar_email(email):
            mostrar_aviso(
                "E-mail inválido! \nPor favor insira um e-mail válido.")
        else:
            break
    while True:
        password = str(input('Senha: '))
        if not validar_senha(password):
            mostrar_aviso("Senha fraca!\n"
                          "A senha deve conter 8 caracteres ou mais,\n"
                          "uma letra maiúscula, uma letra minúscula,\n"
                          "um número e um caractere especial.")
        else:
            break

    try:
        response = server_request(
            query="SELECT COUNT(*) AS count FROM usuarios WHERE email = ?",
            params=(email,)
        )

        if response and 'data' in response and response['data'] and response['data'][0]['count'] > 0:
            mostrar_aviso("Este email já está cadastrado!")

        hashed_password = generate_hash(password)
        server_request(
            query="INSERT INTO usuarios (email, hash_senha, nome) VALUES (?, ?, ?)",
            params=(email, hashed_password, nome)
        )

        limpar_tela()
        print('\033[32mCadastro efetuado com sucesso!\033[m')
        print('=' * 50)

    except Exception as e:
        logging.error(f"Erro ao criar conta: {e}")
        mostrar_erro(
            "Ocorreu um erro ao tentar criar a conta. Tente novamente.")


def main():
    try:
        exibir_titulo('IMPREXTAE')
        login = False
        id = None
        nome = None
        tipo = None

        while not login:
            try:
                print('1 - Fazer login\n2 - Criar conta\n3 - Sair')
                print('=' * 50)
                opcao = int(input('Escolha uma opção: '))

                if opcao == 1:
                    retorno = fazer_login()
                    login = retorno[0]
                    id = retorno[1]
                    nome = retorno[2]
                    tipo = retorno[3]

                elif opcao == 2:
                    criar_conta()

                elif opcao == 3:
                    limpar_tela()
                    exibir_titulo("Obrigado por usar nosso sistema!")
                    return

                else:
                    mostrar_aviso("Opção inválida, escolha novamente!")

            except ValueError:
                mostrar_aviso("Opção inválida, escolha novamente!")

        limpar_tela()
        exibir_titulo(f"Bem-vindo, {nome.title()}!")

        # Implementar a continuação do sistema aqui!

    finally:
        close_connection()


if __name__ == "__main__":
    main()
