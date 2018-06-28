from django import forms
from django.utils.translation import gettext_lazy as _

from recommender.models import Preparation_Session, Training_Session, Prediction_Session


class PreparationControlForm(forms.ModelForm):
    class Meta:
        model = Preparation_Session
        fields = ('decomposition', 'num_initial_pids', 'num_target_features')
        labels = {
            'decomposition': _('Decomposition Model'),
            'num_initial_pids': _('Anzahl Playlists'),
            'num_target_features': _('Anzahl Zielfeatures'),
        }


class TrainingControlForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TrainingControlForm, self).__init__(*args, **kwargs)
        self.fields['preparation_session'].queryset = Preparation_Session.objects.filter(status="FINISH")

    class Meta:
        model = Training_Session
        fields = ('preparation_session', 'model_algorithm', 'num_iteration')
        labels = {
            'preparation_session': _('Datensatz'),
            'model_algorithm': _('Vorhersage Model'),
            'num_iteration': _('Anzahl Iterationen'),
        }


class PredictionControlForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PredictionControlForm, self).__init__(*args, **kwargs)
        self.fields['training_session'].queryset = Training_Session.objects.filter(status="FINISH")

    class Meta:
        model = Prediction_Session
        fields = ('training_session', 'num_batch_size')
        labels = {
            'training_session': _('Trainingseinheit'),
            'num_batch_size': _('Anzahl Batches'),
        }
