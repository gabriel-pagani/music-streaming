import logging
from src.utils.connection import server_request
from src.utils.hash import generate_hash
from main import *

id = 1
tipo = 'User'

if tipo == 'User':
    """
        atualizar o cadastro
        fazer uma solicitação
        acompanhar a solicitação
        acompanhar o empréstimo
    """
    while True:
        try:
            print('1 - Solicitar empréstimo\n2 - Acompanhar solicitação\n3 - Acompanhar Empréstimos\n4 - Atualizar cadastro')
            print('='*50)
            opcao = int(input('Escolha uma opção: '))
            if opcao == 1:
                ...
            elif opcao == 2:
                ...
            elif opcao == 3:
                ...
            elif opcao == 4:
                limpar_tela()
                exibir_titulo('Atualização de Cadastro')
                while True:
                    print('Deixe em branco os campos que não deseja alterar.')
                    print('=' * 50)
                    nome = str(input('Nome: ')).lower().strip()
                    email = str(input('Email: ')).lower().strip()
                    senha = str(input('Senha: ')).lower().strip()
                    cpf = str(input('Cpf: ')).lower().strip()
                    data_nascimento = str(
                        input('Data Nascimento: ')).lower().strip()
                    renda_mensal = input('Renda Mensal: ')
                    telefone = str(input('Telefone: ')).lower().strip()
                    estado = str(input('Estado: ')).lower().strip()
                    cidade = str(input('Cidade: ')).lower().strip()
                    bairro = str(input('Bairro: ')).lower().strip()
                    logradouro = str(input('Logradouro: ')).lower().strip()
                    numero = input('Número: ')
                    complemento = str(input('Complemento: ')).lower().strip()
                    cep = str(input('Cep: ')).lower().strip()

                    # Verifica campos preenchidos e constrói query dinâmica
                    campos_preenchidos = {}
                    if nome:
                        campos_preenchidos['nome'] = nome
                    if email:
                        if validar_email(email):
                            campos_preenchidos['email'] = email
                        else:
                            mostrar_aviso("Email inválido!")
                            continue
                    if senha:
                        if validar_senha(senha):
                            senha_hash = generate_hash(senha)
                            campos_preenchidos['senha'] = senha_hash
                        else:
                            mostrar_aviso(
                                "Senha fraca! Deve conter pelo menos 8 caracteres, uma letra maiúscula, uma minúscula, um número e um caractere especial.")
                            continue
                    if cpf:
                        campos_preenchidos['cpf'] = cpf
                    if data_nascimento:
                        campos_preenchidos['data_nascimento'] = data_nascimento
                    if renda_mensal:
                        try:
                            campos_preenchidos['renda_mensal'] = float(
                                renda_mensal)
                        except ValueError:
                            mostrar_erro("Renda mensal deve ser um número.")
                            continue
                    if telefone:
                        campos_preenchidos['telefone'] = telefone
                    if estado:
                        campos_preenchidos['estado'] = estado
                    if cidade:
                        campos_preenchidos['cidade'] = cidade
                    if bairro:
                        campos_preenchidos['bairro'] = bairro
                    if logradouro:
                        campos_preenchidos['logradouro'] = logradouro
                    if numero:
                        try:
                            campos_preenchidos['numero'] = int(numero)
                        except ValueError:
                            mostrar_erro("Número deve ser um valor inteiro.")
                            continue
                    if complemento:
                        campos_preenchidos['complemento'] = complemento
                    if cep:
                        campos_preenchidos['cep'] = cep

                    # Se nenhum campo foi preenchido
                    if not campos_preenchidos:
                        mostrar_aviso(
                            "Nenhum dado foi informado para atualização.")
                        break

                    # Construir query SQL dinâmica
                    colunas = list(campos_preenchidos.keys())
                    valores = list(campos_preenchidos.values())

                    # Monta a string "coluna1 = ?, coluna2 = ?, ..."
                    set_clause = ", ".join([f"{col} = ?" for col in colunas])

                    # Adiciona o ID para o WHERE
                    valores.append(id)

                    query = f"UPDATE usuarios SET {set_clause} WHERE id = ?"

                    try:
                        server_request(query=query, params=valores)
                        mostrar_aviso("Cadastro atualizado com sucesso!")
                    except Exception as e:
                        logging.error(f"Erro ao atualizar cadastro: {e}")
                        mostrar_erro(
                            "Erro ao atualizar cadastro. Tente novamente mais tarde.")

                    break

            else:
                raise ValueError

        except ValueError:
            mostrar_aviso("Opção inválida, escolha novamente!")

elif tipo == 'Approver':
    """
        aprovar as solicitações
        acompanhar a solicitação
    """

elif tipo == 'Admin':
    """
        editar os usuários
        editar as solicitações
        editar os empréstimos
        acompanhar a solicitação
        acompanhar o empréstimo
    """
