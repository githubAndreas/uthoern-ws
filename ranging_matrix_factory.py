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
    def create(file_collection: List[str], pids:int):
        template_ranging_matrix, unique_track_uris = RangingMatrixFactory._create_template(file_collection);

        template_ranging_matrix = RangingMatrixFactory._reduce_dimension(template_ranging_matrix, pids)

        Logger.log_info('Create sparse data frame')
        return unique_track_uris, template_ranging_matrix, template_ranging_matrix.copy()

    @staticmethod
    def _reduce_dimension(sparse_matrix, row_numbs):
        shape = sparse_matrix.get_shape()
        Logger.log_info('Start reducing dimension of sparse matrix from: x=' + str(shape[1]) + '; y=' + str(shape[0]))
        Logger.log_info('Reduce to {} rows'.format(str(row_numbs)))

        new_dim = (row_numbs, shape[1])
        sparse_matrix.resize(new_dim);
        shape = sparse_matrix.get_shape()
        Logger.log_info('Sparse matrix format after resizing: x=' + str(shape[1]) + '; y=' + str(shape[0]))

        return sparse_matrix

    @staticmethod
    def _create_template(file_collection: List[str]):
        Logger.log_info('Start creating initial ranging data frame')

        slices = PlaylistSliceConverter.from_json_files(file_collection)

        unique_track_uris = TrackFilter.unique_track_uris_from_playlist_slices(slices)
        total_number_of_playlist = PlaylistUtil.count_playlists_of_slices(slices)

        x_number = len(unique_track_uris)
        y_number = total_number_of_playlist

        Logger.log_info('Matrixdimension: x=' + str(x_number) + '; y=' + str(y_number))
        template_ranging_matrix = sparse.dok_matrix((y_number, x_number), dtype=np.float32)

        for p_slice in slices:
            for playlist in p_slice.get_playlist_collection():
                playlist_id = playlist.get_pid()

                for track in playlist.get_tracks():
                    track_index = unique_track_uris[track.get_simplified_uri()]

                    template_ranging_matrix[playlist_id, track_index] = 1.0

            Logger.log_info(
                'Slice[' + p_slice.get_info().get_item_range() + '] ratings successfully insert into ranging matrix')

        Logger.log_info('Finishing initialization of ranging data frame')

        return template_ranging_matrix, unique_track_uris
