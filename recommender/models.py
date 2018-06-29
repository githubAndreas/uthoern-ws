import datetime
import threading
from os import path

import numpy as np
import pandas as pd
from django.db import models
from scipy import sparse
from sklearn.model_selection import train_test_split

from .data_frame_util import DataFrameUtil
from .decomposition_factory import DecompositionFactory
from .logger import Logger
from .model_util import ModelUtil
from .playlist_parser import PlaylistParser
from .playlist_slice_converter import PlaylistSliceConverter
from .prediction_model_factory import PredictionModelFactory
from .ranging_matrix_factory import RangingMatrixFactory

SPARSE_FILE_NAME_FORMAT = "{}_sparse_{}.npz"

CHALLENGE_SET_FILE = "challenge_set.json"


class Environment(models.Model):
    name = models.CharField(max_length=10)
    mdp_set_dir_path = models.CharField(max_length=200)
    challenge_set_dir_path = models.CharField(max_length=200)
    recommendation_dir_path = models.CharField(max_length=200)
    columns_dir_path = models.CharField(max_length=200)
    decomposition_alg_dir_path = models.CharField(max_length=200)
    ml_alg_dir_path = models.CharField(max_length=200)

    @staticmethod
    def get_local():
        if path.exists(path.abspath("environment.testing")):
            Logger.log_info("Environment: testing")
            return Environment.objects.get(name__exact='testing')

        if path.exists(path.abspath("environment.production")):
            Logger.log_info("Environment: production")
            return Environment.objects.get(name__exact='production')

        err_msg = "Could not find environment configuration!"
        Logger.log_error(err_msg)
        raise ValueError(err_msg)


class Session_Meta(models.Model):
    start_time = models.DateTimeField(blank=True)
    end_time = models.DateTimeField(blank=True, null=True)


