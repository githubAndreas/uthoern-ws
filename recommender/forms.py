from django import forms
from django.utils.translation import gettext_lazy as _

from recommender.models import Preparation_Session


class PreparationControlForm(forms.ModelForm):
    class Meta:
        model = Preparation_Session
        fields = ('decomposition', 'initial_pids',)
        labels = {
            'decomposition': _('Decomposition Model'),
            'initial_pids': _('Anzahl Playlists'),
        }
