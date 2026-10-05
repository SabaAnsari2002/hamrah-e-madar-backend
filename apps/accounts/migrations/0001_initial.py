import uuid
from django.conf import settings
from django.db import migrations, models
import django.utils.timezone
import django.contrib.auth.models
import django.contrib.auth.validators
import apps.accounts.models

class Migration(migrations.Migration):
    initial=True
    dependencies=[('auth','0012_alter_user_first_name_max_length')]
    operations=[
        migrations.CreateModel(
            name='User',
            fields=[
                ('password',models.CharField(max_length=128,verbose_name='password')),
                ('last_login',models.DateTimeField(blank=True,null=True,verbose_name='last login')),
                ('is_superuser',models.BooleanField(default=False,help_text='Designates that this user has all permissions without explicitly assigning them.',verbose_name='superuser status')),
                ('id',models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True,serialize=False)),
                ('phone_number',models.CharField(db_index=True,max_length=16,unique=True)),
                ('display_name',models.CharField(blank=True,max_length=80)),
                ('is_active',models.BooleanField(default=True)),('is_staff',models.BooleanField(default=False)),('date_joined',models.DateTimeField(auto_now_add=True)),
                ('groups',models.ManyToManyField(blank=True,help_text='The groups this user belongs to.',related_name='user_set',related_query_name='user',to='auth.group',verbose_name='groups')),
                ('user_permissions',models.ManyToManyField(blank=True,help_text='Specific permissions for this user.',related_name='user_set',related_query_name='user',to='auth.permission',verbose_name='user permissions')),
            ],
            options={'abstract':False}, managers=[('objects',apps.accounts.models.UserManager())]
        ),
        migrations.CreateModel(name='OTPChallenge',fields=[
            ('id',models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True,serialize=False)),('phone_number',models.CharField(db_index=True,max_length=16)),('code_hash',models.CharField(max_length=128)),('expires_at',models.DateTimeField(db_index=True)),('attempt_count',models.PositiveSmallIntegerField(default=0)),('is_used',models.BooleanField(default=False)),('created_at',models.DateTimeField(auto_now_add=True,db_index=True)),('request_ip',models.GenericIPAddressField(blank=True,db_index=True,null=True))],options={'ordering':['-created_at']}),
        migrations.AddIndex(model_name='otpchallenge',index=models.Index(fields=['phone_number','created_at'],name='accounts_ot_phone__4e68b0_idx')),
    ]
