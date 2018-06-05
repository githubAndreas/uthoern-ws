import numpy as np
from playlist_slice import PlaylistSlice
from typing import List, Dict
from logger import Logger
from scipy import sparse
from playlist_util import PlaylistUtil
from track_filter import TrackFilter
import pandas as pd
from playlist_slice_converter import PlaylistSliceConverter


class RangingMatrixFactory:

    @staticmethod
    def create(file_collection: List[str]) -> pd.DataFrame:

        template_ranging_matrix, unique_track_uris, playlist_ids = RangingMatrixFactory._create_template(file_collection);

        Logger.log_info('Create sparse data frame')
        return pd.SparseDataFrame(data=template_ranging_matrix, index=playlist_ids, columns=[*unique_track_uris],
                                  default_fill_value=0.0, dtype=np.float64), template_ranging_matrix

    @staticmethod
    def _create_template( file_collection: List[str]):
        Logger.log_info('Start creating initial ranging data frame')

        slices = PlaylistSliceConverter.from_json_files(file_collection)

        playlist_ids = list()
        unique_track_uris = TrackFilter.unique_track_uris_from_playlist_slices(slices)
        total_number_of_playlist = PlaylistUtil.count_playlists_of_slices(slices)

        x_number = len(unique_track_uris)
        y_number = total_number_of_playlist

        Logger.log_info('Matrixdimension: x=' + str(x_number) + '; y=' + str(y_number))
        template_ranging_matrix = sparse.csr_matrix((y_number, x_number), dtype=np.float32)
        # ranging_matrix = np.zeros((y_number, x_number), np.float32, 'F')

        for p_slice in slices:
            for playlist in p_slice.get_playlist_collection():
                playlist_id = playlist.get_pid()
                playlist_ids.append(playlist_id)

                for track in playlist.get_tracks():
                    track_index = unique_track_uris[track.get_simplified_uri()]

                    template_ranging_matrix[playlist_id, track_index] = 1.0

            Logger.log_info(
                'Slice[' + p_slice.get_info().get_item_range() + '] ratings successfully insert into ranging matrix')

        Logger.log_info('Finishing initialization of ranging data frame')

        return template_ranging_matrix, unique_track_uris, playlist_ids;
