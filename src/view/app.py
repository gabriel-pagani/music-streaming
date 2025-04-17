import flet as ft
from src.utils.validation_formatting import *
from logging import basicConfig, ERROR, error
from src.utils.hash import generate_hash
from src.utils.search_cep import search_cep
from src.controller.user import User

basicConfig(filename='main.log', level=ERROR,
            format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s')


class App:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.user = User(email='testes', password='testes', name='Gabriel')
        self.setup_page()
        self.show_menu_view()

    def setup_page(self) -> None:
        self.page.title = 'Sprobify'
        self.page.window.icon = r''
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.bgcolor = ft.Colors.WHITE
        self.page.padding = 0
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

    def show_password_confirmation(self, e, password_confirmed_input):
        if e.control.value:
            password_confirmed_input.visible = True
        else:
            password_confirmed_input.visible = False
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
                    self.show_menu_view()

                elif login_result[0] == 'Warning':
                    self.show_warning(login_result[1])
                elif login_result[0] == 'Error':
                    self.show_error(login_result[1])

        def go_to_register(e):
            self.page.clean()
            self.show_register_view()

        # Componentes da tela de login
        title = ft.Text("Sprobify!", size=70,
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
            cursor_color=ft.Colors.BLUE_900,
            on_submit=login_click,
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
            password_confirmed = password_confirmed_input.value

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
            elif password != password_confirmed:
                self.show_warning(
                    "As senhas não coincidem! Por favor, verifique novamente.")
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
        title = ft.Text("Criar Conta", size=70,
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
            cursor_color=ft.Colors.BLUE_900,
            on_change=lambda e: self.show_password_confirmation(
                e, password_confirmed_input)
        )

        password_confirmed_input = ft.TextField(
            label="Confirmar Senha",
            prefix_icon=ft.Icons.LOCK,
            hint_text="Confirme sua senha aqui...",
            password=True,
            can_reveal_password=True,
            width=400,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900,
            visible=False,
            on_submit=register_click,
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
                password_confirmed_input,
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

    def show_update_view(self) -> None:
        def back_to_menu(e):
            self.page.clean()
            self.show_menu_view()

        def save_profile(e):
            if cpf_input.value != '' and not validate_cpf(cpf_input.value):
                self.show_warning('CPF inválido!')
            elif email_input.value != '' and not validate_email(email_input.value.strip()):
                self.show_warning('Email inválido!')
            elif birth_date_input.value != '' and not validate_birth_date(birth_date_input.value):
                self.show_warning('Data de nascimento inválida!')
            elif phone_input.value != '' and not validate_phone(phone_input.value):
                self.show_warning('Telefone inválido!')
            elif zip_code_input.value != '' and not validate_zip_code(zip_code_input.value):
                self.show_warning('CEP inválido!')
            elif password_input.value != password_confirmed_input.value:
                self.show_warning('As senhas não coincidem!')
            elif password_input.value != '' and not validate_password(password_input.value):
                self.show_warning(
                    'Senha fraca! A senha deve conter no mínimo 8 caracteres ou mais, uma letra maiúscula, uma letra minúscula, um número e um caractere especial.')
            else:
                try:
                    # Cria um novo objeto User com apenas os campos preenchidos
                    updated_user = User(id=self.user.id)

                    # Adiciona apenas os campos que foram realmente preenchidos
                    if cpf_input.value:
                        updated_user.id_number = ''.join(
                            filter(str.isdigit, cpf_input.value))
                    if name_input.value:
                        updated_user.name = name_input.value.strip().lower()
                    if email_input.value:
                        updated_user.email = email_input.value.strip().lower()
                    if birth_date_input.value:
                        updated_user.birth_date = birth_date_input.value
                    if phone_input.value:
                        updated_user.phone = ''.join(
                            filter(str.isdigit, phone_input.value))
                    if zip_code_input.value:
                        updated_user.zip_code = ''.join(
                            filter(str.isdigit, zip_code_input.value))
                    if state_input.value:
                        updated_user.state = state_input.value.strip().lower()
                    if city_input.value:
                        updated_user.city = city_input.value.strip().lower()
                    if neighborhood_input.value:
                        updated_user.neighborhood = neighborhood_input.value.strip().lower()
                    if street_input.value:
                        updated_user.street = street_input.value.strip().lower()
                    if number_input.value:
                        updated_user.number = number_input.value.strip().lower()
                    if complement_input.value:
                        updated_user.complement = complement_input.value.strip().lower()
                    if password_input.value:
                        updated_user.password = generate_hash(
                            password_input.value)

                    update_result = updated_user.update_account()

                    if update_result[0] == 'Error':
                        self.show_error(update_result[1])
                    elif update_result[0] == 'Warning':
                        self.show_warning(update_result[1])
                    else:
                        # Atualize o usuário atual com os novos valores
                        if password_input.value:
                            self.user.password = generate_hash(
                                password_input.value)
                        if email_input.value:
                            self.user.email = email_input.value.strip().lower()
                        if name_input.value:
                            self.user.name = name_input.value.strip().lower()
                        if cpf_input.value:
                            self.user.id_number = ''.join(
                                filter(str.isdigit, cpf_input.value))
                        if birth_date_input.value:
                            self.user.birth_date = f'{birth_date_input.value[6:]}-{birth_date_input.value[3:5]}-{birth_date_input.value[:2]}'
                        if phone_input.value:
                            self.user.phone = ''.join(
                                filter(str.isdigit, phone_input.value))
                        if zip_code_input.value:
                            self.user.zip_code = ''.join(
                                filter(str.isdigit, zip_code_input.value))
                        if state_input.value:
                            self.user.state = state_input.value.strip().lower()
                        if city_input.value:
                            self.user.city = city_input.value.strip().lower()
                        if neighborhood_input.value:
                            self.user.neighborhood = neighborhood_input.value.strip().lower()
                        if street_input.value:
                            self.user.street = street_input.value.strip().lower()
                        if number_input.value:
                            self.user.number = number_input.value.strip().lower()
                        if complement_input.value:
                            self.user.complement = complement_input.value.strip().lower()

                        self.page.clean()
                        self.show_success('Perfil atualizado com sucesso!')
                        self.show_menu_view()
                except Exception as e:
                    error(f"Erro ao atualizar conta: {e}")
                    self.show_error(
                        'Ocorreu um erro ao tentar atualizar a conta. Tente novamente.')
                    return

        # Barra superior
        title = ft.Text(
            f"Painel da Conta",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE
        )

        popup_button = ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.SAVE),
                            ft.Text("Salvar Alterações"),
                        ]
                    ),
                    on_click=save_profile,
                ),
                ft.PopupMenuItem(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.ARROW_BACK),
                            ft.Text("Voltar"),
                        ]
                    ),
                    on_click=back_to_menu,
                ),
            ],
            icon_color=ft.Colors.WHITE
        )

        top_bar = ft.Container(
            content=ft.Row(
                [title, ft.Container(expand=True), popup_button],
                alignment=ft.MainAxisAlignment.START
            ),
            padding=ft.padding.all(20),
            bgcolor=ft.Colors.BLUE_900,
            border_radius=ft.border_radius.only(
                bottom_left=10, bottom_right=10),
        )

        # Estilo comum para os cards
        card_style = {
            "elevation": 3,
            "margin": ft.margin.only(bottom=15),
        }

        # Informações Pessoais
        name_input = ft.TextField(
            label="Nome",
            prefix_icon=ft.Icons.PERSON,
            hint_text="Digite seu nome aqui...",
            expand=True,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900,
            value=self.user.name.title(),
        )

        cpf_input = ft.TextField(
            label="CPF",
            prefix_icon=ft.Icons.PERSON,
            hint_text="Digite seu CPF aqui...",
            expand=True,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900,
            value=f'{self.user.id_number[:3]}.{self.user.id_number[3:6]}.{self.user.id_number[6:9]}-{self.user.id_number[9:]}' if self.user.id_number else '',
            on_change=format_cpf
        )

        birth_date_input = ft.TextField(
            label="Data de Nascimento",
            prefix_icon=ft.Icons.CAKE,
            hint_text="dd/mm/aaaa",
            expand=True,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900,
            value=f'{self.user.birth_date[8:]}/{self.user.birth_date[5:7]}/{self.user.birth_date[:4]}' if self.user.birth_date else '',
            on_change=format_date
        )

        phone_input = ft.TextField(
            label="Telefone",
            prefix_icon=ft.Icons.LOCAL_PHONE,
            hint_text="(00)00000-0000",
            expand=True,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900,
            value=f'({self.user.phone[:2]}){self.user.phone[2:7]}-{self.user.phone[7:]}' if self.user.phone else '',
            on_change=format_phone
        )

        email_input = ft.TextField(
            label="Email",
            prefix_icon=ft.Icons.MAIL,
            hint_text="Digite seu email aqui... ",
            expand=True,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900,
            value=self.user.email.lower()
        )

        password_input = ft.TextField(
            label="Nova Senha",
            prefix_icon=ft.Icons.LOCK,
            hint_text="Digite sua senha aqui... ",
            password=True,
            can_reveal_password=True,
            expand=True,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900,
            on_change=lambda e: self.show_password_confirmation(
                e, password_confirmed_input)
        )

        password_confirmed_input = ft.TextField(
            label="Confirmar Senha",
            prefix_icon=ft.Icons.LOCK,
            hint_text="Digite sua senha aqui... ",
            password=True,
            can_reveal_password=True,
            expand=True,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900,
            visible=False
        )

        # Endereço
        zip_code_input = ft.TextField(
            label="CEP",
            prefix_icon=ft.Icons.LOCATION_ON,
            hint_text="00000-000",
            expand=True,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900,
            value=f'{self.user.zip_code[:5]}-{self.user.zip_code[5:]}' if self.user.zip_code else '',
            on_change=format_cep,
            on_blur=lambda e: search_cep(
                e, state_input, city_input, neighborhood_input, street_input)
        )

        state_input = ft.TextField(
            label="Estado",
            prefix_icon=ft.Icons.MAP,
            hint_text="Digite seu estado aqui...",
            expand=True,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900,
            value=self.user.state.title() if self.user.state else '',
        )

        city_input = ft.TextField(
            label="Cidade",
            prefix_icon=ft.Icons.LOCATION_CITY,
            hint_text="Digite sua cidade aqui...",
            expand=True,
            border_color=ft.Colors.BLUE_400,
            value=self.user.city.title() if self.user.city else '',
            cursor_color=ft.Colors.BLUE_900
        )

        neighborhood_input = ft.TextField(
            label="Bairro",
            prefix_icon=ft.Icons.HOLIDAY_VILLAGE,
            hint_text="Digite seu bairro aqui...",
            expand=True,
            border_color=ft.Colors.BLUE_400,
            value=self.user.neighborhood.title() if self.user.neighborhood else '',
            cursor_color=ft.Colors.BLUE_900
        )

        street_input = ft.TextField(
            label="Rua",
            prefix_icon=ft.Icons.SIGNPOST,
            hint_text="Digite sua rua aqui...",
            expand=True,
            border_color=ft.Colors.BLUE_400,
            value=self.user.street.title() if self.user.street else '',
            cursor_color=ft.Colors.BLUE_900
        )

        number_input = ft.TextField(
            label="Número",
            prefix_icon=ft.Icons.TAG,
            hint_text="Digite seu número aqui...",
            expand=True,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900,
            value=self.user.number.upper() if self.user.number else ''
        )

        complement_input = ft.TextField(
            label="Complemento",
            prefix_icon=ft.Icons.APARTMENT,
            hint_text="Digite seu complemento aqui...",
            expand=True,
            border_color=ft.Colors.BLUE_400,
            value=self.user.complement.title() if self.user.complement else '',
            cursor_color=ft.Colors.BLUE_900
        )

        # Cards
        personal_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.PERSON, color=ft.Colors.BLUE_900),
                            ft.Text("Informações Pessoais",
                                    weight=ft.FontWeight.BOLD,
                                    size=18,
                                    color=ft.Colors.BLUE_900)
                        ]),
                        padding=ft.padding.only(bottom=10)
                    ),
                    ft.Divider(height=1, color=ft.Colors.BLUE_100),
                    ft.ResponsiveRow(
                        [
                            ft.Column(
                                col={"sm": 12, "md": 6, "lg": 6},
                                controls=[
                                    name_input
                                ]
                            ),
                            ft.Column(
                                col={"sm": 12, "md": 6, "lg": 6},
                                controls=[
                                    email_input
                                ]
                            )
                        ]
                    ),
                    ft.ResponsiveRow(
                        [
                            ft.Column(
                                col={"sm": 12, "md": 6, "lg": 6},
                                controls=[
                                    cpf_input
                                ]
                            ),
                            ft.Column(
                                col={"sm": 12, "md": 6, "lg": 6},
                                controls=[
                                    phone_input
                                ]
                            )
                        ]
                    ),
                    ft.ResponsiveRow(
                        [
                            ft.Column(
                                col={"sm": 12, "md": 6, "lg": 6},
                                controls=[
                                    birth_date_input
                                ]
                            ),
                            ft.Column(
                                col={"sm": 12, "md": 6, "lg": 6},
                                controls=[
                                    password_input
                                ]
                            )
                        ]
                    ),
                    ft.ResponsiveRow(
                        [
                            ft.Column(
                                col={"sm": 12, "md": 6, "lg": 6},
                                controls=[
                                    password_confirmed_input
                                ]
                            ),
                        ]
                    ),

                ]),
                padding=20,
                expand=True
            ),
            **card_style
        )

        address_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.HOME, color=ft.Colors.BLUE_900),
                            ft.Text("Endereço",
                                    weight=ft.FontWeight.BOLD,
                                    size=18,
                                    color=ft.Colors.BLUE_900)
                        ]),
                        padding=ft.padding.only(bottom=10)
                    ),
                    ft.Divider(height=1, color=ft.Colors.BLUE_100),
                    ft.ResponsiveRow(
                        [
                            ft.Column(
                                col={"sm": 12, "md": 6, "lg": 6},
                                controls=[
                                    zip_code_input
                                ]
                            ),
                            ft.Column(
                                col={"sm": 12, "md": 6, "lg": 6},
                                controls=[
                                    state_input
                                ]
                            )
                        ]
                    ),
                    ft.ResponsiveRow(
                        [
                            ft.Column(
                                col={"sm": 12, "md": 6, "lg": 6},
                                controls=[
                                    city_input
                                ]
                            ),
                            ft.Column(
                                col={"sm": 12, "md": 6, "lg": 6},
                                controls=[
                                    neighborhood_input
                                ]
                            )
                        ]
                    ),
                    ft.ResponsiveRow(
                        [
                            ft.Column(
                                col={"sm": 12, "md": 6, "lg": 6},
                                controls=[
                                    street_input
                                ]
                            ),
                            ft.Column(
                                col={"sm": 12, "md": 6, "lg": 6},
                                controls=[
                                    number_input
                                ]
                            )
                        ]
                    ),
                    ft.ResponsiveRow(
                        [
                            ft.Column(
                                col={"sm": 12, "md": 6, "lg": 6},
                                controls=[
                                    complement_input
                                ]
                            )
                        ]
                    )
                ]),
                padding=20,
                expand=True
            ),
            **card_style
        )

        # Container do formulário em uma ListView com scroll
        form_content = ft.ListView(
            controls=[
                personal_card,
                address_card,
            ],
            spacing=10,
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            expand=True
        )

        # Layout principal
        content = ft.Column(
            [
                top_bar,
                form_content
            ],
            spacing=10,
            expand=True
        )

        self.page.clean()
        self.page.add(content)

    def show_menu_view(self) -> None:
        def update_account(e):
            self.page.clean()
            self.show_update_view()

        def logout(e):
            self.page.clean()
            self.page.scroll = None
            self.user = None
            self.show_login_view()
            self.show_success('Logout efetuado com sucesso!')

        user_greeting = ft.Text(
            f"Olá, {self.user.name.title()}!",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE
        )

        popup_button = ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.PERSON),
                            ft.Text("Minha Conta"),
                        ]
                    ),
                    on_click=update_account,
                ),
                ft.PopupMenuItem(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.LOGOUT),
                            ft.Text("Sair"),
                        ]
                    ),
                    on_click=logout,
                ),
            ],
            icon_color=ft.Colors.WHITE
        )

        top_bar = ft.Container(
            content=ft.Row(
                [user_greeting, ft.Container(expand=True), popup_button],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding=ft.padding.all(20),
            bgcolor=ft.Colors.BLUE_900,
            border_radius=ft.border_radius.only(
                bottom_left=10, bottom_right=10),
        )

        ...  # Desenvolver os elementos apartir daqui

        # Layout principal
        content = ft.Column(
            controls=[
                top_bar,
            ],
            spacing=5,
            expand=True
        )

        self.page.clean()
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.add(content)
