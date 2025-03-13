from pyodbc import connect, Error


def server_request(server: str, database: str, query_type: str, query: str, user: str = '', password: str = '') -> dict:
    server_connection = f'DRIVER={{SQL Server}}; SERVER={server}; DATABASE={database}; UID={user}; PWD={password}'
    result = dict()

    try:
        with connect(server_connection) as connection:
            with connection.cursor() as cursor:
                formatted_query = query.strip().upper()
                cursor.execute(formatted_query)

                if query_type.lower() == 'view':
                    data = cursor.fetchall()
                    result['data'] = data
                    result['message'] = 'Consulta executada com sucesso!'
                elif query_type.lower() == 'edit':
                    connection.commit()
                    result['message'] = 'Script executado com sucesso!'
                else:
                    raise ValueError

    except Error as e:
        result['message'] = f'Erro de conexão: {e}'
    except ValueError:
        result['message'] = f'Tipo de consulta inválido!'
    except Exception as e:
        result['message'] = f'Erro inesperado: {e}'

    finally:
        return result
