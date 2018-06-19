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


class DecompositionConfiguration(models.Model):
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=200)


class DecompositionSession(models.Model):
    decomposition = models.ForeignKey(Decomposition, on_delete=models.PROTECT)
    decomposition_configuration = models.ForeignKey(DecompositionConfiguration, on_delete=models.CASCADE)


class PreparationSession(models.Model):
    environment = models.ForeignKey(Environment, on_delete=models.PROTECT)
    decomposition_session = models.ForeignKey(DecompositionSession, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    init_slices = models.IntegerField()
    init_pids = models.IntegerField()
