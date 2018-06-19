from logger import Logger
from playlist_parser import PlaylistParser

from ranging_matrix_factory import RangingMatrixFactory
from sklearn.linear_model import Ridge
import numpy as np
from sklearn.model_selection import train_test_split
from business.date_time_util import DateTimeUtil
from model_util import ModelUtil
import sys
from argparse import ArgumentParser
from os import path
from sklearn.decomposition import TruncatedSVD
import pandas as pd

mpd_pattern = 'mpd\.slice\.\d+\-\d+\.json'


def train_model(absolute_train_data_path: str, pids: int):
    instance_id = DateTimeUtil.generate_timestamp_id()
    Logger.log_info("Start train model instance '{}'".format(instance_id))

    file_collection = PlaylistParser.parse_folder(absolute_train_data_path, mpd_pattern)

    unique_track_uris, sparse_ranging_matrix, ranging_bool_mask = RangingMatrixFactory.create(file_collection,
                                                                                              pids)
    number_of_iterations = 1
    Logger.log_info('Configured number of complete iterations: {}'.format(number_of_iterations))

    selector = TruncatedSVD(n_components=2)
    selector = selector.fit(sparse_ranging_matrix)

    X_sparse = selector.transform(sparse_ranging_matrix)
    X = pd.DataFrame(data=X_sparse, dtype=np.float32)

    ModelUtil.save_to_disk(selector, instance_id, 'TruncatedSVD', '')

    for ranging_iter in range(number_of_iterations):
        for column_index, target_column in enumerate(unique_track_uris):
            Logger.log_info(
                'Model[' + str(column_index + 1) + '/' + str(len(unique_track_uris)) + '] Name:' + target_column)

            y = sparse_ranging_matrix.getcol(column_index)
            y_df = pd.DataFrame(data=y.toarray(), dtype=np.float32)

            X_train, X_test, y_train, y_test = train_test_split(X, y_df, random_state=42)

            # Modele
            # reg = KNeighborsRegressor(n_neighbors=2,n_jobs=-1)
            # reg = LinearRegression(n_jobs=-1)
            reg = Ridge()
            # reg = Lasso
            # reg = BayesianRidge()
            # reg = SVR(C=1.0, epsilon=0.2)

            # Train
            reg_train = reg.fit(X_train.values, y_train)

            # Predict
            matrix = X_test.as_matrix()
            predicted_column = reg.predict(matrix)

            # Save model
            if ranging_iter == number_of_iterations - 1:
                ModelUtil.save_to_disk(reg, instance_id, 'Ridge', target_column)

            Logger.log_info('Start writing predicted values into rating matrix')

            row_indexes = X_test.index.values
            filtered_mask = (ranging_bool_mask[row_indexes, column_index]).toarray()
            predicted_column[filtered_mask] = 1.0
            sparse_ranging_matrix[row_indexes, column_index] = predicted_column

            Logger.log_info('Finish writing predicted values into rating matrix')

            Logger.log_info("Score Trainingsdatensatz: {:.2f}".format(reg_train.score(X_train, y_train)))
            Logger.log_info("Score Testdatensatz: {:.2f}".format(reg.score(X_test, y_test)))

    ModelUtil.save_columns_to_disk(unique_track_uris, instance_id)

    Logger.log_info("Finish train model instance '{}'".format(instance_id))


def recommend_challenge_set():
    pass


def __receive_path_argument():
    """Read path from command line arguments"""
    parser = ArgumentParser()
    parser.add_argument("path", type=str, help='path to show')
    parser.add_argument("pids", type=int, help='Number of pids')

    # Show --help if arguments are absent
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    return args.path, args.pids


if __name__ == '__main__':
    Logger.__init__()
    Logger.log_info('Start uthoern')

    # Main function
    string_path, pids = __receive_path_argument()

    # Validate path
    target_path = path.normpath(string_path)
    if not path.exists(target_path):
        print("Error: Path not found: " + string_path + "!")
        sys.exit(1)

    train_model(target_path, pids)

    Logger.log_info('Stop uthoern')
