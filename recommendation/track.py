from typing import Dict


class Track:

    def __init__(self, uri: str):
        self.__uri = uri

    def get_uri(self) -> str:
        return self.__uri

    def get_simplified_uri(self) -> str:
        return self.__uri[14:]

    @staticmethod
    def from_dict(data: Dict) -> 'Track':
        return Track(data['track_uri'])
