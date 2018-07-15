from django.http import HttpResponse
from django.shortcuts import render

from .forms import PreparationControlForm, TrainingControlForm, PredictionControlForm
from .models import Preparation_Session, Training_Session, Prediction_Session, Environment


# Create your views here.
def dataset(request):
    if request.method == "POST":
        form = PreparationControlForm(request.POST)
        if form.is_valid():
            preparation_session = form.save(commit=False)
            preparation_session.start()

    Environment.get_local()  # Validate if environment config exists

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

    Environment.get_local()  # Validate if environment config exists

    training_control_form = TrainingControlForm
    context = {'training_control_form': training_control_form,
               'training_sessions': Training_Session.objects.all()}

    return render(request, 'recommender/training.html', context)


def prediction(request):
    if request.method == "POST":
        form = PredictionControlForm(request.POST)
        if form.is_valid():
            prediction_session = form.save(commit=False)
            prediction_session.start()

    Environment.get_local()  # Validate if environment config exists

    prediction_control_form = PredictionControlForm
    context = {'prediction_control_form': prediction_control_form,
               'prediction_sessions': Prediction_Session.objects.all()}
    return render(request, 'recommender/prediction.html', context)


def download_prediction_csv(request, prediction_id):
    pred = Prediction_Session.objects.get(pk=prediction_id)
    file_path = pred.get_file_path()
    print(file_path)
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/csv")
        response['Content-Disposition'] = 'inline; filename=' + pred.export_file_name
        return response
