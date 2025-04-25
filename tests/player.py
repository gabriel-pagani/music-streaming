import flet as ft
from src.controller.music import Music


class App:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.music = Music(id=2)
        self.playlist = []
        self.audio = None
        self.timeline = None
        self.setup_page()
        self.load_playlist()
        self.initialize_audio()
        self.show_interface()

    def setup_page(self) -> None:
        """Configura as propriedades básicas da página"""
        self.page.title = 'Sprobify'
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.bgcolor = ft.Colors.WHITE
        self.page.padding = 0
        self.page.update()

    def load_playlist(self) -> None:
        """Carrega músicas do banco de dados"""
        self.playlist = [
            Music(id=1).get_data(),
            Music(id=2).get_data(),
            Music(id=3).get_data(),
            Music(id=4).get_data(),
        ]

    def initialize_audio(self) -> None:
        """Inicializa o componente de áudio"""
        self.audio = ft.Audio(
            src_base64=self.playlist[self.music.id - 1]['music'],
            volume=self.music.volume,
            on_duration_changed=self.on_duration_changed,
            on_position_changed=self.on_position_changed
        )
        self.page.overlay.append(self.audio)
        self.page.update()

    def on_duration_changed(self, e) -> None:
        """Callback quando a duração da música é detectada"""
        duration = self.audio.get_duration()
        if duration and self.timeline:
            self.timeline.max = duration / 1000
            self.page.update()

    def on_position_changed(self, e) -> None:
        """Callback para atualizar a posição da timeline durante a reprodução"""
        if self.music.is_playing and self.timeline:
            position = self.audio.get_current_position()
            if position is not None:
                self.timeline.value = position / 1000
                self.timeline.update()

    def seek_position(self, e) -> None:
        """Altera a posição de reprodução da música"""
        if self.audio.get_duration() is not None:
            new_position = int(self.timeline.value * 1000)
            self.audio.seek(new_position)
            self.audio.update()

    def show_interface(self) -> None:
        """Cria e exibe a interface do player"""
        # ELEMENTOS DA INTERFACE

        # 1. COMPONENTES DO PLAYER DE MÚSICA

        # 1.1 Exibição de informações da música atual
        current_music = self.playlist[self.music.id - 1]

        music_title = ft.Text(
            current_music['title'] if self.playlist else "Sem música",
            weight=ft.FontWeight.BOLD,
            size=16,
            overflow=ft.TextOverflow.ELLIPSIS
        )

        artist_name = ft.Text(
            current_music['artist'] if self.playlist else "",
            size=14,
            color=ft.Colors.GREY_800,
            overflow=ft.TextOverflow.ELLIPSIS
        )

        album_name = ft.Text(
            current_music['album'] if self.playlist else "",
            size=12,
            color=ft.Colors.GREY_600,
            overflow=ft.TextOverflow.ELLIPSIS
        )

        # 1.2 Timeline para navegação na música
        self.timeline = ft.Slider(
            min=0,
            max=100,  # Será atualizado quando a música carregar
            value=0,
            on_change=self.seek_position,
            thumb_color=ft.Colors.BLUE_900,
            active_color=ft.Colors.BLUE_900,
            inactive_color=ft.Colors.BLUE_100,
            tooltip="Posição"
        )

        # 1.3 Controles de reprodução

        # Botões de controle
        random_button = ft.IconButton(
            icon=ft.Icons.SHUFFLE,
            icon_color=ft.Colors.GREY,
            on_click=self.toggle_shuffle,
            tooltip="Aleatório"
        )

        previous_button = ft.IconButton(
            icon=ft.Icons.SKIP_PREVIOUS,
            icon_color=ft.Colors.BLUE_900,
            on_click=self.skip_previous,
            tooltip="Anterior"
        )

        play_button = ft.IconButton(
            icon=ft.Icons.PLAY_ARROW,
            icon_color=ft.Colors.BLUE_900,
            icon_size=40,
            on_click=self.play_pause,
            tooltip="Reproduzir/Pausar"
        )

        next_button = ft.IconButton(
            icon=ft.Icons.SKIP_NEXT,
            icon_color=ft.Colors.BLUE_900,
            on_click=self.skip_next,
            tooltip="Próxima"
        )

        loop_button = ft.IconButton(
            icon=ft.Icons.LOOP,
            icon_color=ft.Colors.GREY,
            on_click=self.toggle_loop,
            tooltip="Repetir"
        )

        # 1.4 Controle de volume
        volume_slider = ft.Slider(
            min=0,
            max=100,
            value=self.music.volume * 100,  # Convert 0-1 to 0-100
            thumb_color=ft.Colors.BLUE_900,
            active_color=ft.Colors.BLUE_900,
            on_change=self.change_volume,
            tooltip="Volume"
        )

        volume_icon = ft.Icon(
            name=ft.Icons.VOLUME_UP,
            color=ft.Colors.BLUE_900,
        )

        # 1.5 Capa do álbum
        album_cover = ft.Image(
            src_base64=current_music['cover'],
            width=60,
            height=60,
            fit=ft.ImageFit.COVER,
            border_radius=10
        ) if current_music.get('cover') else ft.Container(
            width=60,
            height=60,
            bgcolor=ft.Colors.BLUE_200,
            border_radius=10,
            content=ft.Icon(ft.Icons.MUSIC_NOTE, color=ft.Colors.BLUE_900),
            alignment=ft.alignment.center
        )

        # 2. CABEÇALHO
        user_greeting = ft.Text(
            f"Olá, Gabriel!",
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
                    on_click=self.update_account,
                ),
                ft.PopupMenuItem(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.LOGOUT),
                            ft.Text("Sair"),
                        ]
                    ),
                    on_click=self.logout,
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

        # 3. ORGANIZAÇÃO DOS CONTROLES EM LAYOUTS

        # 3.1 Informações da música
        music_info = ft.Column(
            [music_title, artist_name, album_name],
            spacing=2,
            tight=True
        )

        # 3.2 Controles de reprodução
        player_controls = ft.Row(
            [random_button, previous_button, play_button, next_button, loop_button],
            alignment=ft.MainAxisAlignment.CENTER
        )

        # 3.3 Controle de volume
        volume_control = ft.Row(
            [volume_icon, volume_slider],
            spacing=0
        )

        # 3.4 Layout do player completo
        music_player = ft.Container(
            content=ft.Column(
                [
                    # Timeline
                    self.timeline,
                    ft.Container(height=10),

                    # Player completo
                    ft.Row(
                        [
                            # Capa e informações da música
                            ft.Row(
                                [
                                    album_cover,
                                    ft.Container(width=10),
                                    music_info
                                ],
                                vertical_alignment=ft.CrossAxisAlignment.CENTER
                            ),

                            ft.Container(expand=True),

                            # Controles de reprodução
                            player_controls,

                            ft.Container(expand=True),

                            # Controle de volume
                            volume_control
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                ]
            ),
            padding=ft.padding.all(15),
            border_radius=ft.border_radius.only(top_left=10, top_right=10),
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_300),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                offset=ft.Offset(0, -3)
            )
        )

        # 4. LISTA DE REPRODUÇÃO
        playlist_items = [self.create_playlist_item(
            music) for music in self.playlist]

        playlist_column = ft.ListView(
            playlist_items,
            spacing=5,
            auto_scroll=True,
            height=self.page.height - 353
        )
        self.page.on_resized = lambda e: self.resize_list_view(
            e, playlist_column)

        playlist_container = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Biblioteca de Músicas", size=20,
                            weight=ft.FontWeight.BOLD),
                    ft.Container(height=10),
                    playlist_column
                ]
            ),
            padding=ft.padding.all(20),
            expand=True
        )

        # 5. LAYOUT PRINCIPAL COMPLETO
        content = ft.Column(
            controls=[
                top_bar,
                playlist_container,
                music_player
            ],
            spacing=0
        )

        # Adicionando à página
        self.page.clean()
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.add(content)

    # MÉTODOS DE CONTROLE DO PLAYER

    def update_music_display(self) -> None:
        """Atualiza a exibição com os dados da música atual"""
        if self.playlist:
            current = self.playlist[self.music.id - 1]
            # Atualizar labels
            for control in self.page.controls[0].controls:
                if isinstance(control, ft.Container) and control.content and isinstance(control.content, ft.Column):
                    for child in control.content.controls:
                        if isinstance(child, ft.Column) and len(child.controls) > 0:
                            if isinstance(child.controls[0], ft.Text) and child.controls[0].value == "Biblioteca de Músicas":
                                # Não faça nada
                                pass

            # Atualizar áudio
            self.audio.src_base64 = current['music']
            self.audio.update()
            self.page.update()

    def play_pause(self, e) -> None:
        """Alterna entre reproduzir e pausar a música"""
        self.music.is_playing = not self.music.is_playing
        if self.music.is_playing:
            e.control.icon = ft.Icons.PAUSE
            self.audio.resume()
        else:
            e.control.icon = ft.Icons.PLAY_ARROW
            self.audio.pause()
        self.page.update()

    def skip_next(self, e) -> None:
        """Avança para a próxima música"""
        playlist_len = len(self.playlist)
        if playlist_len > 0:
            if self.music.is_random:
                import random
                self.music.id = random.randint(1, playlist_len)
            else:
                self.music.id = (self.music.id % playlist_len) + 1

            # Atualizar com a nova música
            current_music = self.playlist[self.music.id - 1]
            self.audio.src_base64 = current_music['music']
            self.audio.update()

            # Reiniciar timeline
            if self.timeline:
                self.timeline.value = 0

            # Se estiver tocando, continua tocando a próxima música
            if self.music.is_playing:
                self.audio.play()

            self.update_music_display()

    def skip_previous(self, e) -> None:
        """Volta para a música anterior"""
        playlist_len = len(self.playlist)
        if playlist_len > 0:
            if self.music.is_random:
                import random
                self.music.id = random.randint(1, playlist_len)
            else:
                self.music.id = (self.music.id - 2) % playlist_len + 1

            # Atualizar com a nova música
            current_music = self.playlist[self.music.id - 1]
            self.audio.src_base64 = current_music['music']
            self.audio.update()

            # Reiniciar timeline
            if self.timeline:
                self.timeline.value = 0

            # Se estiver tocando, continua tocando a música anterior
            if self.music.is_playing:
                self.audio.play()

            self.update_music_display()

    def toggle_shuffle(self, e) -> None:
        """Alterna o modo aleatório"""
        self.music.is_random = not self.music.is_random
        if self.music.is_random:
            e.control.icon_color = ft.Colors.BLUE_900
        else:
            e.control.icon_color = ft.Colors.GREY
        self.page.update()

    def toggle_loop(self, e) -> None:
        """Alterna o modo de repetição"""
        self.music.is_looping = not self.music.is_looping
        if self.music.is_looping:
            e.control.icon_color = ft.Colors.BLUE_900
        else:
            e.control.icon_color = ft.Colors.GREY
        self.page.update()

    def change_volume(self, e) -> None:
        """Altera o volume do player"""
        volume_value = e.control.value
        self.music.volume = volume_value / 100  # Convert 0-100 to 0-1

        # Atualizar o volume no componente de áudio
        self.audio.volume = self.music.volume
        self.audio.update()

        # Atualizar ícone de volume conforme valor
        volume_icon = e.control.parent.controls[0]
        if volume_value == 0:
            volume_icon.name = ft.Icons.VOLUME_OFF
        elif volume_value < 50:
            volume_icon.name = ft.Icons.VOLUME_DOWN
        else:
            volume_icon.name = ft.Icons.VOLUME_UP
        self.page.update()

    def resize_list_view(self, e, playlist_column) -> None:
        """Ajusta o tamanho da lista de reprodução conforme o tamanho da janela"""
        available_height = self.page.height - 353
        playlist_column.height = max(75, available_height)
        self.page.update()

    def create_playlist_item(self, music) -> ft.Container:
        """Cria um item para a lista de reprodução"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        width=40,
                        height=40,
                        bgcolor=ft.Colors.BLUE_100,
                        border_radius=5,
                        content=ft.Icon(ft.Icons.MUSIC_NOTE,
                                        size=20, color=ft.Colors.BLUE_900),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(width=10),
                    ft.Column(
                        [
                            ft.Text(music['title'],
                                    weight=ft.FontWeight.BOLD),
                            ft.Text(f"{music['artist']} • {music['album']}",
                                    size=12, color=ft.Colors.GREY_700)
                        ],
                        spacing=2,
                        tight=True
                    ),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.PLAY_CIRCLE,
                        icon_color=ft.Colors.BLUE_900,
                        on_click=lambda e, id=music['id']: self.play_selected_music(
                            e, id)
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=ft.padding.all(10),
            margin=ft.margin.only(bottom=5),
            border_radius=5,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_300),
        )

    def play_selected_music(self, e, music_id) -> None:
        """Reproduz uma música selecionada da lista"""
        # Música selecionada
        self.music.id = music_id

        # Atualizar interface com nova música
        current_music = self.playlist[self.music.id - 1]
        self.audio.src_base64 = current_music['music']
        self.audio.update()

        # Iniciar a reprodução
        self.music.is_playing = True

        # Atualizar botão de play
        for control in self.page.controls[0].controls:
            if isinstance(control, ft.Container) and control.content and isinstance(control.content, ft.Column):
                for column_control in control.content.controls:
                    if isinstance(column_control, ft.Row):
                        for row_control in column_control.controls:
                            if isinstance(row_control, ft.IconButton) and row_control.tooltip == "Reproduzir/Pausar":
                                row_control.icon = ft.Icons.PAUSE
                                break

        # Tocar música
        self.audio.play()
        self.update_music_display()

    def update_account(self, e) -> None:
        """Atualiza as informações da conta"""
        pass

    def logout(self, e) -> None:
        """Realiza logout do sistema"""
        pass


def main(page: ft.Page) -> None:
    App(page)


if __name__ == "__main__":
    ft.app(target=main, assets_dir='assets', view=ft.WEB_BROWSER)
