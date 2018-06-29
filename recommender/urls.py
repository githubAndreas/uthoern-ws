from django.conf.urls import url

from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^dataset$', views.dataset, name='dataset'),
    url(r'^training$', views.training, name='training'),
    url(r'^prediction$', views.prediction, name='prediction'),
    url(r'^prediction/(?P<prediction_id>\d+)/$$', views.download_prediction_csv, name='prediction'),

    url(r'^.*$', RedirectView.as_view(url="/dataset"), name='default_redirect'),  # default route
]
