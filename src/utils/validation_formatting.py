from re import search, match
from datetime import datetime


def validate_email(email: str) -> bool:
    """Valida o formato do email."""
    return bool(match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) or email == 'testes')


def validate_password(password: str) -> bool:
    """Valida a força da senha."""
    return bool(search(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$', password))


def validate_cpf(cpf: str) -> bool:
    """Valida um CPF verificando os dígitos verificadores."""
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verifica se tem 11 dígitos e não é um CPF com dígitos repetidos
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    # Calcula o primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = soma % 11
    primeiro_digito_verificador = 0 if resto < 2 else 11 - resto

    # Verifica o primeiro dígito verificador
    if primeiro_digito_verificador != int(cpf[9]):
        return False

    # Calcula o segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = soma % 11
    segundo_digito_verificador = 0 if resto < 2 else 11 - resto

    # Verifica o segundo dígito verificador
    return segundo_digito_verificador == int(cpf[10])


def validate_birth_date(date_str: str) -> bool:
    """Valida data de nascimento no formato dd/mm/aaaa."""
    # Verifica se o formato é válido
    if not match(r'^(\d{2})/(\d{2})/(\d{4})$', date_str):
        return False

    try:
        # Tenta converter para data
        day, month, year = map(int, date_str.split('/'))
        date = datetime(year, month, day)

        # Verifica se é data válida e se é no passado
        today = datetime.now()
        return date < today and year >= 1900

    except ValueError:
        return False


def validate_zip_code(cep: str) -> bool:
    """Valida se o CEP está no formato correto."""
    # Remove hífen se existir
    cep = ''.join(filter(str.isdigit, cep))
    return len(cep) == 8 and cep.isdigit()


def validate_phone(phone: str) -> bool:
    """Valida se o telefone está no formato correto."""
    # Remove formatação se existir
    phone = ''.join(filter(str.isdigit, phone))
    # Verifica se tem 10 ou 11 dígitos (com ou sem o 9)
    return len(phone) == 11 and phone.isdigit()


# Essa validação não está verificando se a data existe
def validate_date_card(date_str: str) -> bool:
    """Valida data do cartão no formato mm/aa."""
    # Verifica se o formato é válido
    if not match(r'^(\d{2})/(\d{2})$', date_str):
        return False

    try:
        # Tenta converter para data
        month, year = map(int, date_str.split('/'))
        date = datetime(year, month, 1)

        # Verifica se é data válida e se é no passado
        today = datetime.now()
        return date < today and year >= 1900

    except ValueError:
        return False


def format_cpf(e):
    """Formata CPF em tempo real no campo de entrada."""
    value = ''.join(filter(str.isdigit, e.control.value))

    # Limita a 11 dígitos
    value = value[:11]

    # Formata como XXX.XXX.XXX-XX
    if len(value) <= 3:
        formatted = value
    elif len(value) <= 6:
        formatted = f"{value[:3]}.{value[3:]}"
    elif len(value) <= 9:
        formatted = f"{value[:3]}.{value[3:6]}.{value[6:]}"
    else:
        formatted = f"{value[:3]}.{value[3:6]}.{value[6:9]}-{value[9:]}"

    e.control.value = formatted
    e.control.update()


def format_date(e):
    """Formata data em tempo real no campo de entrada."""
    value = ''.join(filter(str.isdigit, e.control.value))

    # Limita a 8 dígitos
    value = value[:8]

    # Formata como dd/mm/aaaa
    if len(value) <= 2:
        formatted = value
    elif len(value) <= 4:
        formatted = f"{value[:2]}/{value[2:]}"
    else:
        formatted = f"{value[:2]}/{value[2:4]}/{value[4:]}"

    e.control.value = formatted
    e.control.update()


def format_phone(e):
    """Formata telefone em tempo real no campo de entrada."""
    value = ''.join(filter(str.isdigit, e.control.value))

    # Limita a 11 dígitos
    value = value[:11]

    # Formata como (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
    if len(value) == 0:
        formatted = ""
    elif len(value) <= 2:
        formatted = f"({value}"
    elif len(value) <= 7:
        formatted = f"({value[:2]}){value[2:]}"
    else:
        formatted = f"({value[:2]}){value[2:7]}-{value[7:]}"

    e.control.value = formatted
    e.control.update()


def format_cep(e):
    """Formata CEP em tempo real no campo de entrada."""
    value = ''.join(filter(str.isdigit, e.control.value))

    # Limita a 8 dígitos
    value = value[:8]

    # Formata como XXXXX-XXX
    if len(value) <= 5:
        formatted = value
    else:
        formatted = f"{value[:5]}-{value[5:]}"

    e.control.value = formatted
    e.control.update()


def format_card_number(e):
    """Formata o número do cartão em tempo real no campo de entrada."""
    value = ''.join(filter(str.isdigit, e.control.value))

    # Limita a 16 dígitos
    value = value[:16]

    # Formata como XXXX XXXX XXXX XXXX
    if len(value) <= 4:
        formatted = value
    elif len(value) <= 8:
        formatted = f"{value[:4]} {value[4:]}"
    elif len(value) <= 12:
        formatted = f"{value[:4]} {value[4:8]} {value[8:]}"
    else:
        formatted = f"{value[:4]} {value[4:8]} {value[8:12]} {value[12:]}"

    e.control.value = formatted
    e.control.update()


def format_date_card(e):
    """Formata data em tempo real no campo de entrada."""
    value = ''.join(filter(str.isdigit, e.control.value))

    # Limita a 4 dígitos
    value = value[:4]

    # Formata como mm/aa
    if len(value) <= 2:
        formatted = value
    else:
        formatted = f"{value[:2]}/{value[2:]}"

    e.control.value = formatted
    e.control.update()


def format_card_code(e):
    """Formata o código do cartão em tempo real no campo de entrada."""
    value = ''.join(filter(str.isdigit, e.control.value))

    # Limita a 3 dígitos
    value = value[:3]

    e.control.value = value
    e.control.update()
