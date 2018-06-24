from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^dataset$', views.dataset, name='dataset'),
    url(r'^training$', views.training, name='training'),
    url(r'^prediction$', views.prediction, name='prediction'),
]
