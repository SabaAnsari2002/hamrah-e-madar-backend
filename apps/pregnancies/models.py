import uuid
from django.conf import settings
from django.db import models
from django.db.models import Q

class Pregnancy(models.Model):
    class Status(models.TextChoices): ACTIVE='ACTIVE','Active'; COMPLETED='COMPLETED','Completed'; ENDED='ENDED','Ended'
    class ProviderStatus(models.TextChoices): NONE='NONE','None'; DOCTOR='DOCTOR','Doctor'; MIDWIFE='MIDWIFE','Midwife'; OTHER='OTHER','Other'
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='pregnancies',db_index=True)
    status=models.CharField(max_length=16,choices=Status.choices,default=Status.ACTIVE,db_index=True)
    lmp_date=models.DateField(null=True,blank=True); estimated_due_date=models.DateField(null=True,blank=True); actual_delivery_date=models.DateField(null=True,blank=True)
    is_multiple=models.BooleanField(default=False); is_first_pregnancy=models.BooleanField(null=True,blank=True)
    provider_status=models.CharField(max_length=16,choices=ProviderStatus.choices,default=ProviderStatus.NONE)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        ordering=['-created_at']
        constraints=[models.UniqueConstraint(fields=['user'],condition=Q(status='ACTIVE'),name='one_active_pregnancy_per_user')]

class PregnancyWeek(models.Model):
    week_number=models.PositiveSmallIntegerField(primary_key=True)
    baby_summary=models.TextField(); mother_summary=models.TextField(); baby_size_text=models.CharField(max_length=160,blank=True); baby_weight_text=models.CharField(max_length=160,blank=True)
    nutrition_summary=models.TextField(blank=True); activity_summary=models.TextField(blank=True); care_summary=models.TextField(blank=True); attention_summary=models.TextField(blank=True)
    medical_reviewer=models.CharField(max_length=160,blank=True); source_information=models.TextField(blank=True,default='Demo content — source not added.')
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: constraints=[models.CheckConstraint(condition=Q(week_number__gte=1)&Q(week_number__lte=40),name='pregnancy_week_1_40')]
