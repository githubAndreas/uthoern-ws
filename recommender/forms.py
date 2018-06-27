from django import forms
from django.utils.translation import gettext_lazy as _

from recommender.models import Preparation_Session, Training_Session


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
    class Meta:
        model = Training_Session
        fields = ('model_algorithm', 'num_iteration')
        labels = {
            'model_algorithm': _('Vorhersage Model'),
            'num_iteration': _('Anzahl Iterationen'),
        }
