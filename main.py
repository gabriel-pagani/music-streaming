from src.utils.terminal import limpar_tela, exibir_titulo, mostrar_aviso
from src.utils.validation import validate_email, validate_password
from logging import basicConfig, ERROR
from src.utils.connection import close_connection
from src.model.user import User


basicConfig(filename='main.log', level=ERROR,
            format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s')


def main():
    try:
        exibir_titulo('IMPREXTAE')
        login = False
        id = nome = tipo = None

        while not login:
            try:
                print('1 - Fazer login\n2 - Criar conta\n3 - Sair')
                print('=' * 50)
                opcao = int(input('Escolha uma opção: '))

                if opcao == 1:
                    limpar_tela()
                    exibir_titulo('Login')
                    while True:
                        email = str(input('Email: ')).lower().strip()
                        if not validate_email(email):
                            mostrar_aviso("Email inválido, tente novamente!")
                        else:
                            break
                    password = str(input('Senha: '))
                    user = User(email=email, password=password)
                    retorno = user.log_in()
                    login = retorno[0]
                    id = retorno[1]
                    nome = retorno[2]
                    tipo = retorno[3]

                elif opcao == 2:
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
                        if not validate_email(email):
                            mostrar_aviso(
                                "E-mail inválido! \nPor favor insira um e-mail válido.")
                        else:
                            break
                    while True:
                        password = str(input('Senha: '))
                        if not validate_password(password):
                            mostrar_aviso("Senha fraca!\n"
                                          "A senha deve conter 8 caracteres ou mais,\n"
                                          "uma letra maiúscula, uma letra minúscula,\n"
                                          "um número e um caractere especial.")
                        else:
                            break
                    user = User(name=nome, email=email, password=password)
                    user.create_account()

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
