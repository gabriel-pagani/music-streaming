import flet as ft


def main(page: ft.Page):
    page.title = 'Login'
    page.window.width = 550
    page.window.min_width = 550
    page.window.height = 450
    page.window.min_height = 450
    page.window.center()
    page.window.to_front()
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE
    page.window.icon = r'icons\logo.ico'
    page.update()

    # Texts
    title = ft.Text(
        value='Login',
        size=50,
        color=ft.Colors.BLUE_900
    )

    # TextFields
    email_input = ft.TextField(
        label='Email',
        prefix_icon=ft.Icons.PERSON,
        hint_text='Digite seu email aqui...',
        width=450
    )
    password_input = ft.TextField(
        label='Senha',
        prefix_icon=ft.Icons.LOCK,
        hint_text='Digite sua senha aqui...',
        width=450,
        password=True,
        can_reveal_password=True
    )

    # Buttons
    create_account = ft.TextButton(
        text='Criar Conta',
        on_click=...,
    )
    login_button = ft.ElevatedButton(
        text='Entrar',
        width=450,
        height=50,
        bgcolor=ft.Colors.BLUE_900,
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=5)
        ),
        on_click=...,
    )

    # Positions
    line_create_account = ft.Row(
        controls=[create_account],
        alignment=ft.MainAxisAlignment.END,
        width=450
    )

    column = ft.Column(
        controls=[
            title,
            email_input,
            password_input,
            line_create_account,
            login_button
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    container = ft.Container(
        content=column,
        expand=True,
        alignment=ft.alignment.center
    )

    page.add(container)


ft.app(target=main, assets_dir='assets')
