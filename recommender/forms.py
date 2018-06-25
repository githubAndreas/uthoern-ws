from django import forms
from django.utils.translation import gettext_lazy as _

from recommender.models import Preparation_Session


class PreparationControlForm(forms.ModelForm):
    class Meta:
        model = Preparation_Session
        fields = ('decomposition', 'num_initial_pids', 'num_target_features')
        labels = {
            'decomposition': _('Decomposition Model'),
            'num_initial_pids': _('Anzahl Playlists'),
            'num_target_features': _('Anzahl Zielfeatures'),
        }
