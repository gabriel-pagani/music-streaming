from re import search, match


def validate_email(email: str):
    """Valida o formato do email."""
    return bool(match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))


def validate_password(password: str):
    """Valida a força da senha."""
    return bool(search(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$', password))


def format_zip_code(cep):
    """Formata o CEP para o padrão 00000-000."""
    return f"{cep[:5]}-{cep[5:]}" if len(cep) == 8 else ''


def format_id(cpf):
    """Formata o CPF para o padrão 000.000.000-00."""
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}" if len(cpf) == 11 else ''


def format_phone(phone):
    """Formata o número de telefone para o padrão (00) 00000-0000."""
    return f"({phone[:2]}) {phone[2:7]}-{phone[7:]}" if len(phone) == 11 else ''
