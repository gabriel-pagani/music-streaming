import flet as ft
from src.utils.validation_formatting import *
from logging import basicConfig, ERROR, error
from src.model.user import User

basicConfig(filename='main.log', level=ERROR,
            format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s')


class ImprextaeApp:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.user = None
        self.setup_page()
        self.show_login_view()

    def setup_page(self) -> None:
        self.page.title = 'IMPREXTAE'
        self.page.window.width = 800
        self.page.window.min_width = 600
        self.page.window.height = 700
        self.page.window.min_height = 500
        self.page.window.center()
        self.page.window.to_front()
        self.page.window.icon = r'icons\logo.ico'
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.bgcolor = ft.Colors.WHITE
        self.page.padding = 20
        self.page.update()

    def show_error(self, message: str) -> None:
        snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.RED_600
        )
        self.page.overlay.append(snack_bar)
        snack_bar.open = True
        self.page.update()

    def show_success(self, message: str) -> None:
        snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.GREEN_600
        )
        self.page.overlay.append(snack_bar)
        snack_bar.open = True
        self.page.update()

    def show_warning(self, message: str) -> None:
        snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.BLACK),
            bgcolor=ft.Colors.AMBER_400
        )
        self.page.overlay.append(snack_bar)
        snack_bar.open = True
        self.page.update()

    def show_login_view(self) -> None:
        def login_click(e):
            email = email_input.value.lower().strip()
            password = password_input.value

            if not email:
                self.show_warning("O campo de email é obrigatório!")
                return
            elif not validate_email(email):
                self.show_warning("Email inválido, tente novamente!")
                return
            elif not password:
                self.show_warning("O campo de senha é obrigatório!")
                return
            else:
                login_result = User(email=email, password=password).login()
                if login_result[0] == 'Success':
                    self.user = login_result[2]
                    self.page.clean()
                    self.show_success(login_result[1])

                    if self.user.user_type == 'Admin':
                        print('Visão do administrador')
                    elif self.user.user_type == 'Approver':
                        print('Visão do aprovador')
                    else:
                        print('Visão do usuário padrão')

                elif login_result[0] == 'Warning':
                    self.show_warning(login_result[1])
                elif login_result[0] == 'Error':
                    self.show_error(login_result[1])

        def go_to_register(e):
            self.page.clean()
            self.show_register_view()

        # Componentes da tela de login
        title = ft.Text("Imprextae!", size=50,
                        weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900)

        email_input = ft.TextField(
            label="Email",
            prefix_icon=ft.Icons.EMAIL,
            hint_text="Digite seu email aqui...",
            width=400,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900
        )

        password_input = ft.TextField(
            label="Senha",
            prefix_icon=ft.Icons.LOCK,
            hint_text="Digite sua senha aqui...",
            password=True,
            can_reveal_password=True,
            width=400,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900
        )

        login_button = ft.ElevatedButton(
            text="Entrar",
            width=400,
            height=50,
            bgcolor=ft.Colors.BLUE_900,
            color=ft.Colors.WHITE,
            on_click=login_click,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )

        register_button = ft.ElevatedButton(
            text="Criar conta",
            width=400,
            height=50,
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLUE_900,
            on_click=go_to_register,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )

        # Layout
        content = ft.Column(
            controls=[
                title,
                ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                email_input,
                password_input,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                login_button,
                register_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )

        container = ft.Container(
            content=content,
            expand=True,
            alignment=ft.alignment.center
        )

        self.page.add(container)

    def show_register_view(self) -> None:
        def register_click(e):
            name = name_input.value.lower().strip()
            email = email_input.value.lower().strip()
            password = password_input.value

            if not name:
                self.show_warning("O campo de nome é obrigatório!")
                return
            elif not email:
                self.show_warning("O campo de email é obrigatório!")
                return
            elif not validate_email(email):
                self.show_warning(
                    "E-mail inválido! Por favor insira um e-mail válido.")
                return
            elif not password:
                self.show_warning("O campo de senha é obrigatório!")
                return
            elif not validate_password(password):
                self.show_warning(
                    "Senha fraca! A senha deve conter no mínimo 8 caracteres ou mais, uma letra maiúscula, uma letra minúscula, um número e um caractere especial.")
                return
            else:
                try:
                    register_result = User(
                        name=name, email=email, password=password).create_account()
                    if register_result[0] == 'Success':
                        self.show_success("Cadastro efetuado com sucesso!")
                        self.page.clean()
                        self.show_login_view()
                    elif register_result[0] == 'Warning':
                        self.show_warning(register_result[1])
                    elif register_result[0] == 'Error':
                        self.show_error(register_result[1])
                except Exception as e:
                    error(f"Erro ao criar conta: {e}")
                    self.show_error(
                        'Ocorreu um erro ao tentar criar a conta. Tente novamente.')
                    return

        def go_to_login(e):
            self.page.clean()
            self.show_login_view()

        # Componentes da tela de registro
        title = ft.Text("Criar Conta", size=50,
                        weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900)

        name_input = ft.TextField(
            label="Nome Completo",
            prefix_icon=ft.Icons.PERSON,
            hint_text="Digite seu nome completo aqui...",
            width=400,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900
        )

        email_input = ft.TextField(
            label="Email",
            prefix_icon=ft.Icons.EMAIL,
            hint_text="Digite seu email aqui...",
            width=400,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900
        )

        password_input = ft.TextField(
            label="Senha",
            prefix_icon=ft.Icons.LOCK,
            hint_text="Digite sua senha aqui...",
            password=True,
            can_reveal_password=True,
            width=400,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900
        )

        register_button = ft.ElevatedButton(
            text="Criar Conta",
            width=400,
            height=50,
            bgcolor=ft.Colors.BLUE_900,
            color=ft.Colors.WHITE,
            on_click=register_click,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )

        login_button = ft.ElevatedButton(
            text="Já tenho uma conta",
            width=400,
            height=50,
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLUE_900,
            on_click=go_to_login,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )

        # Layout
        content = ft.Column(
            controls=[
                title,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                name_input,
                email_input,
                password_input,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                register_button,
                login_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )

        container = ft.Container(
            content=content,
            expand=True,
            alignment=ft.alignment.center
        )

        self.page.add(container)
