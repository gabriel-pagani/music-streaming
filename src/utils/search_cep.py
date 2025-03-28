import requests


def search_cep(e) -> None:
    """
    Busca informações de endereço com base no CEP informado.

    Args:
        cep: O CEP a ser consultado (apenas números)

    Returns:
        Dicionário com dados do endereço ou None se não encontrado
    """

    cep = ''.join(filter(str.isdigit, e.zip_code_input.value))
    if len(cep) == 8:
        try:
            # Faz a requisição para a API ViaCEP
            response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
            if response.status_code == 200:
                data = response.json()
                e.state_input.value = data['estado']
                e.city_input.value = data['localidade']
                e.neighborhood_input.value = data['bairro']
                e.street_input.value = data['logradouro']

                # Verifica se a API retornou erro
                if "erro" in data and data["erro"]:
                    return None
                return data
            return None
        except Exception as e:
            return None
    return None
