import flet as ft
import time


class App:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.duration = 0  # Inicializa a duração como 0
        self.is_playing = False
        self.repetir = False  # Flag de repetição
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
        self.page.theme_mode = ft.ThemeMode.DARK
        self.audio = ft.Audio(
            src="assets\\audios\\tu-tu-tu-du-max-verstappen.mp3",
            volume=0.05,
            on_duration_changed=self.on_duration_changed,
            on_position_changed=self.on_position_changed,
            on_state_changed=self.on_audio_state_changed,  # ← novo!
        )

        self.page.overlay.append(self.audio)

        self.background = ft.Image(
            src="assets\\images\\max-logo.jpg",
            fit=ft.ImageFit.COVER,
            width=self.page.window.width,
            height=self.page.window.height,
        )

        # Inicializa os textos de tempo
        self.txt_start = ft.Text("0:00", color="white")
        self.txt_end = ft.Text(self.format_time(self.duration), color="white")

        # Slider
        self.time_line = ft.Slider(
            min=0,
            max=1,
            value=0,
            interaction=True,  # Deixe o slider interativo
            on_change=self.seek_position,
            divisions=100
        )

        # Botões
        self.play_button = ft.IconButton(
            icon=ft.Icons.PLAY_ARROW_ROUNDED,
            on_click=self.toggle_play_pause  # Agora o método está acessível
        )

        # Botão de repetição
        self.repeat_button = ft.IconButton(
            icon=ft.Icons.REPEAT,
            selected_icon=ft.Icons.REPEAT_ON,
            selected=False,
            on_click=self.toggle_repeat,
            tooltip="Repetir música"
        )

    def toggle_play_pause(self, e):
        """
        Alterna entre reproduzir e pausar a música.
        """
        if self.is_playing:
            self.audio.pause()
            self.play_button.icon = ft.Icons.PLAY_ARROW_ROUNDED
        else:
            self.audio.resume()
            self.play_button.icon = ft.Icons.PAUSE_ROUNDED

        self.is_playing = not self.is_playing
        self.page.update()

    def toggle_repeat(self, e):
        """
        Alterna entre ativar e desativar a repetição.
        """
        self.repetir = not self.repetir
        self.repeat_button.selected = self.repetir
        self.repeat_button.update()

    def format_time(self, segundos):
        return f"{int(segundos) // 60}:{int(segundos) % 60:02d}"

    def on_duration_changed(self, e):
        """
        Atualiza a duração da música quando o evento de mudança de duração é disparado.
        """
        duration = self.audio.get_duration()
        if duration:
            self.duration = duration / 1000  # Atualiza a duração em segundos
            self.time_line.max = self.duration
            self.txt_end.value = self.format_time(
                self.duration)  # Atualiza o texto do tempo final
            self.page.update()

    def on_position_changed(self, e):
        """
        Atualiza a posição do slider com a posição atual da música e verifica a repetição.
        """
        if self.is_playing:
            position = self.audio.get_current_position()
            if position is not None:
                self.time_line.value = position / 1000
                self.time_line.update()

            # Verifica se a música terminou e a repetição está ativada
            # Multiplicado por 1000 para converter em milissegundos
            if self.repetir and position >= self.duration * 1000:
                self.audio.seek(0)  # Recomeça a música
                self.audio.resume()  # Reinicia a reprodução
                self.page.update()

    def seek_position(self, e):
        """
        Muda a posição da música conforme o usuário interage com o slider.
        """
        if self.audio.get_duration() is not None:
            new_position = int(self.time_line.value * 1000)
            self.audio.seek(new_position)
            self.audio.update()

    def on_audio_state_changed(self, e):
        if e.data == "completed":
            if self.repetir:
                self.audio.seek(0)
                self.audio.resume()
                self.is_playing = True
                self.play_button.icon = ft.Icons.PAUSE_ROUNDED
            else:
                self.is_playing = False
                self.play_button.icon = ft.Icons.PLAY_ARROW_ROUNDED
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
                ft.Container(content=self.txt_start,
                             padding=ft.Padding(20, 0, 0, 0)),
                ft.Container(content=self.time_line, expand=True,
                             padding=ft.Padding(10, 4, 10, 0)),
                ft.Container(content=self.txt_end,
                             padding=ft.Padding(0, 0, 20, 0)),
            ],
            alignment="center",
            vertical_alignment="center",
        )

        control_buttons = ft.Row(
            [
                ft.IconButton(
                    icon=ft.Icons.FAST_REWIND_SHARP,
                    on_click=lambda e: self.pular_para(
                        {"data": max(0, self.time_line.value - 5)})
                ),
                self.play_button,
                ft.IconButton(
                    icon=ft.Icons.FAST_FORWARD_SHARP,
                    on_click=lambda e: self.pular_para(
                        {"data": min(self.duration, self.time_line.value + 5)})
                ),
                self.repeat_button  # Adiciona o botão de repetição aqui
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
