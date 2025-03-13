import bcrypt


def generate_hash(password):
    # Gera um hash seguro para a senha
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()


def verify_hash(password, hashed_password):
    # Verifica se a senha digitada confere com o hash armazenado
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
