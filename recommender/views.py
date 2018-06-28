from django.shortcuts import render

from .forms import PreparationControlForm, TrainingControlForm, PredictionControlForm
from .models import Preparation_Session, Training_Session


# Create your views here.
def dataset(request):
    if request.method == "POST":
        form = PreparationControlForm(request.POST)
        if form.is_valid():
            preparation_session = form.save(commit=False)
            preparation_session.start()

    preparation_control_form = PreparationControlForm()
    context = {'preparation_control_form': preparation_control_form,
               'preparation_sessions': Preparation_Session.objects.all()}

    return render(request, 'recommender/dataset.html', context)


def training(request):
    if request.method == "POST":
        form = TrainingControlForm(request.POST)
        if form.is_valid():
            training_session = form.save(commit=False)
            training_session.start()

    training_control_form = TrainingControlForm
    context = {'training_control_form': training_control_form,
               'training_sessions': Training_Session.objects.all()}

    return render(request, 'recommender/training.html', context)


def prediction(request):

    prediction_control_form = PredictionControlForm
    context = {'prediction_control_form': prediction_control_form,}
    return render(request, 'recommender/prediction.html', context)
