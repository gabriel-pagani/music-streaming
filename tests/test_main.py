from os import system
from re import search, match
import logging
from copy_connection import server_request, close_connection
from copy_hash import generate_hash, verify_hash

# Configurar logging
logging.basicConfig(filename='app.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def limpar_tela():
    """Limpa a tela de forma compatível com diferentes sistemas operacionais."""
    system('clear')


def exibir_titulo(titulo):
    print('=' * 50)
    print(f'{titulo:^50}')
    print('=' * 50)


def validar_email(email):
    """Valida o formato do email."""
    return bool(match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))


def validar_senha(password):
    """Valida a força da senha."""
    return (len(password) >= 8 and
            search(r'[A-Z]', password) and
            search(r'[a-z]', password) and
            search(r'[0-9]', password) and
            search(r'[!@#$%^&*(),.?":{}|<>]', password))


def sanitizar_input(texto):
    """Sanitiza o input para prevenir SQL injection e outros ataques."""
    # Remove caracteres potencialmente perigosos
    return texto.replace("'", "").replace('"', '').replace(';', '')


def mostrar_erro(mensagem):
    limpar_tela()
    print(f'\033[31m{mensagem}\033[m')
    print('=' * 50)
    logging.error(mensagem)


def mostrar_aviso(mensagem):
    limpar_tela()
    print(f'\033[93m{mensagem}\033[m')
    print('=' * 50)


def fazer_login():
    limpar_tela()
    exibir_titulo('Login')
    email = str(input('Email: ')).lower().strip()
    password = str(input('Senha: '))

    if not validar_email(email):
        mostrar_aviso("Email inválido!")
        return [False, None, None]

    try:
        # Usa parâmetros para prevenir SQL injection
        response = server_request(
            query="SELECT hash_senha, nome FROM usuarios WHERE email = ?",
            params=(email,)
        )

        if not response or 'data' not in response or not response['data']:
            mostrar_aviso("Usuário inexistente!")
            return [False, None, None]

        # Acesso por nome de coluna em vez de índice
        hash_senha = response['data'][0]['hash_senha']
        nome = response['data'][0]['nome']

        if verify_hash(string=password, hash=hash_senha):
            limpar_tela()
            print('\033[32mLogin efetuado com sucesso!\033[m')
            print('=' * 50)
            return [True, email, nome]
        else:
            mostrar_aviso("Usuário e/ou senha incorretos!")
            return [False, None, None]

    except Exception as e:
        logging.error(f"Erro ao fazer login: {e}")
        mostrar_erro("Ocorreu um erro ao tentar fazer login. Tente novamente.")
        return [False, None, None]


def criar_conta():
    limpar_tela()
    exibir_titulo('Cadastro')
    nome = sanitizar_input(str(input('Nome: ')).strip())
    email = str(input('Email: ')).lower().strip()
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
        # Verifica se o email já existe
        response = server_request(
            query="SELECT COUNT(*) AS count FROM usuarios WHERE email = ?",
            params=(email,)
        )

        if response and 'data' in response and response['data'] and response['data'][0]['count'] > 0:
            mostrar_aviso("Este email já está cadastrado!")
            return False

        # Cria a conta usando parâmetros para prevenir SQL injection
        hashed_password = generate_hash(password)
        server_request(
            query="INSERT INTO usuarios (email, hash_senha, nome) VALUES (?, ?, ?)",
            params=(email, hashed_password, nome)
        )

        limpar_tela()
        print('\033[32mCadastro efetuado com sucesso!\033[m')
        print('=' * 50)
        return True

    except Exception as e:
        logging.error(f"Erro ao criar conta: {e}")
        mostrar_erro(
            "Ocorreu um erro ao tentar criar a conta. Tente novamente.")
        return False


def main():
    try:
        exibir_titulo('IMPREXTAE')
        login = False
        email = None
        nome = None

        while not login:
            try:
                print('1 - Fazer login\n2 - Criar conta\n3 - Sair')
                print('=' * 50)
                escolhido = int(input('Escolha uma opção: '))

                if escolhido == 1:
                    retorno = fazer_login()
                    login = retorno[0]
                    email = retorno[1]
                    nome = retorno[2]

                elif escolhido == 2:
                    criar_conta()

                elif escolhido == 3:
                    limpar_tela()
                    print("Obrigado por usar nosso sistema!")
                    return

                else:
                    mostrar_aviso("Opção inválida, escolha novamente!")

            except ValueError:
                mostrar_aviso("Opção inválida, escolha novamente!")

        limpar_tela()
        exibir_titulo(f"Bem-vindo, {nome.title()}!")

        # Implementar o sistema aqui!

    finally:
        # Garante que a conexão será fechada quando o programa terminar
        close_connection()


if __name__ == "__main__":
    main()
