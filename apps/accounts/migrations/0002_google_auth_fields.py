from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, db_index=True, max_length=16, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='google_sub',
            field=models.CharField(blank=True, db_index=True, max_length=128, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='avatar_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='auth_provider',
            field=models.CharField(choices=[('PHONE', 'Phone'), ('GOOGLE', 'Google')], default='PHONE', max_length=16),
        ),
    ]
