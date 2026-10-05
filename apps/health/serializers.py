from rest_framework import serializers
from .models import *
class WeightSerializer(serializers.ModelSerializer):
    class Meta: model=WeightMeasurement;fields=['id','pregnancy','value_kg','measured_at','note','created_at','updated_at'];read_only_fields=['id','created_at','updated_at']
class BloodPressureSerializer(serializers.ModelSerializer):
    class Meta: model=BloodPressureMeasurement;fields=['id','pregnancy','systolic','diastolic','pulse','measured_at','note','created_at','updated_at'];read_only_fields=['id','created_at','updated_at']
class BloodGlucoseSerializer(serializers.ModelSerializer):
    class Meta: model=BloodGlucoseMeasurement;fields=['id','pregnancy','value','measurement_type','measured_at','note','created_at','updated_at'];read_only_fields=['id','created_at','updated_at']
class SymptomSerializer(serializers.ModelSerializer):
    class Meta: model=SymptomEntry;fields=['id','pregnancy','symptom_type','severity','occurred_at','note','created_at','updated_at'];read_only_fields=['id','created_at','updated_at']
