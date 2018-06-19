from typing import Dict


class Artist:

    def __init__(self, name: str, uri: str):
        self.__name = name
        self.__uri = uri

    def get_name(self) -> str:
        return self.__name

    def get_uri(self) -> str:
        return self.__uri

    @staticmethod
    def from_dict(data: Dict) -> 'Artit':
        return Artist(data['artist_name'], data['artist_uri'])
