from logger import Logger
from argparse import ArgumentParser
from os import path
import sys
from date_time_util import DateTimeUtil
from playlist_parser import PlaylistParser
from playlist_slice_converter import PlaylistSliceConverter
from model_util import ModelUtil
from ranging_matrix_factory import RangingMatrixFactory
from track_filter import TrackFilter
from sklearn.decomposition import TruncatedSVD
from scipy import sparse
import numpy as np
import pandas as pd
from data_frame_util import DataFrameUtil
from playlist_util import PlaylistUtil

challenge_set_file_name = "challenge_set.json"


def __predict_model(abs_challenge_set_path: str, abs_model_path: str, model_instance_id: int) -> None:
    instance_id = DateTimeUtil.generate_timestamp_id()
    Logger.log_info("Start predict model instance '{}'".format(instance_id))

    # Load challange set
    file_collection = PlaylistParser.parse_folder(abs_challenge_set_path, challenge_set_file_name)
    unique_track_uris = ModelUtil.load_columns_from_disk(abs_model_path, model_instance_id)
    selector = ModelUtil.load_from_disk(model_instance_id, 'TruncatedSVD', '')

    p_slices = PlaylistSliceConverter.from_json_files(file_collection)

    model_dict = ModelUtil.load_dict_from_disk(model_instance_id, 'Ridge', unique_track_uris)

    recommentation_dict = {}

    # iteriere über challange set Batch
    for p_slice in p_slices:
        total_number_of_playlist = PlaylistUtil.count_playlists_of_slices([p_slice])
        item_range = p_slice.get_info().get_item_range()
        chunk_count = 0

        for chunk in np.array_split(p_slice.get_playlist_collection(), 1):
            chunk_count = chunk_count + 1
            sparse_challenge_matrix, template_sparse_challenge_matrix, pids = RangingMatrixFactory.create_sparse_challenge_set(
                chunk, item_range, unique_track_uris, len(chunk))

            Logger.log_info("Start reducing dimension")
            X_sparse = selector.transform(sparse_challenge_matrix)
            Logger.log_info("Finishing reducing dimension")

            # Iteriere über columns
            Logger.log_info("Start iterate ofer columns")
            for column_index, track_url in enumerate(unique_track_uris):
                Logger.log_info(
                    "Chunk[{}] - Column [{}/{}] - {} predict".format(str(chunk_count), str(column_index),
                                                                     str(len(unique_track_uris)), track_url))

                reg = model_dict[track_url]
                predicted_column = reg.predict(X_sparse)

                template_column_array = template_sparse_challenge_matrix[:, column_index].toarray()
                predicted_column[template_column_array] = 1.0
                sparse_challenge_matrix[:, column_index] = predicted_column

            for row_index in range(sparse_challenge_matrix.shape[0]):
                Logger.log_info(
                    "Start recommendation for {}/{}".format(str(row_index), str(sparse_challenge_matrix.shape[0])))
                sparse_row = sparse_challenge_matrix[row_index, :].toarray()
                template_row = template_sparse_challenge_matrix[row_index, :]
                template_row_array = template_row.toarray()

                sparse_row_df = pd.DataFrame(data=sparse_row, columns=unique_track_uris, dtype=np.float32)

                all_columns = sparse_row_df.columns.values

                selected_columns = all_columns[template_row_array[0, :]]

                sparse_row_df = __drop_columns(sparse_row_df, selected_columns)

                sparse_row_df = sparse_row_df.T

                sparse_row_df = sparse_row_df.sort_values(by=0, ascending=False)

                sparse_row_df = sparse_row_df.T

                recommendation = sparse_row_df.columns.values[:500]

                recomm_pid = pids[row_index] # Fehler !!!!
                recommentation_dict[recomm_pid] = recommendation
                Logger.log_info("Finish recommendation for {}".format(str(row_index)))

        DataFrameUtil.export_to_csv(recommentation_dict, './model_storage/{}'.format(str(model_instance_id)))


def __drop_columns(sparse_row_df, selected_columns):
    cols = [c for c in selected_columns if c in sparse_row_df.columns.values]

    sparse_row_df = sparse_row_df.drop(columns=cols)
    return sparse_row_df


def __receive_path_argument():
    """Read path from command line arguments"""
    parser = ArgumentParser()
    parser.add_argument("challenge_set_path", type=str, help='Path to challenge set')
    parser.add_argument("instance_id", type=int, help='Id of the instance')

    # Show --help if arguments are absent
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    return args.challenge_set_path, args.instance_id


if __name__ == '__main__':
    Logger.__init__()
    Logger.log_info('Start predict uthoern')

    challenge_set_path, instance_id = __receive_path_argument()

    abs_challenge_set_path = path.abspath(challenge_set_path)
    abs_model_path = path.abspath("./model_storage/{}".format(str(instance_id)))

    __predict_model(abs_challenge_set_path, abs_model_path, instance_id)

    Logger.log_info('Stop predict uthoern')
