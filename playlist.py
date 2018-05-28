from track import Track
from typing import List, Dict


class Playlist:

    def __init__(self, name: str, collaborative: str, pid: int, modified_at: str, num_tracks: str, num_albums: str,
                 num_followers: str, tracks: List[Track], num_edits: str,
                 duration_ms: str, num_artists: str):
        self.__name = name
        self.__collaborative = collaborative
        self.__pid = pid
        self.__modified_at = modified_at
        self.__num_tracks = num_tracks
        self.__num_albums = num_albums
        self.__num_followers = num_followers
        self.__tracks = tracks
        self.__num_edits = num_edits
        self.__duration_ms = duration_ms
        self.__num_artists = num_artists

    def get_name(self) -> str:
        return self.__name;

    def get_collaborative(self) -> str:
        return self.__collaborative

    def get_pid(self) -> int:
        return self.__pid

    def get_modified_at(self):
        return self.__modified_at

    def get_num_tracks(self) -> str:
        return self.__num_tracks

    def get_num_albums(self) -> str:
        return self.__num_albums

    def get_num_followers(self) -> str:
        return self.__num_followers

    def get_tracks(self) -> List[Track]:
        return self.__tracks

    def get_num_edits(self) -> str:
        return self.__num_edits

    def get_duration_ms(self) -> str:
        return self.__duration_ms

    def get_num_artists(self) -> str:
        return self.__num_artists

    @staticmethod
    def from_dict(data: Dict) -> 'Playlist':
        tracks = []
        for item in data['tracks']:
            track = Track.from_dict(item)
            tracks.append(track)

        return Playlist(data['name'], data['collaborative'], int(data['pid']), data['modified_at'], data['num_tracks'],
                        data['num_albums'], data['num_followers'], tracks, data['num_edits'],
                        data['duration_ms'], data['num_artists'])
