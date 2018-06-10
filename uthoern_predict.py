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

challenge_set_file_name = "challenge_set.json"


def __predict_model(abs_challenge_set_path: str, abs_model_path: str, model_instance_id: int) -> None:
    instance_id = DateTimeUtil.generate_timestamp_id()
    Logger.log_info("Start predict model instance '{}'".format(instance_id))

    # Load challange set
    file_collection = PlaylistParser.parse_folder(abs_challenge_set_path, challenge_set_file_name)
    unique_track_uris = ModelUtil.load_columns_from_disk(abs_model_path, model_instance_id)
    selector = ModelUtil.load_from_disk(model_instance_id, 'TruncatedSVD', '')

    p_slices = PlaylistSliceConverter.from_json_files(file_collection)

    # iteriere über challange set Batch
    for p_slice in p_slices:
        p_slice_unique_track_uris, sparse_challenge_matrix, template_challenge_matrix = RangingMatrixFactory.create_sparse_challenge_set(
            p_slice, unique_track_uris)

        # Reduce dimension
        X_sparse = selector.transform(sparse_challenge_matrix)

        # Iteriere über columns
        for column_index, target_column in enumerate(unique_track_uris):
            reg = ModelUtil.load_from_disk(model_instance_id, 'Ridge', target_column)

            # Predict value
            predicted_column = reg.predict(X_sparse)

            for row_index, row in predicted_column:
                if template_challenge_matrix[row_index, column_index] != 1:
                    sparse_challenge_matrix[row_index, column_index] = predicted_column[row_index]

        print(sparse_challenge_matrix)


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