class Decomposition(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Preparation_Session(models.Model):
    environment = models.ForeignKey(Environment, on_delete=models.PROTECT)
    decomposition = models.ForeignKey(Decomposition, on_delete=models.PROTECT)
    status = models.CharField(max_length=20)
    num_initial_pids = models.IntegerField()
    num_target_features = models.IntegerField()
    meta = models.ForeignKey(Session_Meta, on_delete=models.CASCADE)

    def __str__(self):
        return '#{} - {} - P{} - F{} - {}'.format(self.id, self.decomposition, self.num_initial_pids,
                                                  self.num_target_features, self.status)

    def start(self):
        self.environment = Environment.get_local()

        Logger.log_info("Change preparator status to INITIALIZE")
        self.status = "INITIALIZE"

        meta = Session_Meta()
        meta.start_time = datetime.datetime.now()
        meta.save()

        self.meta = meta;
        self.save()

        preparation_session_thread = PreparationThread(self.id, self.decomposition,
                                                       self.num_initial_pids,
                                                       self.num_target_features)
        preparation_session_thread.start()


class Model_Algorithm(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Training_Session(models.Model):
    preparation_session = models.ForeignKey(Preparation_Session, on_delete=models.PROTECT)
    model_algorithm = models.ForeignKey(Model_Algorithm, on_delete=models.PROTECT)
    num_iteration = models.IntegerField()
    status = models.CharField(max_length=20)
    meta = models.ForeignKey(Session_Meta, on_delete=models.CASCADE)

    def __str__(self):
        return '#{} - {} - It{} - P#{} - {}'.format(self.id, self.model_algorithm, self.num_iteration,
                                                    self.preparation_session.id, self.status)

    def start(self):
        Logger.log_info("Change trainer status to INITIALIZE")
        self.status = "INITIALIZE"

        meta = Session_Meta()
        meta.start_time = datetime.datetime.now()
        meta.save()

        self.meta = meta;
        self.save()

        training_session_thread = TrainingThread(self.id, self.preparation_session, self.model_algorithm,
                                                 self.num_iteration)
        training_session_thread.start()


class Model_Configuration(models.Model):
    training_session = models.ForeignKey(Training_Session, on_delete=models.PROTECT)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)


class Prediction_Session(models.Model):
    training_session = models.ForeignKey(Training_Session, on_delete=models.PROTECT)
    num_batch_size = models.IntegerField()
    status = models.CharField(max_length=20)
    export_file_name = models.CharField(max_length=100)
    meta = models.ForeignKey(Session_Meta, on_delete=models.CASCADE)

    def __str__(self):
        return '#{} - T#{} - P#{} - {}'.format(self.id, self.training_session.id,
                                               self.training_session.preparation_session.id, self.status)

    def start(self):
        Logger.log_info("Change prediction status to INITIALIZE")
        self.status = "INITIALIZE"

        meta = Session_Meta()
        meta.start_time = datetime.datetime.now()
        meta.save()

        self.meta = meta;
        self.save()

        prediction_session_thread = PredictionThread(self.id, self.training_session, self.num_batch_size)
        prediction_session_thread.start()

    def get_file_path(self):
        environment = Environment.get_local()
        absolute_export_path = path.abspath(environment.recommendation_dir_path)

        return path.join(absolute_export_path, self.export_file_name)


class PreparationThread(threading.Thread):

    def __init__(self, session_id, decomposer: Decomposition, num_pids: int, num_features: int):
        threading.Thread.__init__(self)
        self.__session_id = session_id
        self.__decomposer = decomposer
        self.__num_pids = num_pids
        self.__num_features = num_features

    def run(self):
        preparator = Preparation_Session.objects.get(pk=self.__session_id)

        Logger.log_info("Change preparator status to RUNNING")
        preparator.status = "RUNNING"
        preparator.decomposition = self.__decomposer
        preparator.num_initial_pids = self.__num_pids
        preparator.num_target_features = self.__num_features
        preparator.save()

        self.__fit(preparator.environment)

        Logger.log_info("Change preparator status to FINISH")
        preparator.status = "FINISH"

        preparator.meta.end_time = datetime.datetime.now()
        preparator.meta.save()
        preparator.save()

    def __fit(self, environment: Environment):
        train_data_path = path.abspath(environment.mdp_set_dir_path)

        file_collection = PlaylistParser.parse_folder(train_data_path, 'mpd\.slice\.\d+\-\d+\.json')

        unique_track_uris, sparse_ranging_matrix, ranging_bool_mask = RangingMatrixFactory.create(file_collection,
                                                                                                  self.__num_pids)

        selector = DecompositionFactory.get(self.__decomposer.name, self.__num_features)
        selector = selector.fit(sparse_ranging_matrix)

        decomposition_alg_path = path.abspath(environment.decomposition_alg_dir_path)

        # Save sparse matrix
        Logger.log_info("Start saving sparse matrix")
        sparse.save_npz(path.join(decomposition_alg_path, SPARSE_FILE_NAME_FORMAT.format(self.__session_id, 'num')),
                        sparse_ranging_matrix.tocoo())

        sparse.save_npz(path.join(decomposition_alg_path, SPARSE_FILE_NAME_FORMAT.format(self.__session_id, 'mask')),
                        ranging_bool_mask.tocoo())

        Logger.log_info("Finish saving sparse matrix")

        # Save decomposer
        Logger.log_info("Start save decomposer")
        ModelUtil.save_to_disk(selector, self.__session_id, self.__decomposer, '', decomposition_alg_path)
        Logger.log_info("Finish save decomposer")

        # Save columns
        Logger.log_info("Start save columns")
        ModelUtil.save_columns_to_disk(unique_track_uris, self.__session_id, environment.columns_dir_path)
        Logger.log_info("Finish save columns")


class TrainingThread(threading.Thread):

    def __init__(self, session_id, preparation_session: Preparation_Session, model_algorithm: Model_Algorithm,
                 num_iterations: int):
        threading.Thread.__init__(self)

        self.__session_id = session_id
        self.__preparation_session = preparation_session
        self.__model_algorithm = model_algorithm
        self.__num_iterations = num_iterations

    def run(self):
        trainer = Training_Session.objects.get(pk=self.__session_id)

        Logger.log_info("Change trainer status to RUNNING")
        trainer.status = "RUNNING"
        trainer.preparation_session = self.__preparation_session
        trainer.model_algorithm = self.__model_algorithm
        trainer.num_iterations = self.__num_iterations
        trainer.save()

        self.__fit(trainer.preparation_session.environment)

        Logger.log_info("Change trainer status to FINISH")
        trainer.status = "FINISH"
        trainer.meta.end_time = datetime.datetime.now()
        trainer.meta.save()
        trainer.save()

    def __fit(self, environment: Environment):
        decomposition_alg_path = path.abspath(environment.decomposition_alg_dir_path)

        Logger.log_info("Start load sparse rangingmatrix")
        sparse_ranging_matrix = sparse.load_npz(path.join(decomposition_alg_path, SPARSE_FILE_NAME_FORMAT.format(
            self.__preparation_session.id, 'num'))).todok()
        Logger.log_info("Finish load sparse rangingmatrix")

        Logger.log_info("Start load bool mask matrix")
        ranging_bool_mask = sparse.load_npz(path.join(decomposition_alg_path, SPARSE_FILE_NAME_FORMAT.format(
            self.__preparation_session.id, 'mask'))).todok()
        Logger.log_info("Finish load bool mask matrix")

        Logger.log_info("Start load unique track list")
        unique_track_uris = ModelUtil.load_columns_from_disk(environment.columns_dir_path,
                                                             self.__preparation_session.id)
        Logger.log_info("Finish load unique track list")

        Logger.log_info("Start load decomposer")
        decomposer = ModelUtil.load_from_disk(self.__preparation_session.id,
                                              self.__preparation_session.decomposition.name, '',
                                              environment.decomposition_alg_dir_path)
        Logger.log_info("Finish load decomposer")

        X_sparse = decomposer.transform(sparse_ranging_matrix)
        X = pd.DataFrame(data=X_sparse, dtype=np.float32)

        for ranging_iter in range(self.__num_iterations):
            for column_index, target_column in enumerate(unique_track_uris):
                Logger.log_info(
                    'Model[' + str(column_index + 1) + '/' + str(len(unique_track_uris)) + '] Name:' + target_column)

                y = sparse_ranging_matrix.getcol(column_index)
                y_df = pd.DataFrame(data=y.toarray(), dtype=np.float32)

                X_train, X_test, y_train, y_test = train_test_split(X, y_df, random_state=42)

                # Modele
                reg = PredictionModelFactory.get(self.__model_algorithm.name)

                # Train
                reg_train = reg.fit(X_train.values, y_train)

                # Predict
                matrix = X_test.as_matrix()
                predicted_column = reg.predict(matrix)

                # Save model
                if ranging_iter == self.__num_iterations - 1:
                    ModelUtil.save_to_disk(reg, self.__session_id, self.__model_algorithm.name, target_column,
                                           environment.ml_alg_dir_path)

                Logger.log_info('Start writing predicted values into rating matrix')

                row_indexes = X_test.index.values
                filtered_mask = (ranging_bool_mask[row_indexes, column_index]).toarray()
                predicted_column[filtered_mask] = 1.0
                sparse_ranging_matrix[row_indexes, column_index] = predicted_column

                Logger.log_info('Finish writing predicted values into rating matrix')

                Logger.log_info("Score Trainingsdatensatz: {:.2f}".format(reg_train.score(X_train, y_train)))
                Logger.log_info("Score Testdatensatz: {:.2f}".format(reg.score(X_test, y_test)))

        Logger.log_info("Finish train model instance '{}'".format(self.__session_id))


class PredictionThread(threading.Thread):

    def __init__(self, session_id, training_session: Training_Session, num_batch_size: int):
        threading.Thread.__init__(self)

        self.__session_id = session_id
        self.__training_session = training_session
        self.__num_batch_size = num_batch_size

    def run(self):
        clairvoyants = Prediction_Session.objects.get(pk=self.__session_id)

        Logger.log_info("Change prediction status to RUNNING")
        clairvoyants.status = "RUNNING"
        clairvoyants.training_session = self.__training_session
        clairvoyants.num_batch_size = self.__num_batch_size
        clairvoyants.save()

        clairvoyants.export_file_name = self.__transform(clairvoyants.training_session.preparation_session.environment)

        Logger.log_info("Change prediction status to FINISH")
        clairvoyants.status = "FINISH"
        clairvoyants.meta.end_time = datetime.datetime.now()
        clairvoyants.meta.save()
        clairvoyants.save()

    def __transform(self, environment: Environment) -> str:
        Logger.log_info("Start predict model instance '{}'".format(self.__session_id))

        Logger.log_info("Start load challenge set")
        file_collection = PlaylistParser.parse_folder(path.abspath(environment.challenge_set_dir_path),
                                                      CHALLENGE_SET_FILE)
        Logger.log_info("Finish load challenge set")

        Logger.log_info("Start load unique track list")
        unique_track_uris = ModelUtil.load_columns_from_disk(environment.columns_dir_path,
                                                             self.__training_session.preparation_session.id)
        Logger.log_info("Finish load unique track list")

        Logger.log_info("Start load decomposer")
        decomposer = ModelUtil.load_from_disk(self.__training_session.preparation_session.id,
                                              self.__training_session.preparation_session.decomposition.name, '',
                                              environment.decomposition_alg_dir_path)
        Logger.log_info("Finish load decomposer")

        p_slices = PlaylistSliceConverter.from_json_files(file_collection)

        Logger.log_info("Start load models")
        model_dict = ModelUtil.load_dict_from_disk(self.__training_session.id,
                                                   self.__training_session.model_algorithm.name, unique_track_uris,
                                                   environment.ml_alg_dir_path)
        Logger.log_info("Finish load models")

        recommentation_dict = {}

        for p_slice in p_slices:
            item_range = p_slice.get_info().get_item_range()
            batch_count = 0

            for batch in np.array_split(p_slice.get_playlist_collection(), self.__num_batch_size):
                batch_count = batch_count + 1
                sparse_challenge_matrix, template_sparse_challenge_matrix, pids = RangingMatrixFactory.create_sparse_challenge_set(
                    batch, item_range, unique_track_uris, len(batch))

                Logger.log_info("Start reducing dimension")
                X_sparse = decomposer.transform(sparse_challenge_matrix)
                Logger.log_info("Finishing reducing dimension")

                # Iteriere über columns
                Logger.log_info("Start iterate ofer columns")
                for column_index, track_url in enumerate(unique_track_uris):
                    Logger.log_info(
                        "Batch[{}] - Column [{}/{}] - {} predict".format(str(batch_count), str(column_index),
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

                    sparse_row_df = DataFrameUtil.drop_columns(sparse_row_df, selected_columns)

                    sparse_row_df = sparse_row_df.T

                    sparse_row_df = sparse_row_df.sort_values(by=0, ascending=False)

                    sparse_row_df = sparse_row_df.T

                    recommendation = sparse_row_df.columns.values[:500]

                    recomm_pid = pids[row_index]
                    recommentation_dict[recomm_pid] = recommendation
                    Logger.log_info("Finish recommendation for {}".format(str(row_index)))

        return DataFrameUtil.export_to_csv(recommentation_dict, environment.recommendation_dir_path)
