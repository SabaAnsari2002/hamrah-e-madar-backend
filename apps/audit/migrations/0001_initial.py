import uuid
from django.conf import settings
from django.db import migrations,models
class Migration(migrations.Migration):
    initial=True;dependencies=[migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations=[migrations.CreateModel(name='AuditLog',fields=[('id',models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True,serialize=False)),('action',models.CharField(choices=[('LOGIN','Login'),('ACCOUNT_DELETE','Account delete'),('PREGNANCY_CREATE','Pregnancy create'),('FILE_UPLOAD','File upload')],db_index=True,max_length=30)),('object_type',models.CharField(blank=True,max_length=60)),('object_id',models.CharField(blank=True,max_length=80)),('ip_address',models.GenericIPAddressField(blank=True,null=True)),('created_at',models.DateTimeField(auto_now_add=True,db_index=True)),('user',models.ForeignKey(blank=True,null=True,on_delete=models.deletion.SET_NULL,to=settings.AUTH_USER_MODEL))],options={'ordering':['-created_at']})]
