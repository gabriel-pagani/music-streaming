from re import search, match


def validate_email(email):
    """Valida o formato do email."""
    return bool(match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))


def validate_password(password):
    """Valida a força da senha."""
    return bool(search(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$', password))


def validate_zip_code(cep):
    """Valida o formato do CEP."""
    return bool(match(r'^\d{5}-?\d{3}$', cep))


def validate_id(cpf):
    """Valida o formato do CPF."""
    return bool(match(r'^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$', cpf))


def validate_phone(phone):
    """Valida o formato do número de telefone."""
    return bool(search(r'^\(\d{2}\)\s?\d{4,5}-?\d{4}$', phone))
