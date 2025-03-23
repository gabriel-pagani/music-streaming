from src.utils.terminal import limpar_tela, exibir_titulo, mostrar_aviso
from src.utils.validation_formatting import *
from logging import basicConfig, ERROR
from src.utils.connection import close_connection
from src.model.user import User


basicConfig(filename='main.log', level=ERROR,
            format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s')


def main():
    try:
        exibir_titulo('IMPREXTAE')
        login = False
        user = None

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
                    user = User(email=email, password=password).login()
                    if user:
                        login = True
                    else:
                        login = False

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
                    new_user = User(name=nome, email=email, password=password)
                    new_user.create_account()

                elif opcao == 3:
                    limpar_tela()
                    exibir_titulo("Obrigado por usar nosso sistema!")
                    return

                else:
                    mostrar_aviso("Opção inválida, escolha novamente!")

            except ValueError:
                mostrar_aviso("Opção inválida, escolha novamente!")

        limpar_tela()
        exibir_titulo(f"Bem-vindo, {user.name.title()}!")

        if user.user_type == 'User':
            while True:
                try:
                    print(
                        '1 - Solicitar empréstimo\n2 - Acompanhar solicitação\n3 - Acompanhar Empréstimos\n4 - Atualizar cadastro')
                    print('='*50)
                    opcao = int(input('Escolha uma opção: '))
                    if opcao == 1:
                        limpar_tela()
                        ...
                    elif opcao == 2:
                        limpar_tela()
                        ...
                    elif opcao == 3:
                        limpar_tela()
                        ...
                    elif opcao == 4:
                        limpar_tela()
                        exibir_titulo('Atualização de Cadastro')
                        print('Deixe em branco os campos que não deseja alterar.')
                        print('=' * 50)
                        while True:
                            campos = {
                                'cpf': format_id(str(input('CPF (Somente dígitos): ')).strip()),
                                'data_nascimento': validate_birth_date(str(input('Data Nascimento (dd/mm/aaaa): ')).strip()),
                                'renda_mensal': validate_monthly_income(str(input('Renda Mensal: ')).strip()),
                                'telefone': format_phone(str(input('Telefone (Somente dígitos): ')).strip()),
                                'estado': validate_state(str(input('Estado (Sigla): ')).upper().strip()),
                                'cidade': str(input('Cidade: ')).strip(),
                                'bairro': str(input('Bairro: ')).strip(),
                                'logradouro': str(input('Logradouro: ')).strip(),
                                'numero': validate_number(str(input('Número (Somente dígitos): ')).strip()),
                                'complemento': str(input('Complemento: ')).strip(),
                                'cep': format_zip_code(str(input('CEP (Somente dígitos): ')).strip())
                            }

                            user.update_account(campos)
                            break

                    else:
                        raise ValueError

                except ValueError:
                    mostrar_aviso("Opção inválida, escolha novamente!")

        elif user.user_type == 'Approver':
            """
                aprovar as solicitações
                acompanhar a solicitação
            """

        elif user.user_type == 'Admin':
            """
                editar os usuários
                editar as solicitações
                editar os empréstimos
                acompanhar a solicitação
                acompanhar o empréstimo
            """

    finally:
        close_connection()


if __name__ == "__main__":
    main()
