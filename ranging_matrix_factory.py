import numpy as np
from playlist_slice import PlaylistSlice
from typing import List, Dict
from logger import Logger
from scipy import sparse


class RangingMatrixFactory:

    @staticmethod
    def create_nparray_matrix(x_number: int, y_number: int, slices: List[PlaylistSlice],
                              unique_track_uris: Dict[str, int]) -> np.ndarray:
        Logger.log_info('Start creating initial ranging matrix')

        ranging_matrix = np.zeros((y_number, x_number), np.float32, 'F')
        Logger.log_info('Matrixdimension: x=' + str(x_number) + '; y=' + str(y_number))

        for p_slice in slices:
            for playlist in p_slice.get_playlist_collection():
                playlist_id = playlist.get_pid()

                for track in playlist.get_tracks():
                    track_index = unique_track_uris[track.get_simplified_uri()]

                    ranging_matrix[track_index, playlist_id] = 1.0

            Logger.log_info(
                'Slice[' + p_slice.get_info().get_item_range() + '] ratings successfully insert into ranging matrix')

        Logger.log_info('Finishing initialization of ranging matrix')
        return ranging_matrix

    @staticmethod
    def create_template_ranging_matrix(ranging_matrix: np.array) -> sparse.csr_matrix:
        Logger.log_info('Start creating template ranging matrix')

        csr = sparse.csr_matrix(ranging_matrix)

        Logger.log_info('Finish successfly creation of ranging matrix')
        return csr
