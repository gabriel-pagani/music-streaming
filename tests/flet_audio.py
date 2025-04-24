import flet as ft
import pyodbc
import base64


def get_capa_base64(musica_id: int) -> str:
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER=GABRIEL\\SQLSERVER;DATABASE=database;UID=admin;PWD=12345")
    cursor = conn.cursor()
    cursor.execute("SELECT CAPA FROM MUSICAS WHERE ID = ?", musica_id)
    row = cursor.fetchone()
    conn.close()

    if row and row[0]:
        return base64.b64encode(row[0]).decode("utf-8")
    return None


def get_audio_base64(musica_id: int) -> str:
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER=GABRIEL\\SQLSERVER;DATABASE=database;UID=admin;PWD=12345")
    cursor = conn.cursor()
    cursor.execute("SELECT MUSICA FROM MUSICAS WHERE ID = ?", musica_id)
    row = cursor.fetchone()
    conn.close()

    if row and row[0]:
        return base64.b64encode(row[0]).decode("utf-8")
    return None


class App:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.musica_id = 1
        self.is_playing = False
        self.timeline = None
        self.audio = None
        self.setup_page()
        self.show_ui()

    def setup_page(self):
        self.page.title = "Sprobify"
        self.page.window_width = 400
        self.page.window_height = 500
        self.page.window.center()
        self.page.window.resizable = False
        self.page.bgcolor = ft.Colors.WHITE
        self.page.theme_mode = ft.ThemeMode.LIGHT

        audio_base64 = get_audio_base64(self.musica_id)
        self.audio = ft.Audio(
            src_base64=audio_base64,
            volume=0.50,
            on_duration_changed=self.on_duration_changed,
            on_position_changed=self.on_position_changed
        )
        self.page.overlay.append(self.audio)
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

    def show_ui(self):
        capa_base64 = get_capa_base64(self.musica_id)
        capa_image = ft.Image(
            src_base64=capa_base64,
            width=200,
            height=200,
            fit=ft.ImageFit.CONTAIN
        )

        self.timeline = ft.Slider(
            on_change=self.seek_position,
            divisions=100
        )

        def toggle_play_pause(e):
            if self.is_playing:
                self.audio.pause()
                e.control.icon = ft.Icons.PLAY_ARROW
            else:
                self.audio.resume()
                e.control.icon = ft.Icons.PAUSE
            self.is_playing = not self.is_playing
            self.page.update()

        toggle_button = ft.IconButton(
            icon=ft.Icons.PLAY_ARROW,
            icon_size=50,
            on_click=toggle_play_pause
        )

        layout = ft.Column(
            controls=[
                capa_image,
                self.timeline,
                ft.Row([toggle_button], alignment=ft.MainAxisAlignment.CENTER)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

        self.page.add(layout)


def main(page: ft.Page):
    App(page)


if __name__ == "__main__":
    ft.app(target=main)
