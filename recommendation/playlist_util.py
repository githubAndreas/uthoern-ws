from logger import Logger
from typing import List
from playlist_slice import PlaylistSlice


class PlaylistUtil:

    @staticmethod
    def count_playlists_of_slices(playlist_slices: List[PlaylistSlice]) -> int:
        Logger.log_info('Start counting total number of playlists')

        counter = 0;

        for p_slice in playlist_slices:
            for playlist in p_slice.get_playlist_collection():
                counter = counter + 1

            Logger.log_info('Slice[' + p_slice.get_info().get_item_range() + '] successfully inspected')

        Logger.log_info(str(counter) + ' playlists totally founded')
        return counter
