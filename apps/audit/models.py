import uuid
from django.conf import settings
from django.db import models
class AuditLog(models.Model):
    class Action(models.TextChoices): LOGIN='LOGIN','Login'; ACCOUNT_DELETE='ACCOUNT_DELETE','Account delete'; PREGNANCY_CREATE='PREGNANCY_CREATE','Pregnancy create'; FILE_UPLOAD='FILE_UPLOAD','File upload'
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True); action=models.CharField(max_length=30,choices=Action.choices,db_index=True); object_type=models.CharField(max_length=60,blank=True); object_id=models.CharField(max_length=80,blank=True); ip_address=models.GenericIPAddressField(null=True,blank=True); created_at=models.DateTimeField(auto_now_add=True,db_index=True)
    class Meta: ordering=['-created_at']
