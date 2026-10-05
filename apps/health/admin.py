from django.contrib import admin
from .models import *
for model in (WeightMeasurement,BloodPressureMeasurement,BloodGlucoseMeasurement,SymptomEntry):
    admin.site.register(model)
