import threading

from django.db import models


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

        self.__preparate()

        preparator.status = "FINISH"
        preparator.save()

    def __preparate(self):
        pass
