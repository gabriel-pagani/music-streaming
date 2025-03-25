from re import search, match


def validate_email(email: str) -> bool:
    """Valida o formato do email."""
    return bool(match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))


def validate_password(password: str) -> bool:
    """Valida a força da senha."""
    return bool(search(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$', password))


def format_zip_code(cep: str) -> str:
    """Formata o CEP para o padrão 00000-000."""
    if (len(cep) == 8 and cep.isdigit()):
        return f"{cep[:5]}-{cep[5:]}"
    else:
        return None


def format_id(cpf: str) -> str:
    """Formata o CPF para o padrão 000.000.000-00."""
    if (len(cpf) == 11 and cpf.isdigit()):
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}" if len(cpf) == 11 else ''
    else:
        return None


def format_phone(phone: str) -> str:
    """Formata o telefone para o padrão (00) 00000-0000."""
    if (len(phone) == 11 and phone.isdigit()):
        return f"({phone[:2]}){phone[2:7]}-{phone[7:]}"
    else:
        return None


def validate_birth_date(date: str) -> str:
    """Valida data de nascimento no formato dd/mm/aaaa."""
    if match(r'^(\d{2})/(\d{2})/(\d{4})$', date):
        return date
    else:
        return None


def validate_monthly_income(income: str) -> str:
    """Valida se a renda mensal é um valor numérico positivo."""
    try:
        income_value = float(income.replace(',', '.'))
        if income_value > 0:
            return income_value
    except ValueError:
        return None


def validate_state(state: str) -> str:
    """Valida sigla do estado (2 caracteres)."""
    if state in ('AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA',
                 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'):
        return state
    else:
        return None


def validate_number(number: str) -> str:
    """Valida se o número é composto apenas por dígitos."""
    try:
        number = int(number)
        return number
    except ValueError:
        return None
