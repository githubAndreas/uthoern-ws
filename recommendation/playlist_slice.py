from info import Info
from playlist import Playlist
from typing import List, Dict


class PlaylistSlice:

    def __init__(self, info: Info, playlist_collection: List[Playlist]):
        self.__info = info;
        self.__playlist_collection = playlist_collection

    def get_info(self) -> Info:
        return self.__info

    def get_playlist_collection(self) -> List[Playlist]:
        return self.__playlist_collection

    @staticmethod
    def from_dict(data: Dict) -> 'PlaylistSlice':
        info = Info.from_dict(data['info'])

        playlist_collection = []
        for item in data['playlists']:
            playlist = Playlist.from_dict(item)
            playlist_collection.append(playlist)

        return PlaylistSlice(info, playlist_collection)
