from pyodbc import connect, Error
from os import getenv
from dotenv import load_dotenv
from logging import error


load_dotenv()
_connection = None


def get_connection() -> connect:
    """Retorna uma conexão com o banco de dados, criando-a se necessário."""
    global _connection
    if _connection is None or _connection.closed:
        server_connection = f'DRIVER={{SQL Server}}; SERVER={getenv("SERVER")}; DATABASE={getenv("DATABASE")}; UID={getenv("USER")}; PWD={getenv("PASSWORD")}'
        try:
            _connection = connect(server_connection)
        except Error as e:
            error(f"Erro ao conectar ao banco de dados: {e}")
            raise
    return _connection


def server_request(query: str, params: tuple = None) -> dict:
    """
    Executa uma query SQL com parâmetros para evitar SQL injection

    Args:
        query: Query SQL com placeholders para parâmetros (?)
        params: Tupla de parâmetros para substituir os placeholders

    Returns:
        dict: Dicionário com os resultados ou mensagem de erro
    """
    response = dict()

    try:
        connection = get_connection()
        with connection.cursor() as cursor:

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if query.lower().strip().startswith('select'):
                columns = [column[0] for column in cursor.description]
                data = cursor.fetchall()

                result = []
                for row in data:
                    result.append(dict(zip(columns, row)))

                response['data'] = result
            else:
                connection.commit()

    except Error as e:
        error(f"Erro no banco de dados: {e}")
    except Exception as e:
        error(f"Erro inesperado: {e}")

    return response


def close_connection():
    """Fecha a conexão com o banco de dados."""
    global _connection
    if _connection and not _connection.closed:
        _connection.close()
        _connection = None
