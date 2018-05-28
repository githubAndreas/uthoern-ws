from logger import Logger
from typing import List
from playlist_slice import PlaylistSlice


class PlaylistUtil:

    @staticmethod
    def count_playlists_of_slices(playlist_slices: List[PlaylistSlice]) -> int:
        Logger.log_info('Start counting total number of playlists')

        greatest_id = -1;

        for p_slice in playlist_slices:

            for playlist in p_slice.get_playlist_collection():
                pid = playlist.get_pid()
                if greatest_id < pid:
                    greatest_id = pid

        Logger.log_info('Slice[' + p_slice.get_info().get_item_range() + '] successfully inspected')

        Logger.log_info(str(greatest_id) + ' playlists totally founded')
        return greatest_id
