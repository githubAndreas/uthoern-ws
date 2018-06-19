from typing import Dict


class Album:

    def __init__(self, name: str, uri: str):
        self.__name = name
        self.__uri = uri

    def get_name(self) -> str:
        return self.__name

    def get_uri(self) -> str:
        return self.__uri

    @staticmethod
    def from_dict(data: Dict) -> 'Album':
        return Album(data['album_name'], data['album_uri'])
