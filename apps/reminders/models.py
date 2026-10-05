import uuid
from django.conf import settings
from django.db import models
from apps.pregnancies.models import Pregnancy
class Reminder(models.Model):
    class Type(models.TextChoices): VISIT='VISIT','Visit'; LAB='LAB','Lab'; ULTRASOUND='ULTRASOUND','Ultrasound'; MEDICATION='MEDICATION','Medication'; MEASUREMENT='MEASUREMENT','Measurement'; PERSONAL='PERSONAL','Personal'
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='reminders'); pregnancy=models.ForeignKey(Pregnancy,on_delete=models.CASCADE,null=True,blank=True,related_name='reminders'); title=models.CharField(max_length=200); type=models.CharField(max_length=20,choices=Type.choices,db_index=True); scheduled_at=models.DateTimeField(db_index=True); is_completed=models.BooleanField(default=False,db_index=True); note=models.TextField(blank=True); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['scheduled_at']
