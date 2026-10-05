# Generated for Hamrah-e-Madar subscription entitlement support.
import uuid
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [("accounts", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="SubscriptionProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("trial_started_at", models.DateTimeField()),
                ("trial_ends_at", models.DateTimeField(db_index=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="subscription_profile", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="BazaarCheckoutNonce",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("nonce", models.CharField(db_index=True, max_length=96, unique=True)),
                ("expires_at", models.DateTimeField(db_index=True)),
                ("used_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="bazaar_checkout_nonces", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="BazaarSubscription",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("product_id", models.CharField(db_index=True, max_length=160)),
                ("package_name", models.CharField(max_length=240)),
                ("purchase_token", models.TextField(unique=True)),
                ("order_id", models.CharField(blank=True, db_index=True, max_length=240)),
                ("developer_payload", models.CharField(blank=True, max_length=512)),
                ("starts_at", models.DateTimeField()),
                ("expires_at", models.DateTimeField(db_index=True)),
                ("auto_renewing", models.BooleanField(default=False)),
                ("status", models.CharField(choices=[("ACTIVE", "Active"), ("EXPIRED", "Expired"), ("INVALID", "Invalid")], db_index=True, default="ACTIVE", max_length=16)),
                ("verified_at", models.DateTimeField(db_index=True)),
                ("provider_response", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(db_index=True, on_delete=django.db.models.deletion.CASCADE, related_name="bazaar_subscriptions", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-expires_at", "-verified_at"]},
        ),
        migrations.AddIndex(
            model_name="bazaarsubscription",
            index=models.Index(fields=["user", "status", "expires_at"], name="subscr_user_status_exp_idx"),
        ),
    ]
