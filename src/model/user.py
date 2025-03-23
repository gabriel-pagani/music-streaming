from src.utils.terminal import limpar_tela, mostrar_aviso, mostrar_erro
from src.utils.connection import server_request
from src.utils.hash import generate_hash, verify_hash
from logging import error


class User:

    def __init__(self, email: str, password: str, name: str = None, id_number: str = None, birth_date: str = None, monthly_income: float = None,
                 phone: str = None, state: str = None, city: str = None, neighborhood: str = None, street: str = None, number: int = None,
                 complement: str = None, zip_code: str = None, id: int = None, score: int = None, status: str = None, user_type: str = None,
                 registration_date: str = None, update_date: str = None, observations: str = None) -> None:
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
        self.id = id
        self.user_type = user_type
        self.score = score
        self.status = status
        self.registration_date = registration_date
        self.update_date = update_date
        self.observations = observations

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

    def login(self):
        try:
            response = server_request(
                query="SELECT * FROM usuarios WHERE email = ?",
                params=(self.email,)
            )

            if not response or 'data' not in response or not response['data']:
                mostrar_aviso("Usuário inexistente!")
                return False
            else:
                id = response['data'][0]['ID']
                hash_senha = response['data'][0]['HASH_SENHA']
                name = response['data'][0]['NOME']
                id_number = response['data'][0]['CPF']
                birth_date = response['data'][0]['DATA_NASCIMENTO']
                monthly_income = response['data'][0]['RENDA_MENSAL']
                phone = response['data'][0]['TELEFONE']
                state = response['data'][0]['ESTADO']
                city = response['data'][0]['CIDADE']
                neighborhood = response['data'][0]['BAIRRO']
                street = response['data'][0]['LOGRADOURO']
                number = response['data'][0]['NUMERO']
                complement = response['data'][0]['COMPLEMENTO']
                zip_code = response['data'][0]['CEP']
                user_type = response['data'][0]['TIPO']
                score = response['data'][0]['SCORE']
                status = response['data'][0]['STATUS']
                registration_date = response['data'][0]['DATA_CADASTRO']
                update_date = response['data'][0]['DATA_ATUALIZACAO']
                observations = response['data'][0]['OBSERVACOES']

                if verify_hash(string=self.password, hash=hash_senha):
                    limpar_tela()
                    print('\033[32mLogin efetuado com sucesso!\033[m')
                    print('=' * 50)

                    self.id = id
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
                    self.user_type = user_type
                    self.score = score
                    self.status = status
                    self.registration_date = registration_date
                    self.update_date = update_date
                    self.observations = observations

                    return self
                else:
                    mostrar_aviso("Usuário e/ou senha incorretos!")
                    return False

        except Exception as e:
            error(f"Erro ao fazer login: {e}")
            mostrar_erro(
                "Ocorreu um erro ao tentar fazer login. Tente novamente.")
            return False

    def update_account(self, fields: dict):
        filled_fields = {}

        for field, value in fields.items():
            if not value:
                continue

            else:
                filled_fields[field] = value

        if not filled_fields:
            mostrar_aviso(
                'Nenhum dado foi informado ou estão\n'
                'fora do formato necessário para atualização.')
            return

        else:
            try:
                set_clause = ", ".join(
                    [f"{col} = ?" for col in filled_fields])
                valores = tuple(
                    filled_fields.values()) + (self.id,)
                query = f"UPDATE usuarios SET {set_clause} WHERE id = ?"

                server_request(query=query, params=valores)
                print(
                    '\033[32mCadastro atualizado com sucesso!\033[m')
                return

            except Exception as e:
                error(
                    f"Erro ao atualizar cadastro: {e}")
                mostrar_erro(
                    "Erro ao atualizar cadastro. Tente novamente mais tarde.")
                return
