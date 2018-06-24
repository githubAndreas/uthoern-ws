from django.shortcuts import render

from .forms import PreparationControlForm
from .models import Environment


# Create your views here.
def dataset(request):
    if request.method == "POST":
        form = PreparationControlForm(request.POST)
        if form.is_valid():
            preparation_session = form.save(commit=False)
            preparation_session.status = "IN PROGRESS"

            environment = Environment.objects.get(name__exact='testing')

            preparation_session.environment = environment
            preparation_session.save()

    preparation_control_form = PreparationControlForm()
    context = {'preparation_control_form': preparation_control_form}

    return render(request, 'recommender/dataset.html', context)


def training(request):
    return render(request, 'recommender/training.html', {})


def prediction(request):
    return render(request, 'recommender/prediction.html', {})
