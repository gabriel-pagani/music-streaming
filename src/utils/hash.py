from bcrypt import gensalt, hashpw, checkpw


def generate_hash(string: str) -> str:
    """Gera um hash seguro a partir de uma string"""
    salt = gensalt(rounds=12)
    return hashpw(string.encode(), salt).decode()


def verify_hash(string: str, hash: str) -> bool:
    """Verifica se a string confere com o hash"""
    return checkpw(string.encode(), hash.encode())
