import numpy as np
from playlist_slice import PlaylistSlice
from typing import List, Dict
from logger import Logger
from scipy import sparse
from playlist_util import PlaylistUtil
from track_filter import TrackFilter
import pandas as pd
from playlist_slice_converter import PlaylistSliceConverter
from playlist import Playlist


class RangingMatrixFactory:

    @staticmethod
    def create(file_collection: List[str], pids: int):
        sparse_ranging_matrix, ranging_bool_mask, unique_track_uris = RangingMatrixFactory._create_template(file_collection);

        sparse_ranging_matrix, ranging_bool_mask, RangingMatrixFactory._reduce_dimension(sparse_ranging_matrix, ranging_bool_mask ,pids)

        Logger.log_info('Create sparse data frame')
        return unique_track_uris, sparse_ranging_matrix, ranging_bool_mask

    @staticmethod
    def _reduce_dimension(sparse_matrix, ranging_bool_mask, row_numbs):
        shape = sparse_matrix.get_shape()
        Logger.log_info('Start reducing dimension of sparse matrix from: x=' + str(shape[1]) + '; y=' + str(shape[0]))
        Logger.log_info('Reduce to {} rows'.format(str(row_numbs)))

        new_dim = (row_numbs, shape[1])
        sparse_matrix.resize(new_dim);
        ranging_bool_mask.resize(new_dim);
        shape = sparse_matrix.get_shape()
        Logger.log_info('Sparse matrix format after resizing: x=' + str(shape[1]) + '; y=' + str(shape[0]))

        return sparse_matrix, ranging_bool_mask

    @staticmethod
    def _create_template(file_collection: List[str]):
        Logger.log_info('Start creating initial ranging data frame')

        slices = PlaylistSliceConverter.from_json_files(file_collection)

        unique_track_uris = TrackFilter.unique_track_uris_from_playlist_slices(slices)
        total_number_of_playlist = PlaylistUtil.count_playlists_of_slices(slices)

        x_number = len(unique_track_uris)
        y_number = total_number_of_playlist

        Logger.log_info('Matrixdimension: x=' + str(x_number) + '; y=' + str(y_number))
        sparse_ranging_matrix = sparse.dok_matrix((y_number, x_number), dtype=np.float32)
        ranging_bool_mask = sparse.dok_matrix((y_number, x_number), dtype=np.bool)

        for p_slice in slices:
            for playlist in p_slice.get_playlist_collection():
                playlist_id = playlist.get_pid()

                for track in playlist.get_tracks():
                    track_index = unique_track_uris[track.get_simplified_uri()]

                    sparse_ranging_matrix[playlist_id, track_index] = 1.0
                    ranging_bool_mask[playlist_id, track_index] = True

            Logger.log_info(
                'Slice[' + p_slice.get_info().get_item_range() + '] ratings successfully insert into ranging matrix')

        Logger.log_info('Finishing initialization of ranging data frame')

        return sparse_ranging_matrix, ranging_bool_mask, unique_track_uris

    @staticmethod
    def create_sparse_challenge_set(chunk, item_range, unique_track_uris, total_number_of_playlist):
        x_number = len(unique_track_uris)
        y_number = total_number_of_playlist

        Logger.log_info('Matrixdimension: x=' + str(x_number) + '; y=' + str(y_number))
        challenge_matrix = sparse.dok_matrix((y_number, x_number), dtype=np.float32)
        template_challenge_matrix = sparse.dok_matrix((y_number, x_number), dtype=np.bool)
        pids = {}

        for index, playlist in enumerate(chunk):
            pids[index] = playlist.get_pid()

            for track in playlist.get_tracks():
                simple_url = track.get_simplified_uri()
                if simple_url in unique_track_uris:  # TODO AHU Wieder entfernen nach Test
                    track_index = unique_track_uris[track.get_simplified_uri()]
                    challenge_matrix[index, int(track_index)] = 1.0
                    template_challenge_matrix[index, int(track_index)] = True

        Logger.log_info(
            'Slice[' + item_range + '] ratings successfully insert into challenge matrix')

        Logger.log_info('Finishing initialization of challenge data frame')

        return challenge_matrix, template_challenge_matrix, pids
