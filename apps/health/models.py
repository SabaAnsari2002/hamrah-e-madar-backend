import uuid
from django.db import models
from django.db.models import Q
from apps.pregnancies.models import Pregnancy

class OwnedMeasurement(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    pregnancy=models.ForeignKey(Pregnancy,on_delete=models.CASCADE)
    measured_at=models.DateTimeField(db_index=True); note=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: abstract=True; ordering=['-measured_at']

class WeightMeasurement(OwnedMeasurement):
    value_kg=models.DecimalField(max_digits=6,decimal_places=2)
    class Meta(OwnedMeasurement.Meta): constraints=[models.CheckConstraint(condition=Q(value_kg__gt=0),name='weight_positive')]

class BloodPressureMeasurement(OwnedMeasurement):
    systolic=models.PositiveIntegerField(); diastolic=models.PositiveIntegerField(); pulse=models.PositiveIntegerField(null=True,blank=True)
    class Meta(OwnedMeasurement.Meta): constraints=[models.CheckConstraint(condition=Q(systolic__gt=0)&Q(diastolic__gt=0),name='bp_positive')]

class BloodGlucoseMeasurement(OwnedMeasurement):
    class Type(models.TextChoices): FASTING='FASTING','Fasting'; BEFORE_MEAL='BEFORE_MEAL','Before meal'; AFTER_MEAL='AFTER_MEAL','After meal'; OTHER='OTHER','Other'
    value=models.DecimalField(max_digits=7,decimal_places=2); measurement_type=models.CharField(max_length=20,choices=Type.choices,db_index=True)
    class Meta(OwnedMeasurement.Meta): constraints=[models.CheckConstraint(condition=Q(value__gt=0),name='glucose_positive')]

class SymptomEntry(models.Model):
    class Severity(models.TextChoices): MILD='MILD','Mild'; MODERATE='MODERATE','Moderate'; SEVERE='SEVERE','Severe'
    class Type(models.TextChoices):
        NAUSEA='NAUSEA','Nausea'; HEADACHE='HEADACHE','Headache'; BACK_PAIN='BACK_PAIN','Back pain'; FATIGUE='FATIGUE','Fatigue'; SWELLING='SWELLING','Swelling'; HEARTBURN='HEARTBURN','Heartburn'; LEG_CRAMPS='LEG_CRAMPS','Leg cramps'; SLEEP_CHANGES='SLEEP_CHANGES','Sleep changes'; MOOD_CHANGES='MOOD_CHANGES','Mood changes'; FREQUENT_URINATION='FREQUENT_URINATION','Frequent urination'; OTHER='OTHER','Other'
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); pregnancy=models.ForeignKey(Pregnancy,on_delete=models.CASCADE)
    symptom_type=models.CharField(max_length=30,choices=Type.choices,db_index=True); severity=models.CharField(max_length=12,choices=Severity.choices,db_index=True); note=models.TextField(blank=True); occurred_at=models.DateTimeField(db_index=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['-occurred_at']
