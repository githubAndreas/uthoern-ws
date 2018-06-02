from track import Track
from typing import List, Dict


class Playlist:

    def __init__(self, pid: int, tracks: List[Track]):
        self.__pid = pid
        self.__tracks = tracks

    def get_pid(self) -> int:
        return self.__pid

    @staticmethod
    def from_dict(data: Dict) -> 'Playlist':
        tracks = []
        for item in data['tracks']:
            track = Track.from_dict(item)
            tracks.append(track)

        return Playlist(int(data['pid']), tracks)
