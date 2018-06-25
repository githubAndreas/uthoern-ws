from django.db import models


class Environment(models.Model):
    name = models.CharField(max_length=10)
    mdp_set_dir_path = models.CharField(max_length=200)
    challenge_set_dir_path = models.CharField(max_length=200)
    recommendation_dir_path = models.CharField(max_length=200)
    columns_dir_path = models.CharField(max_length=200)
    decomposition_alg_dir_path = models.CharField(max_length=200)
    ml_alg_dir_path = models.CharField(max_length=200)


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
