from bcrypt import gensalt, hashpw, checkpw


def generate_hash(password: str) -> bytes:
    # Gera um hash seguro para a senha
    salt = gensalt(rounds=12)
    return hashpw(password.encode(), salt)


def verify_hash(password: str, hashed_password: bytes) -> bool:
    # Verifica se a senha digitada confere com o hash armazenado
    return checkpw(password.encode(), hashed_password)
