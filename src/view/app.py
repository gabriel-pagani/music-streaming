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
        self.page.window.width = 825
        self.page.window.height = 750
        self.page.window.center()
        self.page.window.to_front()
        self.page.window.maximizable = False
        self.page.window.resizable = False
        self.page.window.icon = r'icons\logo.ico'
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

                    if self.user.user_type == 'Admin':
                        print('Visão do administrador')
                    elif self.user.user_type == 'Approver':
                        print('Visão do aprovador')
                    else:
                        self.show_user_menu()

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
            visible=False
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

    def show_update_profile(self) -> None:
        def back_to_menu(e):
            self.page.clean()
            self.show_user_menu()

        def save_profile(e):
            # VERIFICAR O FUNCIONAMENTO DO CÓDIGO ATÉ O LIMITADOR ======================================================================================================================================================

            # Validar todos os campos antes de salvar
            valid_form = True
            error_messages = []

            # Validação de nome (não deve estar vazio)
            name = name_input.value.strip()
            if not name:
                valid_form = False
                error_messages.append("Nome é obrigatório")

            # Validação de CPF
            cpf = ''.join(filter(str.isdigit, cpf_input.value))
            if cpf and not validate_cpf(cpf):
                valid_form = False
                error_messages.append("CPF inválido")

            # Validação de data de nascimento
            birth_date = birth_date_input.value
            if birth_date and not validate_birth_date(birth_date):
                valid_form = False
                error_messages.append("Data de nascimento inválida")

            # Validação de renda mensal
            income = monthly_income_input.value
            if income and not validate_monthly_income(income):
                valid_form = False
                error_messages.append("Valor de renda mensal inválido")

            # Validação de telefone
            phone = phone_input.value
            if phone and not validate_phone(phone):
                valid_form = False
                error_messages.append("Telefone inválido")

            # Validação de senha (apenas se foi preenchida)
            password = password_input.value
            password_confirmed = password_confirmed_input.value

            if password:
                if not validate_password(password):
                    valid_form = False
                    error_messages.append(
                        "Senha fraca! A senha deve conter no mínimo 8 caracteres, uma letra maiúscula, uma minúscula, um número e um caractere especial")
                elif password != password_confirmed:
                    valid_form = False
                    error_messages.append("As senhas não coincidem")

            # Validação de CEP
            zip_code = ''.join(filter(str.isdigit, zip_code_input.value))
            if zip_code and not validate_zip_code(zip_code):
                valid_form = False
                error_messages.append("CEP inválido")

            # Validação de número
            number = number_input.value
            if number and not validate_number(number):
                valid_form = False
                error_messages.append("Número inválido")

            # Se houver erros, mostrar mensagem e não prosseguir
            if not valid_form:
                self.show_warning("\n".join(error_messages))
                return

            # LIMITADOR =====================================================================================================================================================================================================

            self.show_success("Perfil atualizado com sucesso!")
            self.page.clean()
            self.show_user_menu()

        # Barra superior
        title = ft.Text(
            f"Atualização de Cadastro",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE
        )

        back_btn = ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_color=ft.Colors.WHITE,
            tooltip="Voltar",
            on_click=back_to_menu
        )

        top_bar = ft.Container(
            content=ft.Row(
                [back_btn, title, ft.Container(expand=True)],
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
            width=350,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900,
            value=self.user.name.title(),
            disabled=True
        )

        cpf_input = ft.TextField(
            label="CPF",
            prefix_icon=ft.Icons.PERSON,
            hint_text="Digite seu CPF aqui...",
            width=350,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900,
            on_change=format_cpf
        )

        birth_date_input = ft.TextField(
            label="Data de Nascimento",
            prefix_icon=ft.Icons.CAKE,
            hint_text="DD/MM/AAAA",
            width=350,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900,
            on_change=format_date
        )

        monthly_income_input = ft.TextField(
            label="Renda Mensal",
            prefix_icon=ft.Icons.ATTACH_MONEY,
            hint_text="R$ 0,00",
            width=350,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900,
            on_change=format_currency
        )

        phone_input = ft.TextField(
            label="Telefone",
            prefix_icon=ft.Icons.LOCAL_PHONE,
            hint_text="(00) 00000-0000",
            width=350,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900,
            on_change=format_phone
        )

        email_input = ft.TextField(
            label="Email",
            prefix_icon=ft.Icons.MAIL,
            hint_text="Digite seu email aqui... ",
            width=350,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900,
            disabled=True,
            value=self.user.email
        )

        password_input = ft.TextField(
            label="Nova Senha",
            prefix_icon=ft.Icons.LOCK,
            hint_text="Digite sua senha aqui... ",
            password=True,
            can_reveal_password=True,
            width=350,
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
            width=350,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900,
            visible=False
        )

        # Endereço
        zip_code_input = ft.TextField(
            label="CEP",
            prefix_icon=ft.Icons.LOCATION_ON,
            hint_text="00000-000",
            width=350,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900,
            on_change=format_cep
        )

        state_input = ft.TextField(
            label="Estado",
            prefix_icon=ft.Icons.MAP,
            hint_text="Digite seu estado aqui...",
            width=350,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900,
        )

        city_input = ft.TextField(
            label="Cidade",
            prefix_icon=ft.Icons.LOCATION_CITY,
            hint_text="Digite sua cidade aqui...",
            width=350,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900
        )

        neighborhood_input = ft.TextField(
            label="Bairro",
            prefix_icon=ft.Icons.HOLIDAY_VILLAGE,
            hint_text="Digite seu bairro aqui...",
            width=350,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900
        )

        street_input = ft.TextField(
            label="Rua",
            prefix_icon=ft.Icons.SIGNPOST,
            hint_text="Digite sua rua aqui...",
            width=350,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900
        )

        number_input = ft.TextField(
            label="Número",
            prefix_icon=ft.Icons.TAG,
            hint_text="Digite seu número aqui...",
            width=350,
            border_color=ft.Colors.BLUE_400,
            cursor_color=ft.Colors.BLUE_900,
            on_change=lambda e: validate_number(e)
        )

        complement_input = ft.TextField(
            label="Complemento",
            prefix_icon=ft.Icons.APARTMENT,
            hint_text="Digite seu complemento aqui...",
            width=350,
            border_color=ft.Colors.BLUE_400,
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
                    ft.Container(
                        content=ft.Row([
                            name_input,
                            cpf_input
                        ], wrap=True, spacing=20),
                        padding=ft.padding.only(top=10)
                    ),
                    ft.Container(
                        content=ft.Row([
                            birth_date_input,
                            monthly_income_input
                        ], wrap=True, spacing=20),
                        padding=ft.padding.only(top=10)
                    ),
                    ft.Container(
                        content=ft.Row([
                            phone_input,
                            email_input
                        ], wrap=True, spacing=20),
                        padding=ft.padding.only(top=10)
                    ),
                    ft.Container(
                        content=ft.Row([
                            password_input,
                            password_confirmed_input
                        ], wrap=True, spacing=20),
                        padding=ft.padding.only(top=10)
                    )
                ]),
                padding=20
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
                    ft.Container(
                        content=ft.Row([
                            zip_code_input,
                            state_input
                        ], wrap=True, spacing=20),
                        padding=ft.padding.only(top=10)
                    ),
                    ft.Container(
                        content=ft.Row([
                            city_input,
                            neighborhood_input
                        ], wrap=True, spacing=20),
                        padding=ft.padding.only(top=10)
                    ),
                    ft.Container(
                        content=ft.Row([
                            street_input,
                            number_input
                        ], wrap=True, spacing=20),
                        padding=ft.padding.only(top=10)
                    ),
                    ft.Container(
                        content=ft.Row([
                            complement_input
                        ], wrap=True, spacing=20),
                        padding=ft.padding.only(top=10)
                    )
                ]),
                padding=20
            ),
            **card_style
        )

        # Botão de salvar
        save_button = ft.ElevatedButton(
            text="Atualizar Informações",
            icon=ft.Icons.SAVE,
            icon_color=ft.Colors.WHITE,
            width=400,
            height=50,
            bgcolor=ft.Colors.BLUE_900,
            color=ft.Colors.WHITE,
            on_click=save_profile,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )

        # Container do formulário em uma ListView com scroll
        form_content = ft.ListView(
            controls=[
                personal_card,
                address_card,
                save_button
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

    def show_user_menu(self) -> None:
        def update_click(e):
            self.page.clean()
            self.show_update_profile()

        def new_loan_click(e):
            self.show_warning('Funcionalidade em desenvolvimento!')

        def track_request_click(e):
            self.show_warning('Funcionalidade em desenvolvimento!')

        def track_loan_click(e):
            self.show_warning('Funcionalidade em desenvolvimento!')

        def logout(e):
            self.page.clean()
            self.show_login_view()
            self.show_success('Logout efetuado com sucesso!')

        # Barra superior com informações do usuário
        user_greeting = ft.Text(
            f"Olá, {self.user.name.title()}!",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE
        )

        logout_btn = ft.IconButton(
            icon=ft.Icons.LOGOUT,
            icon_color=ft.Colors.WHITE,
            tooltip="Sair",
            on_click=logout
        )

        top_bar = ft.Container(
            content=ft.Row(
                [user_greeting, ft.Container(expand=True), logout_btn],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding=ft.padding.all(20),
            bgcolor=ft.Colors.BLUE_900,
            border_radius=ft.border_radius.only(
                bottom_left=10, bottom_right=10),
        )

        # Container comuns para os cards
        container_style = {
            "width": 350,
            "height": 150,
            "padding": 20,
            "border_radius": 15,
            "margin": 10
        }

        # Cards para cada opção do menu
        update_profile_card = ft.Card(
            elevation=5,
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row([
                            ft.Icon(ft.Icons.PERSON_OUTLINE, size=30,
                                    color=ft.Colors.BLUE_900),
                            ft.Text("Atualizar Cadastro",
                                    weight=ft.FontWeight.BOLD, size=18)
                        ]),
                        ft.Text("Mantenha seus dados pessoais atualizados",
                                size=14, color=ft.Colors.GREY_700),
                        ft.Container(expand=True),
                        ft.Container(
                            content=ft.Text(
                                "ACESSAR", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                            bgcolor=ft.Colors.BLUE_900,
                            border_radius=20,
                            padding=ft.padding.symmetric(
                                horizontal=15, vertical=8),
                            on_click=update_click,
                            ink=True
                        )
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.START
                ),
                **container_style
            )
        )

        new_loan_card = ft.Card(
            elevation=5,
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row([
                            ft.Icon(ft.Icons.ADD_CARD, size=30,
                                    color=ft.Colors.GREEN),
                            ft.Text("Solicitar Empréstimo",
                                    weight=ft.FontWeight.BOLD, size=18)
                        ]),
                        ft.Text("Crie uma nova solicitação de empréstimo",
                                size=14, color=ft.Colors.GREY_700),
                        ft.Container(expand=True),
                        ft.Container(
                            content=ft.Text(
                                "SOLICITAR", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                            bgcolor=ft.Colors.GREEN,
                            border_radius=20,
                            padding=ft.padding.symmetric(
                                horizontal=15, vertical=8),
                            on_click=new_loan_click,
                            ink=True
                        )
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.START
                ),
                **container_style
            )
        )

        track_request_card = ft.Card(
            elevation=5,
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row([
                            ft.Icon(ft.Icons.SEARCH, size=30,
                                    color=ft.Colors.AMBER_700),
                            ft.Text("Acompanhar Solicitação",
                                    weight=ft.FontWeight.BOLD, size=18)
                        ]),
                        ft.Text("Verifique o andamento das suas solicitações",
                                size=14, color=ft.Colors.GREY_700),
                        ft.Container(expand=True),
                        ft.Container(
                            content=ft.Text(
                                "VERIFICAR", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                            bgcolor=ft.Colors.AMBER_700,
                            border_radius=20,
                            padding=ft.padding.symmetric(
                                horizontal=15, vertical=8),
                            on_click=track_request_click,
                            ink=True
                        )
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.START
                ),
                **container_style
            )
        )

        track_loan_card = ft.Card(
            elevation=5,
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row([
                            ft.Icon(ft.Icons.ACCOUNT_BALANCE,
                                    size=30, color=ft.Colors.INDIGO),
                            ft.Text("Acompanhar Empréstimo",
                                    weight=ft.FontWeight.BOLD, size=18)
                        ]),
                        ft.Text("Acompanhe seus empréstimos ativos",
                                size=14, color=ft.Colors.GREY_700),
                        ft.Container(expand=True),
                        ft.Container(
                            content=ft.Text(
                                "GERENCIAR", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                            bgcolor=ft.Colors.INDIGO,
                            border_radius=20,
                            padding=ft.padding.symmetric(
                                horizontal=15, vertical=8),
                            on_click=track_loan_click,
                            ink=True
                        )
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.START
                ),
                **container_style
            )
        )

        # Grid de cards
        card_grid = ft.Row(
            [
                ft.Column([update_profile_card, track_request_card],
                          alignment=ft.MainAxisAlignment.CENTER),
                ft.Column([new_loan_card, track_loan_card],
                          alignment=ft.MainAxisAlignment.CENTER)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=15
        )

        # Layout principal
        content = ft.Column(
            controls=[
                top_bar,
                card_grid
            ],
            spacing=15,
            expand=True
        )

        self.page.clean()
        self.page.add(content)
