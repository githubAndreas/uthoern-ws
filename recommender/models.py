import threading

from os import path
from django.db import models

from .playlist_parser import PlaylistParser
from .ranging_matrix_factory import RangingMatrixFactory
from .decomposition_factory import DecompositionFactory
from .model_util import ModelUtil

from scipy import sparse

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

    def start(self):
        self.environment = Environment.get_local()
        self.status = "INITIALIZE"
        self.save()

        preparation_session_thread = PreparationThread(self.id, self.decomposition,
                                                       self.num_initial_pids,
                                                       self.num_target_features)
        preparation_session_thread.start()


class PreparationThread(threading.Thread):

    def __init__(self, session_id, decomposer: Decomposition, num_pids: int, num_features: int):
        threading.Thread.__init__(self)
        self.__session_id = session_id
        self.__decomposer = decomposer
        self.__num_pids = num_pids
        self.__num_features = num_features

    def run(self):
        preparator = Preparation_Session.objects.get(pk=self.__session_id)
        print(preparator)
        preparator.status = "RUNNING"
        preparator.decomposition = self.__decomposer
        preparator.num_initial_pids = self.__num_pids
        preparator.num_target_features = self.__num_features
        preparator.save()

        self.__preparate(preparator.environment)

        preparator.status = "FINISH"
        preparator.save()

    def __preparate(self, environment: Environment):
        train_data_path = path.abspath(environment.mdp_set_dir_path)

        file_collection = PlaylistParser.parse_folder(train_data_path, 'mpd\.slice\.\d+\-\d+\.json')

        unique_track_uris, sparse_ranging_matrix, ranging_bool_mask = RangingMatrixFactory.create(file_collection,
                                                                                                  self.__num_pids)

        selector = DecompositionFactory.get(self.__decomposer.name, self.__num_features)
        selector = selector.fit(sparse_ranging_matrix)

        decomposition_alg_path = path.abspath(environment.decomposition_alg_dir_path)

        # Save sparse matrix
        print("Save sparse matrix")
        sparse.save_npz(path.join(decomposition_alg_path, str(self.__session_id) + ".npz"), sparse_ranging_matrix.tocoo())

        # Save decomposer
        print("Save decomposer")
        ModelUtil.save_to_disk(selector, self.__session_id, self.__decomposer, '', decomposition_alg_path)

        # Save columns
        print("Save columns")
        ModelUtil.save_columns_to_disk(unique_track_uris, self.__session_id, environment.columns_dir_path)
