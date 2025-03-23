from src.utils.terminal import limpar_tela, mostrar_aviso, mostrar_erro
from src.utils.connection import server_request
from src.utils.hash import generate_hash, verify_hash
from logging import error


class User:

    def __init__(self, email: str, password: str, name: str = None, id_number: str = None, birth_date: str = None, monthly_income: float = None,
                 phone: str = None, state: str = None, city: str = None, neighborhood: str = None, street: str = None,
                 number: int = None, complement: str = None, zip_code: str = None) -> None:
        self.email = email
        self.password = password
        self.name = name
        self.id_number = id_number
        self.birth_date = birth_date
        self.monthly_income = monthly_income
        self.phone = phone
        self.state = state
        self.city = city
        self.neighborhood = neighborhood
        self.street = street
        self.number = number
        self.complement = complement
        self.zip_code = zip_code

    def create_account(self):
        try:
            response = server_request(
                query="SELECT COUNT(*) AS count FROM usuarios WHERE email = ?",
                params=(self.email,)
            )

            if response and 'data' in response and response['data'] and response['data'][0]['count'] > 0:
                mostrar_aviso("Este email já está cadastrado!")

            else:
                hashed_password = generate_hash(self.password)
                server_request(
                    query="INSERT INTO usuarios (email, hash_senha, nome) VALUES (?, ?, ?)",
                    params=(self.email, hashed_password, self.name)
                )

                limpar_tela()
                print('\033[32mCadastro efetuado com sucesso!\033[m')
                print('=' * 50)

        except Exception as e:
            error(f"Erro ao criar conta: {e}")
            mostrar_erro(
                "Ocorreu um erro ao tentar criar a conta. Tente novamente.")

    def log_in(self):
        try:
            response = server_request(
                query="SELECT id, nome, tipo, hash_senha FROM usuarios WHERE email = ?",
                params=(self.email,)
            )

            if not response or 'data' not in response or not response['data']:
                mostrar_aviso("Usuário inexistente!")
                return [False, None, None, None]

            else:
                id = response['data'][0]['id']
                nome = response['data'][0]['nome']
                tipo = response['data'][0]['tipo']
                hash_senha = response['data'][0]['hash_senha']

                if verify_hash(string=self.password, hash=hash_senha):
                    limpar_tela()
                    print('\033[32mLogin efetuado com sucesso!\033[m')
                    print('=' * 50)
                    return [True, id, nome, tipo]
                else:
                    mostrar_aviso("Usuário e/ou senha incorretos!")
                    return [False, None, None, None]

        except Exception as e:
            error(f"Erro ao fazer login: {e}")
            mostrar_erro(
                "Ocorreu um erro ao tentar fazer login. Tente novamente.")
            return [False, None, None, None]
