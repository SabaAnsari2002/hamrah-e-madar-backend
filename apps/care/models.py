import uuid
from django.db import models
from apps.pregnancies.models import Pregnancy

class CareTaskTemplate(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); title=models.CharField(max_length=200); description=models.TextField(); week_from=models.PositiveSmallIntegerField(); week_to=models.PositiveSmallIntegerField(); category=models.CharField(max_length=40); is_active=models.BooleanField(default=True,db_index=True); sort_order=models.PositiveIntegerField(default=0); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['week_from','sort_order','title']

class UserCareTask(models.Model):
    class Status(models.TextChoices): PENDING='PENDING','Pending'; COMPLETED='COMPLETED','Completed'; SKIPPED='SKIPPED','Skipped'
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); pregnancy=models.ForeignKey(Pregnancy,on_delete=models.CASCADE,related_name='care_tasks'); template=models.ForeignKey(CareTaskTemplate,on_delete=models.PROTECT); scheduled_date=models.DateField(db_index=True); status=models.CharField(max_length=12,choices=Status.choices,default=Status.PENDING,db_index=True); completed_at=models.DateTimeField(null=True,blank=True); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['scheduled_date','template__sort_order']; constraints=[models.UniqueConstraint(fields=['pregnancy','template','scheduled_date'],name='unique_care_assignment')]
