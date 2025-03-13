from bcrypt import gensalt, hashpw, checkpw


def generate_hash(password):
    # Gera um hash seguro para a senha
    salt = gensalt(round=12)
    return hashpw(password.encode(), salt)


def verify_hash(password, hashed_password):
    # Verifica se a senha digitada confere com o hash armazenado
    return checkpw(password.encode(), hashed_password)
