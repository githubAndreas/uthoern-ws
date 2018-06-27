import threading
from os import path

import numpy as np
import pandas as pd
from django.db import models
from scipy import sparse
from sklearn.model_selection import train_test_split

from .decomposition_factory import DecompositionFactory
from .logger import Logger
from .model_util import ModelUtil
from .playlist_parser import PlaylistParser
from .prediction_model_factory import PredictionModelFactory
from .ranging_matrix_factory import RangingMatrixFactory

SPARSE_FILE_NAME_FORMAT = "{}_sparse_{}.npz"


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
        return Environment.objects.get(name__exact='testing')


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

    def __str__(self):
        return '#{} - {} - P{} - F{} - {}'.format(self.id, self.decomposition, self.num_initial_pids,
                                                  self.num_target_features, self.status)

    def start(self):
        self.environment = Environment.get_local()

        Logger.log_info("Change preparator status to INITIALIZE")
        self.status = "INITIALIZE"
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

    def __str__(self):
        return '#{} - {} - It{} - {}'.format(self.id, self.model_algorithm, self.num_iteration, self.status)

    def start(self):
        Logger.log_info("Change trainer status to INITIALIZE")
        self.status = "INITIALIZE"
        self.save()

        training_session_thread = TrainingThread(self.id, self.preparation_session, self.model_algorithm,
                                                 self.num_iteration)
        training_session_thread.start()


class Model_Configuration(models.Model):
    training_session = models.ForeignKey(Training_Session, on_delete=models.PROTECT)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)


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
                    ModelUtil.save_to_disk(reg, self.__session_id, self.__model_algorithm.name, target_column, environment.ml_alg_dir_path)

                Logger.log_info('Start writing predicted values into rating matrix')

                row_indexes = X_test.index.values
                filtered_mask = (ranging_bool_mask[row_indexes, column_index]).toarray()
                predicted_column[filtered_mask] = 1.0
                sparse_ranging_matrix[row_indexes, column_index] = predicted_column

                Logger.log_info('Finish writing predicted values into rating matrix')

                Logger.log_info("Score Trainingsdatensatz: {:.2f}".format(reg_train.score(X_train, y_train)))
                Logger.log_info("Score Testdatensatz: {:.2f}".format(reg.score(X_test, y_test)))

        Logger.log_info("Finish train model instance '{}'".format(self.__session_id))
