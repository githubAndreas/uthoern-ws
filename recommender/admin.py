from django.contrib import admin
from .models import Environment, Decomposition, Model_Algorithm


# Register your models here.
admin.site.register(Environment)
admin.site.register(Decomposition)
admin.site.register(Model_Algorithm)