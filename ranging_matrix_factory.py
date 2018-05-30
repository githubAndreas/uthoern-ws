import numpy as np
from playlist_slice import PlaylistSlice
from typing import List, Dict
from logger import Logger
from scipy import sparse
from playlist_util import PlaylistUtil
from track_filter import TrackFilter
import pandas as pd


class RangingMatrixFactory:

    @staticmethod
    def create_data_frame(slices: List[PlaylistSlice]) -> pd.DataFrame:
        Logger.log_info('Start creating initial ranging data frame')

        unique_track_uris = TrackFilter.unique_track_uris_from_playlist_slices(slices)
        total_number_of_playlist = PlaylistUtil.count_playlists_of_slices(slices)

        x_number = len(unique_track_uris)
        y_number = total_number_of_playlist

        ranging_matrix = np.zeros((y_number, x_number), np.float32, 'F')
        Logger.log_info('Matrixdimension: x=' + str(x_number) + '; y=' + str(y_number))

        for p_slice in slices:
            for playlist in p_slice.get_playlist_collection():
                playlist_id = playlist.get_pid()

                for track in playlist.get_tracks():
                    track_index = unique_track_uris[track.get_simplified_uri()]

                    ranging_matrix[playlist_id, track_index] = 1.0

            Logger.log_info(
                'Slice[' + p_slice.get_info().get_item_range() + '] ratings successfully insert into ranging matrix')

        ranging_data_frame = pd.DataFrame(ranging_matrix, columns=unique_track_uris)
        Logger.log_info('Finishing initialization of ranging data frame')

        return ranging_data_frame

    @staticmethod
    def create_template_ranging_matrix(ranging_df: pd.DataFrame) -> sparse.csr_matrix:
        Logger.log_info('Start creating template ranging matrix')

        csr = sparse.csr_matrix(ranging_df.values)

        Logger.log_info('Finish successfully creation of ranging matrix')
        return csr
