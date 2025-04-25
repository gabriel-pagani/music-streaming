from base64 import b64encode
from src.utils.connection import server_request
from logging import error


class Music:
    def __init__(self, id: int = None, title: str = None, artist: str = None, album: str = None, cover: str = None, music: str = None,
                 is_playing: bool = False, is_random: bool = False, is_looping: bool = False, volume: float = 0.5):
        self.id = id
        self.title = title
        self.artist = artist
        self.album = album
        self.cover = cover
        self.music = music
        self.is_playing = is_playing
        self.is_random = is_random
        self.is_looping = is_looping
        self.volume = volume

    def get_data(self) -> dict:
        try:
            response = server_request(
                query="select * from musicas where id = ?",
                params=(self.id)
            )

            self.title = response['data'][0]['TITULO']
            self.artist = response['data'][0]['ARTISTA']
            self.album = response['data'][0]['ALBUM']
            self.cover = b64encode(response['data'][0]['CAPA']).decode("utf-8")
            self.music = b64encode(
                response['data'][0]['MUSICA']).decode("utf-8")

            return {
                'id': self.id,
                'title': self.title,
                'artist': self.artist,
                'album': self.album,
                'cover': self.cover,
                'music': self.music,
            }

        except Exception as e:
            error(f"Erro ao requisitar informações da música: {e}")
