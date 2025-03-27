from src.utils.connection import server_request
from src.utils.hash import generate_hash, verify_hash
from logging import error


class User:

    def __init__(self, email: str = None, password: str = None, name: str = None, id_number: str = None, birth_date: str = None, monthly_income: float = None,
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

    def create_account(self) -> list:
        try:
            response = server_request(
                query="SELECT COUNT(*) AS count FROM usuarios WHERE email = ?",
                params=(self.email,)
            )

            if response and 'data' in response and response['data'] and response['data'][0]['count'] > 0:
                return ['Warning', 'Este email já está cadastrado!']
            else:
                hashed_password = generate_hash(self.password)
                server_request(
                    query="INSERT INTO usuarios (email, hash_senha, nome) VALUES (?, ?, ?)",
                    params=(self.email, hashed_password, self.name)
                )
                return ['Success', 'Cadastro efetuado com sucesso!']

        except Exception as e:
            error(f"Erro ao criar conta: {e}")
            return ['Error', 'Ocorreu um erro ao tentar criar a conta. Tente novamente mais tarde.']

    def login(self) -> list:
        try:
            response = server_request(
                query="SELECT * FROM usuarios WHERE email = ?",
                params=(self.email,)
            )

            if not response or 'data' not in response or not response['data']:
                return ['Warning', 'Usuário inexistente!']
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

                    return ['Success', 'Login efetuado com sucesso!', self]
                else:
                    return ['Warning', "Senha incorreta!"]

        except Exception as e:
            error(f"Erro ao fazer login: {e}")
            return ['Error', "Ocorreu um erro ao tentar fazer login. Tente novamente mais tarde."]

    def update_account(self) -> list:
        try:
            clause = ''
            values = list()
            fields = {
                'cpf': self.id_number,
                'data_nascimento': self.birth_date,
                'renda_mensal': self.monthly_income,
                'telefone': self.phone,
                'estado': self.state,
                'cidade': self.city,
                'bairro': self.neighborhood,
                'logradouro': self.street,
                'numero': self.number,
                'complemento': self.complement,
                'cep': self.zip_code
            }

            for field, value in fields.items():
                if value != None:
                    values.append(value)
                    clause += f'{field} = ?, '

            values.append(self.id)

            query = f"UPDATE usuarios SET {clause.rstrip(', ')} WHERE id = ?"

            server_request(query=query, params=tuple(values))

            return ['Success', 'Cadastro atualizado com sucesso!']

        except Exception as e:
            error(f"Erro ao atualizar cadastro: {e}")
            return ['Error', 'Erro ao atualizar cadastro. Tente novamente mais tarde.']
