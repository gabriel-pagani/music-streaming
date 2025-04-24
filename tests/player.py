import flet as ft


class App:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.setup_page()
        self.show_interface()

    def setup_page(self) -> None:
        self.page.title = 'Sprobify'
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.bgcolor = ft.Colors.WHITE
        self.page.padding = 0
        self.page.update()

    def show_interface(self) -> None:
        # Classe para representar uma música do banco de dados
        class Music:
            def __init__(self, id, title, artist, album, cover_url, file_path):
                self.id = id
                self.title = title
                self.artist = artist
                self.album = album
                self.cover_url = cover_url
                self.file_path = file_path

        # Estado do player
        class PlayerState:
            def __init__(self):
                self.current_music_index = 0
                self.is_playing = False
                self.is_shuffle = False
                self.is_loop = False
                self.volume = 50
                self.playlist = []

        # Instanciando o estado do player
        self.player_state = PlayerState()

        # Função para simular o carregamento de músicas do banco de dados
        def load_music_from_db():
            # Simulação de dados que viriam do banco de dados
            # Na implementação real, substitua isso por uma consulta ao banco
            return [
                Music(1, "Bohemian Rhapsody", "Queen",
                      "A Night at the Opera", None, "/path/to/music1.mp3"),
                Music(2, "Imagine", "John Lennon", "Imagine",
                      None, "/path/to/music2.mp3"),
                Music(3, "Shape of You", "Ed Sheeran",
                      "÷", None, "/path/to/music3.mp3"),
                Music(4, "Billie Jean", "Michael Jackson",
                      "Thriller", None, "/path/to/music4.mp3"),
                Music(1, "Bohemian Rhapsody", "Queen",
                      "A Night at the Opera", None, "/path/to/music1.mp3"),
                Music(2, "Imagine", "John Lennon", "Imagine",
                      None, "/path/to/music2.mp3"),
                Music(3, "Shape of You", "Ed Sheeran",
                      "÷", None, "/path/to/music3.mp3"),
                Music(4, "Billie Jean", "Michael Jackson",
                      "Thriller", None, "/path/to/music4.mp3"),
                Music(1, "Bohemian Rhapsody", "Queen",
                      "A Night at the Opera", None, "/path/to/music1.mp3"),
                Music(3, "Shape of You", "Ed Sheeran",
                      "÷", None, "/path/to/music3.mp3"),
                Music(4, "Billie Jean", "Michael Jackson",
                      "Thriller", None, "/path/to/music4.mp3"),
                Music(1, "Bohemian Rhapsody", "Queen",
                      "A Night at the Opera", None, "/path/to/music1.mp3"),
            ]

        # Carregando as músicas
        self.player_state.playlist = load_music_from_db()
        current_music = self.player_state.playlist[self.player_state.current_music_index]

        # Funções de navegação
        def update_account(e):
            pass

        def logout(e):
            pass

        # Funções para controle do player de música
        def update_music_display():
            if self.player_state.playlist:
                current = self.player_state.playlist[self.player_state.current_music_index]
                music_title.value = current.title
                artist_name.value = current.artist
                album_name.value = current.album

                # Aqui você pode atualizar a capa do álbum se tiver URL
                # album_cover.src = current.cover_url if current.cover_url else None

                self.page.update()

        def play_pause(e):
            self.player_state.is_playing = not self.player_state.is_playing
            if self.player_state.is_playing:
                play_button.icon = ft.Icons.PAUSE
                # Aqui você implementaria a lógica para tocar a música
                # player.play(current_music.file_path)
            else:
                play_button.icon = ft.Icons.PLAY_ARROW
                # Aqui você implementaria a lógica para pausar a música
                # player.pause()
            self.page.update()

        def skip_next(e):
            playlist_len = len(self.player_state.playlist)
            if playlist_len > 0:
                if self.player_state.is_shuffle:
                    import random
                    self.player_state.current_music_index = random.randint(
                        0, playlist_len - 1)
                else:
                    self.player_state.current_music_index = (
                        self.player_state.current_music_index + 1) % playlist_len

                update_music_display()

                # Se estiver tocando, continua tocando a próxima música
                if self.player_state.is_playing:
                    # Lógica para tocar a música
                    pass

        def skip_previous(e):
            playlist_len = len(self.player_state.playlist)
            if playlist_len > 0:
                if self.player_state.is_shuffle:
                    import random
                    self.player_state.current_music_index = random.randint(
                        0, playlist_len - 1)
                else:
                    self.player_state.current_music_index = (
                        self.player_state.current_music_index - 1) % playlist_len

                update_music_display()

                # Se estiver tocando, continua tocando a música anterior
                if self.player_state.is_playing:
                    # Lógica para tocar a música
                    pass

        def toggle_shuffle(e):
            self.player_state.is_shuffle = not self.player_state.is_shuffle
            if self.player_state.is_shuffle:
                random_button.icon_color = ft.Colors.BLUE_900
            else:
                random_button.icon_color = ft.Colors.GREY
            self.page.update()

        def toggle_loop(e):
            self.player_state.is_loop = not self.player_state.is_loop
            if self.player_state.is_loop:
                loop_button.icon_color = ft.Colors.BLUE_900
            else:
                loop_button.icon_color = ft.Colors.GREY
            self.page.update()

        def change_volume(e):
            self.player_state.volume = int(volume_slider.value)
            # Implemente a lógica para alterar o volume no player real
            # player.set_volume(self.player_state.volume)

            # Atualizar ícone de volume conforme valor
            if self.player_state.volume == 0:
                volume_icon.name = ft.Icons.VOLUME_OFF
            elif self.player_state.volume < 50:
                volume_icon.name = ft.Icons.VOLUME_DOWN
            else:
                volume_icon.name = ft.Icons.VOLUME_UP
            self.page.update()

        def resize_list_view(e):
            available_height = self.page.height - 275
            playlist_column.height = max(75, available_height)
            self.page.update()

        # Cabeçalho com saudação e menu
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

        # Player de música com melhor organização para responsividade
        music_title = ft.Text(
            current_music.title if self.player_state.playlist else "Sem música",
            weight=ft.FontWeight.BOLD,
            size=16,
            overflow=ft.TextOverflow.ELLIPSIS
        )

        artist_name = ft.Text(
            current_music.artist if self.player_state.playlist else "",
            size=14,
            color=ft.Colors.GREY_800,
            overflow=ft.TextOverflow.ELLIPSIS
        )

        album_name = ft.Text(
            current_music.album if self.player_state.playlist else "",
            size=12,
            color=ft.Colors.GREY_600,
            overflow=ft.TextOverflow.ELLIPSIS
        )

        # Botões de controle
        random_button = ft.IconButton(
            icon=ft.Icons.SHUFFLE,
            icon_color=ft.Colors.GREY,
            on_click=toggle_shuffle,
            tooltip="Aleatório"
        )

        previous_button = ft.IconButton(
            icon=ft.Icons.SKIP_PREVIOUS,
            icon_color=ft.Colors.BLUE_900,
            on_click=skip_previous,
            tooltip="Anterior"
        )

        play_button = ft.IconButton(
            icon=ft.Icons.PLAY_ARROW,
            icon_color=ft.Colors.BLUE_900,
            icon_size=40,
            on_click=play_pause,
            tooltip="Reproduzir/Pausar"
        )

        next_button = ft.IconButton(
            icon=ft.Icons.SKIP_NEXT,
            icon_color=ft.Colors.BLUE_900,
            on_click=skip_next,
            tooltip="Próxima"
        )

        loop_button = ft.IconButton(
            icon=ft.Icons.LOOP,
            icon_color=ft.Colors.GREY,
            on_click=toggle_loop,
            tooltip="Repetir"
        )

        # Controle de volume
        volume_slider = ft.Slider(
            min=0,
            max=100,
            value=self.player_state.volume,
            thumb_color=ft.Colors.BLUE_900,
            active_color=ft.Colors.BLUE_900,
            on_change=change_volume,
            tooltip="Volume"
        )

        volume_icon = ft.Icon(
            name=ft.Icons.VOLUME_UP,
            color=ft.Colors.BLUE_900,
        )

        # Capa do álbum (representada por um container)
        album_cover = ft.Container(
            width=60,
            height=60,
            bgcolor=ft.Colors.BLUE_200,
            border_radius=10,
            content=ft.Icon(ft.Icons.MUSIC_NOTE, color=ft.Colors.BLUE_900),
            alignment=ft.alignment.center
        )

        # Layout responsivo do player
        music_info = ft.Column(
            [music_title, artist_name, album_name],
            spacing=2,
            tight=True
        )

        player_controls = ft.Row(
            [random_button, previous_button, play_button, next_button, loop_button],
            alignment=ft.MainAxisAlignment.CENTER
        )

        volume_control = ft.Row(
            [volume_icon, volume_slider],
            spacing=0
        )

        # Player responsivo adaptado para diferentes tamanhos de tela
        music_player = ft.Container(
            content=ft.Row(
                [
                    # Capa e informações da música
                    ft.Column(
                        [
                            ft.Row([
                                album_cover,
                                ft.Container(width=10),
                                music_info
                            ], vertical_alignment=ft.CrossAxisAlignment.CENTER)
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.START
                    ),

                    # Controles de reprodução
                    ft.Column(
                        [player_controls],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),

                    # Controle de volume
                    ft.Column(
                        [volume_control],
                        horizontal_alignment=ft.CrossAxisAlignment.END
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
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

        # Lista de reprodução
        def create_playlist_item(music):
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
                                ft.Text(music.title,
                                        weight=ft.FontWeight.BOLD),
                                ft.Text(f"{music.artist} • {music.album}",
                                        size=12, color=ft.Colors.GREY_700)
                            ],
                            spacing=2,
                            tight=True
                        ),
                        ft.Container(expand=True),
                        ft.IconButton(
                            icon=ft.Icons.PLAY_CIRCLE,
                            icon_color=ft.Colors.BLUE_900,
                            on_click=lambda e, idx=music.id: play_selected_music(
                                e, idx)
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

        def play_selected_music(e, music_id):
            # Encontrar o índice da música pelo ID
            for i, music in enumerate(self.player_state.playlist):
                if music.id == music_id:
                    self.player_state.current_music_index = i
                    update_music_display()
                    # Iniciar a reprodução
                    self.player_state.is_playing = True
                    play_button.icon = ft.Icons.PAUSE
                    self.page.update()
                    # Aqui implementaria a lógica para tocar a música
                    break

        # Criação da lista de reprodução
        playlist_items = [create_playlist_item(
            music) for music in self.player_state.playlist]

        playlist_column = ft.ListView(
            playlist_items,
            spacing=5,
            auto_scroll=True,
            height=self.page.height - 275
        )
        self.page.on_resized = resize_list_view

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

        # Layout principal responsivo
        content = ft.Column(
            controls=[
                top_bar,
                playlist_container,
                music_player
            ],
            spacing=0
        )

        self.page.clean()
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.add(content)

        # Inicializa o display com a música atual
        update_music_display()


def main(page: ft.Page) -> None:
    App(page)


if __name__ == "__main__":
    ft.app(target=main, assets_dir='assets', view=ft.WEB_BROWSER)
