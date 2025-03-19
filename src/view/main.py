from os import system
from re import search, match
from pyodbc import Error


def exibir_titulo(titulo):
    # Função para exibir títulos formatados com separadores
    print('=' * 50)
    print(f'{titulo:^50}')
    print('=' * 50)


def validar_email(email):
    # Valida formato de email
    return bool(match(r'.+@.+\..+', email))


def validar_senha(password):
    # Valida critérios de senha
    return (len(password) >= 6 and
            search(r'[A-Z]', password) and
            search(r'[a-z]', password) and
            search(r'[0-9]', password) and
            search(r'[!@#$%^&*(),.?":{}|<>]', password))


def fazer_login():
    # Processo de login
    system('cls')
    exibir_titulo('Login')
    email = input('Email: ')
    password = input('Senha: ')

    # Aqui precisa ter uma requisição para o servidor que vai validar se a senha está correta ou se o usuário existe
    if False:  # Placeholder para validação real
        print('\033[32mLogin efetuado com sucesso!\033[m')
        return True
    else:
        system('cls')
        print('\033[93mUsuário e/ou senha incorretos!\033[m')
        print('=' * 50)
        return False


def criar_conta():
    # Processo de criação de conta
    system('cls')
    exibir_titulo('Cadastro')
    nome = input('Nome: ')
    email = input('Email: ')
    password = input('Senha: ')

    if not (nome and password and email):
        system('cls')
        print('\033[93mDados inválidos, tente novamente!\033[m')
        print('=' * 50)
        return False

    email_valido = validar_email(email)
    senha_valida = validar_senha(password)

    if senha_valida and email_valido:
        # Aqui precisa ter uma requisição para o servidor que vai inserir um novo usuario no banco
        # também vai ser necessario importar a função que criptografa a senha
        system('cls')
        print('\033[32mCadastro efetuado com sucesso!\033[m')
        print('=' * 50)
    else:
        system('cls')
        if not email_valido:
            print(
                '\033[93mE-mail inválido! \nPor favor insira um e-mail válido.\033[m')
            print('=' * 50)
        elif not senha_valida:
            print('\033[93mSenha fraca! \nA senha deve conter pelo menos 6 caracteres, \numa letra maiúscula, uma letra minúscula, \num número e um caractere especial.\033[m')
            print('=' * 50)
        return False


# Programa principal
exibir_titulo('EMPREXTAE')
login = False

while True:
    if login:
        ...  # Código para usuário logado
    else:
        try:
            print('1 - Fazer login\n2 - Criar conta')
            print('=' * 50)
            escolhido = int(input('Escolha uma opção: '))

            try:
                if escolhido == 1:
                    login = fazer_login()
                    if login:
                        break

                elif escolhido == 2:
                    if criar_conta():
                        break

                else:
                    raise ValueError

            except Error as e:
                print(f'\033[31mErro na requisição com o banco:\033[m {e}')
                print('=' * 50)

        except ValueError:
            system('cls')
            print('\033[31mOpção inválida, escolha novamente!\033[m')
            print('=' * 50)
