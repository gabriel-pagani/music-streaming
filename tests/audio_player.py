import flet as ft
import pygame
import threading
import time
from mutagen.mp3 import MP3


class App:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.start = 0
        self.is_playing = False
        self.setup_page()
        self.show_page()
        self.ja_iniciou = False
        self.atualizando = False
        self.repetir = False

    def setup_page(self) -> None:
        pygame.mixer.init()
        self.CAMINHO_MUSICA = "assets\\audios\\tu-tu-tu-du-max-verstappen.mp3"
        self.audio = MP3(self.CAMINHO_MUSICA)
        self.duration = int(self.audio.info.length)

        self.page.title = 'Sprobify'
        self.page.window.height = 540
        self.page.window.width = 540
        self.page.window.center()
        self.page.window.to_front()
        self.page.window.resizable = False
        self.page.window.maximizable = False
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.bgcolor = ft.Colors.WHITE
        self.page.padding = 0

        self.background = ft.Image(
            src="assets\\images\\max-logo.jpg",
            fit=ft.ImageFit.COVER,
            width=self.page.window.width,
            height=self.page.window.height,
        )

        self.txt_start = ft.Text("0:00", color="white")
        self.txt_end = ft.Text(self.format_time(self.duration), color="white")

        self.time_line = ft.Slider(
            min=0,
            max=self.duration,
            value=0,
            divisions=self.duration,
            expand=True,
            on_change_end=self.pular_para,
        )

        self.play_button = ft.IconButton(
            icon=ft.icons.PLAY_ARROW_ROUNDED,
            on_click=self.toggle_play_pause
        )

        self.repeat_button = ft.IconButton(
            icon=ft.icons.REPEAT,
            selected_icon=ft.icons.REPEAT_ON,
            selected=False,
            on_click=self.toggle_repeat,
            tooltip="Repetir música"
        )

    def toggle_repeat(self, e):
        self.repetir = not self.repetir
        self.repeat_button.selected = self.repetir
        self.repeat_button.update()

    def format_time(self, segundos):
        return f"{int(segundos) // 60}:{int(segundos) % 60:02d}"

    def toggle_play_pause(self, event=None):
        self.is_playing = not self.is_playing

        if self.is_playing:
            self.play_button.icon = ft.icons.PAUSE_ROUNDED
            if not self.ja_iniciou:
                pygame.mixer.music.load(self.CAMINHO_MUSICA)
                pygame.mixer.music.play()
                self.ja_iniciou = True
            else:
                pygame.mixer.music.unpause()

            if not self.atualizando:
                threading.Thread(target=self.atualizar_slider, daemon=True).start()
        else:
            self.play_button.icon = ft.icons.PLAY_ARROW_ROUNDED
            pygame.mixer.music.pause()

        self.play_button.update()

    def atualizar_slider(self):
        self.atualizando = True
        while self.atualizando:
            if self.is_playing:
                posicao = pygame.mixer.music.get_pos() // 1000
                self.time_line.value = posicao
                self.txt_start.value = self.format_time(posicao)
                self.page.update()

                if posicao >= self.duration:
                    if self.repetir:
                        pygame.mixer.music.play()
                    else:
                        self.is_playing = False
                        self.play_button.icon = ft.icons.PLAY_ARROW_ROUNDED
                        self.play_button.update()
                        self.atualizando = False
            time.sleep(1)

    def pular_para(self, e):
        segundos = int(e.data)
        pygame.mixer.music.stop()
        pygame.mixer.music.play(start=segundos)
        self.time_line.value = segundos
        self.txt_start.value = self.format_time(segundos)
        self.page.update()

    def show_page(self) -> None:
        music_name = ft.Text(
            value="Tu Tu Tu Du - Max Verstappen",
            color=ft.Colors.WHITE,
            size=30,
            font_family="Arial",
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        timeline_section = ft.Row(
            [
                ft.Container(content=self.txt_start, padding=ft.Padding(20, 0, 0, 0)),
                ft.Container(content=self.time_line, expand=True, padding=ft.Padding(10, 4, 10, 0)),
                ft.Container(content=self.txt_end, padding=ft.Padding(0, 0, 20, 0)),
            ],
            alignment="center",
            vertical_alignment="center",
        )

        control_buttons = ft.Row(
            [
                ft.IconButton(
                    icon=ft.icons.FAST_REWIND_SHARP,
                    on_click=lambda e: self.pular_para({"data": max(0, self.time_line.value - 5)})
                ),
                self.play_button,
                ft.IconButton(
                    icon=ft.icons.FAST_FORWARD_SHARP,
                    on_click=lambda e: self.pular_para({"data": min(self.duration, self.time_line.value + 5)})
                ),
                self.repeat_button
            ],
            alignment="spaceEvenly",
        )

        layout = ft.Stack(
            controls=[
                self.background,
                ft.Container(
                    content=music_name,
                    alignment=ft.alignment.top_center,
                    padding=ft.Padding(10, 70, 10, 0),
                ),
                ft.Container(
                    content=timeline_section,
                    alignment=ft.alignment.center,
                    padding=ft.Padding(0, 240, 0, 0),
                ),
                ft.Container(
                    content=control_buttons,
                    alignment=ft.alignment.bottom_center,
                    padding=ft.Padding(0, 0, 0, 50),
                ),
            ],
            expand=True,
        )

        self.page.add(layout)
        self.page.update()


def main(page: ft.Page) -> None:
    App(page)


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
