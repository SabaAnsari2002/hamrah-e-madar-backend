import uuid
from pathlib import Path
from django.core.exceptions import ValidationError
from django.db import models
from apps.pregnancies.models import Pregnancy

def medical_file_validator(f):
    if f.size > 5*1024*1024: raise ValidationError('File must be 5 MB or smaller.')
    if Path(f.name).suffix.lower() not in {'.pdf','.jpg','.jpeg','.png'}: raise ValidationError('Allowed file types: PDF, JPG, JPEG, PNG.')

def upload_to(instance, filename): return f'medical/{instance.pregnancy_id}/{uuid.uuid4()}{Path(filename).suffix.lower()}'

class PrenatalVisit(models.Model):
    class ProviderType(models.TextChoices): DOCTOR='DOCTOR','Doctor'; MIDWIFE='MIDWIFE','Midwife'; OTHER='OTHER','Other'
    class Status(models.TextChoices): UPCOMING='UPCOMING','Upcoming'; COMPLETED='COMPLETED','Completed'; CANCELLED='CANCELLED','Cancelled'
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); pregnancy=models.ForeignKey(Pregnancy,on_delete=models.CASCADE,related_name='visits')
    provider_name=models.CharField(max_length=160); provider_type=models.CharField(max_length=12,choices=ProviderType.choices); clinic_name=models.CharField(max_length=200,blank=True); scheduled_at=models.DateTimeField(db_index=True); status=models.CharField(max_length=12,choices=Status.choices,db_index=True); notes=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['-scheduled_at']

class VisitQuestion(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); visit=models.ForeignKey(PrenatalVisit,on_delete=models.CASCADE,related_name='questions')
    question=models.TextField(); is_answered=models.BooleanField(default=False); answer_note=models.TextField(blank=True); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)

class LabRecord(models.Model):
    class Status(models.TextChoices): SCHEDULED='SCHEDULED','Scheduled'; COMPLETED='COMPLETED','Completed'; CANCELLED='CANCELLED','Cancelled'
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); pregnancy=models.ForeignKey(Pregnancy,on_delete=models.CASCADE,related_name='labs'); title=models.CharField(max_length=200); performed_at=models.DateTimeField(db_index=True); status=models.CharField(max_length=12,choices=Status.choices,db_index=True); result_summary=models.TextField(blank=True); notes=models.TextField(blank=True); attachment=models.FileField(upload_to=upload_to,validators=[medical_file_validator],blank=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['-performed_at']

class UltrasoundRecord(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); pregnancy=models.ForeignKey(Pregnancy,on_delete=models.CASCADE,related_name='ultrasounds'); title=models.CharField(max_length=200); performed_at=models.DateTimeField(db_index=True); gestational_week=models.PositiveSmallIntegerField(); center_name=models.CharField(max_length=200,blank=True); summary=models.TextField(blank=True); notes=models.TextField(blank=True); attachment=models.FileField(upload_to=upload_to,validators=[medical_file_validator],blank=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['-performed_at']

class Medication(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); pregnancy=models.ForeignKey(Pregnancy,on_delete=models.CASCADE,related_name='medications'); name=models.CharField(max_length=160); dosage_text=models.CharField(max_length=200,blank=True); schedule_text=models.CharField(max_length=200,blank=True); start_date=models.DateField(); end_date=models.DateField(null=True,blank=True); notes=models.TextField(blank=True); is_active=models.BooleanField(default=True,db_index=True); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['-is_active','name']

class MedicationIntake(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); medication=models.ForeignKey(Medication,on_delete=models.CASCADE,related_name='intakes'); date=models.DateField(); completed=models.BooleanField(default=True); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: constraints=[models.UniqueConstraint(fields=['medication','date'],name='unique_medication_intake_date')]
