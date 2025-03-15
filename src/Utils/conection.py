from pyodbc import connect, Error


def server_request(server: str, database: str, query_type: str, query: str, user: str = '', password: str = '') -> dict:
    # Args:
    # server (str): Nome/endereço do servidor SQL
    # database (str): Nome do banco de dados
    # query_type (str): Tipo de consulta ('view' ou 'edit')
    # query (str): Query SQL a ser executada
    # user (str, opcional): Nome de usuário para autenticação
    # password (str, opcional): Senha para autenticação

    # Returns:
    # dict: Dicionário contendo resultado da consulta e mensagem de status

    # Monta a string de conexão com o servidor
    server_connection = f'DRIVER={{SQL Server}}; SERVER={server}; DATABASE={database}; UID={user}; PWD={password}'
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

                # Para consultas do tipo 'view' (SELECT)
                if query_type.lower() == 'view':
                    # Obtém todos os resultados
                    data = cursor.fetchall()
                    response['data'] = data
                    response['message'] = 'Consulta executada com sucesso!'
                # Para consultas do tipo 'edit' (INSERT, UPDATE, DELETE)
                elif query_type.lower() == 'edit':
                    # Confirma as alterações no banco
                    connection.commit()
                    response['message'] = 'Script executado com sucesso!'
                else:
                    # Tipo de consulta inválido
                    raise ValueError

    except Error as e:
        # Captura erros específicos de conexão com banco
        response['message'] = f'Erro de conexão: {e}'
    except ValueError:
        # Captura erro de tipo de consulta inválido
        response['message'] = f'Tipo de consulta inválido!'
    except Exception as e:
        # Captura quaisquer outros erros não previstos
        response['message'] = f'Erro inesperado: {e}'

    finally:
        return response
