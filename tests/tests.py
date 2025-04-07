import flet as ft
import flet_audio as fta


class App:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.setup_page()
        self.show_page()

    def setup_page(self) -> None:
        self.page.title = 'Sprobify'
        self.page.window.height = 400
        self.page.window.width = 400
        self.page.window.center()
        self.page.window.to_front()
        self.page.window.resizable = False
        self.page.window.maximizable = False
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.bgcolor = ft.Colors.WHITE
        self.audio = fta.Audio(
            src="assets\\audios\\audio.mp3",
            volume=10
        )
        self.page.overlay.append(self.audio)
        self.page.update()

    def show_page(self) -> None:
        def play(e):
            self.audio.play()

        def pause(e):
            self.audio.pause()

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
            expand=True,
            alignment=ft.alignment.center
        )

        self.page.add(container)


def main(page: ft.Page) -> None:
    App(page)


if __name__ == "__main__":
    ft.app(target=main, assets_dir='assets')
