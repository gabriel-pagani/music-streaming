import flet as ft
import flet_audio as fta


class App:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.setup_page()
        self.show_page()

    def setup_page(self) -> None:
        self.page.title = 'Sprobify'
        self.page.window.height = 512
        self.page.window.width = 512
        self.page.window.center()
        self.page.window.to_front()
        self.page.window.resizable = False
        self.page.window.maximizable = False
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.bgcolor = ft.Colors.WHITE
        self.page.padding = 0
        self.audio = fta.Audio(
            src="assets\\audios\\tu-tu-tu-du-max-verstappen.mp3",
            volume=10
        )
        self.background = ft.Image(
            src="assets\\images\\max-logo.jpg",
            fit=ft.ImageFit.COVER,
            width=self.page.window.width,
            height=self.page.window.height,
        )
        self.page.overlay.append(self.audio)
        self.page.update()

    def show_page(self) -> None:
        def play(e):
            self.audio.play()

        def pause(e):
            self.audio.pause()

        music_name = ft.Text(
            value="Tu Tu Tu Du - Max Verstappen",
            color=ft.Colors.WHITE,
            size=35,
            font_family="Arial",
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        play_button = ft.IconButton(
            icon=ft.Icons.PLAY_ARROW,
            icon_color=ft.Colors.WHITE,
            icon_size=50,
            bgcolor=ft.Colors.GREEN_900,
            on_click=play,
        )

        stop_button = ft.IconButton(
            icon=ft.Icons.PAUSE,
            icon_color=ft.Colors.WHITE,
            icon_size=50,
            bgcolor=ft.Colors.RED_900,
            on_click=pause,
        )


        # Layout
        content = ft.Row(
            controls=[
                play_button,
                stop_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )

        container = ft.Container(
            content=content,
            expand=True,  # Garante que o container ocupe todo o espaço disponível
            alignment=ft.alignment.bottom_center,  # Alinha o conteúdo na parte inferior e centralizado
            padding=ft.Padding(0, 0, 0, 50)  # Adiciona um espaçamento de 50px acima da borda inferior
        )

        music_name_container = ft.Container(
            content=music_name,
            alignment=ft.alignment.top_center,  # Alinha o texto no topo e centralizado
            padding=ft.Padding(10, 70, 10, 0),  # Adiciona espaçamento no topo
            expand=True
)

        # Use Stack to overlay the background and controls
        layout = ft.Stack(
            controls=[
                self.background,
                music_name_container,  # Background image
                container         # Botões centralizados
            ],
            expand=True  # Garante que o Stack ocupe todo o espaço da página
        )

        self.page.add(layout)
        self.page.update()

def main(page: ft.Page) -> None:
    App(page)


if __name__ == "__main__":
    ft.app(target=main, assets_dir='assets')
