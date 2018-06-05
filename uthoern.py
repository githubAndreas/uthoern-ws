from logger import Logger
from playlist_parser import PlaylistParser

from ranging_matrix_factory import RangingMatrixFactory
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso, BayesianRidge
from sklearn.svm import SVR
import numpy as np
from sklearn.model_selection import train_test_split
import math
from data_frame_util import DataFrameUtil
from date_time_util import DateTimeUtil
from model_util import ModelUtil
import sys
from argparse import ArgumentParser
from os import path


def train_model(absolute_train_data_path: str):
    instance_id = DateTimeUtil.generate_timestamp_id()
    Logger.log_info("Start train model instance '{}'".format(instance_id))

    file_collection = PlaylistParser.parse_folder(absolute_train_data_path)

    ranging_sdf, template_ranging_matrix = RangingMatrixFactory.create(file_collection)

    number_of_iterations = 1
    Logger.log_info('Configured number of complete iterations: {}'.format(number_of_iterations))

    for ranging_iter in range(number_of_iterations):
        for column_index, target_column in enumerate(ranging_sdf.columns):
            Logger.log_info(
                'Model[' + str(column_index + 1) + '/' + str(len(ranging_sdf.columns)) + '] Name:' + target_column)

            y = ranging_sdf.loc[:, target_column]
            X = ranging_sdf.drop(target_column, 'columns')

            X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

            # Modele
            # reg = KNeighborsRegressor(n_neighbors=2,n_jobs=-1)
            # reg = LinearRegression(n_jobs=-1)
            reg = Ridge()
            # reg = Lasso
            # reg = BayesianRidge()
            # reg = SVR(C=1.0, epsilon=0.2)

            # Train
            reg_train = reg.fit(X_train.as_matrix(), y_train.as_matrix())

            # Predict
            predicted_column = reg.predict(X_test.as_matrix())

            # Save model
            if ranging_iter == number_of_iterations - 1:
                ModelUtil.save_to_disk(reg, instance_id, 'Ridge', target_column)

            Logger.log_info('Start writing predicted values into rating matrix')
            i = 0
            for row_index, row in X_test.iterrows():
                if template_ranging_matrix[row_index, column_index] == 0:
                    ranging_sdf = ranging_sdf.set_value(row_index, target_column, predicted_column[i])
                    i = i + 1

            Logger.log_info('Finish writing predicted values into rating matrix')

            print("Score Trainingsdatensatz: {:.2f}".format(reg_train.score(X_train, y_train)))
            print("Score Testdatensatz: {:.2f}".format(reg.score(X_test, y_test)))

    Logger.log_info("Finish train model instance '{}'".format(instance_id))


def recommend_challenge_set():
    pass


def __receive_path_argument():
    """Read path from command line arguments"""
    parser = ArgumentParser()
    parser.add_argument("path", type=str, help='path to show')

    # Show --help if arguments are absent
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    return args.path


if __name__ == '__main__':
    Logger.log_info('Start uthoern')

    # Main function
    string_path = __receive_path_argument()

    # Validate path
    target_path = path.normpath(string_path)
    if not path.exists(target_path):
        print("Error: Path not found: " + string_path + "!")
        sys.exit(1)

    train_model(target_path)

    Logger.log_info('Stop uthoern')
