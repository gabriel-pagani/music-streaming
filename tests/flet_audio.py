import flet as ft


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
        self.audio = ft.Audio(
            src="assets\\audios\\audio.mp3",
            volume=0.05,
            on_duration_changed=self.on_duration_changed,
            on_position_changed=self.on_position_changed
        )
        self.page.overlay.append(self.audio)
        self.is_playing = False
        self.timeline = None
        self.page.update()

    def on_duration_changed(self, e):
        duration = self.audio.get_duration()
        if duration:
            self.timeline.max = duration / 1000
            self.page.update()

    def on_position_changed(self, e):
        if self.is_playing:
            position = self.audio.get_current_position()
            if position is not None:
                self.timeline.value = position / 1000
                self.timeline.update()

    def seek_position(self, e):
        if self.audio.get_duration() is not None:
            new_position = int(self.timeline.value * 1000)
            self.audio.seek(new_position)
            self.audio.update()

    def show_page(self) -> None:
        def toggle_play_pause(e):
            if self.is_playing:
                self.audio.pause()
                e.control.icon = ft.Icons.PLAY_ARROW
            else:
                self.audio.resume()
                e.control.icon = ft.Icons.PAUSE

            self.is_playing = not self.is_playing
            self.page.update()

        self.timeline = ft.Slider(
            on_change=self.seek_position,
            divisions=100
        )

        toggle_button = ft.IconButton(
            icon=ft.Icons.PLAY_ARROW,
            icon_size=50,
            on_click=toggle_play_pause,
        )

        # Layout
        content_row = ft.Row(
            controls=[
                toggle_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )

        content_column = ft.Column(
            controls=[
                self.timeline,
                content_row,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0
        )

        container = ft.Container(
            content=content_column,
            expand=True,
            alignment=ft.alignment.center
        )

        self.page.add(container)


def main(page: ft.Page) -> None:
    App(page)


if __name__ == "__main__":
    ft.app(target=main, assets_dir='assets')
