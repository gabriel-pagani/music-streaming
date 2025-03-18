from pyodbc import connect, Error
from os import getenv
from dotenv import load_dotenv

load_dotenv()


def server_request(query: str) -> dict:
    # Monta a string de conexão com o servidor
    server_connection = f'DRIVER={{SQL Server}}; SERVER={getenv("SERVER")}; DATABASE={getenv("DATABASE")}; UID={getenv("USER")}; PWD={getenv("PASSWORD")}'
    # Inicializa dicionário de resposta
    response = dict()

    try:
        # Estabelece conexão com o servidor
        with connect(server_connection) as connection:
            # Cria um cursor para executar comandos
            with connection.cursor() as cursor:
                # Formata a query removendo espaços
                formatted_query = query.strip()
                # Executa a query
                cursor.execute(formatted_query)

                # Para consultas do tipo (SELECT)
                if query.lower().startswith('select'):
                    # Obtém todos os resultados
                    data = cursor.fetchall()
                    response['data'] = data
                    response['message'] = 'Consulta executada com sucesso!'
                # Para consultas do tipo (INSERT, UPDATE, DELETE)
                else:
                    # Confirma as alterações no banco
                    connection.commit()
                    response['message'] = 'Script executado com sucesso!'

    except Error as e:
        # Captura erros específicos de conexão com banco
        response['message'] = f'Erro de conexão: {e}'
    except Exception as e:
        # Captura quaisquer outros erros não previstos
        response['message'] = f'Erro inesperado: {e}'

    finally:
        return response
