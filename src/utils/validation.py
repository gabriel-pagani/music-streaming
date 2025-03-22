from re import search, match


def validar_email(email):
    """Valida o formato do email."""
    return bool(match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))


def validar_senha(password):
    """Valida a força da senha."""
    return bool(search(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$', password))
