from info import Info
from playlist import Playlist


class PlaylistSlice:

    def __init__(self, info, playlist_collection):
        self.__info = info;
        self.__playlist_collection = playlist_collection

    def get_info(self):
        return self.__info

    def get_playlist_collection(self):
        return self.__playlist_collection

    @staticmethod
    def from_dict(data):
        info = Info.from_dict(data['info'])

        playlist_collection = []
        for item in data['playlists']:
            playlist = Playlist.from_dict(item)
            playlist_collection.append(playlist)

        return PlaylistSlice(info, playlist_collection)
