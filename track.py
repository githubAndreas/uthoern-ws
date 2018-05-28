from album import Album
from artist import Artist
from typing import Dict


class Track:

    def __init__(self, name: str, uri: str, pos: int, artist: str, album: str, duration: str):
        self.__name = name
        self.__uri = uri
        self.__pos = pos
        self.__artist = artist
        self.__album = album
        self.__duration = duration

    def get_name(self) -> str:
        return self.__name

    def get_uri(self) -> str:
        return self.__uri

    def get_simplified_uri(self)-> str:
        return self.__uri[14:]

    def get_pos(self) -> int:
        return self.__pos

    def get_artist(self) -> str:
        return self.__artist

    def get_album(self) -> str:
        return self.__album

    def get_duration(self) -> str:
        return self.__duration

    @staticmethod
    def from_dict(data: Dict) -> 'Track':
        album = Album.from_dict(data)
        artist = Artist.from_dict(data)

        return Track(data['track_name'], data['track_uri'], int(data['pos']), artist, album, data['duration_ms'])
