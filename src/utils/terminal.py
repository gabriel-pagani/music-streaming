from os import system, name


def limpar_tela():
    system('cls' if name == 'nt' else 'clear')


def exibir_titulo(titulo):
    print('=' * 50)
    print(f'{titulo:^50}')
    print('=' * 50)


def mostrar_erro(mensagem):
    limpar_tela()
    print(f'\033[31m{mensagem}\033[m')
    print('=' * 50)


def mostrar_aviso(mensagem):
    limpar_tela()
    print(f'\033[93m{mensagem}\033[m')
    print('=' * 50)
