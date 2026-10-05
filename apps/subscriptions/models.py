import uuid

from django.conf import settings
from django.db import models


class SubscriptionProfile(models.Model):
    """Server-owned trial state. One row per application user."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscription_profile",
    )
    trial_started_at = models.DateTimeField()
    trial_ends_at = models.DateTimeField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BazaarSubscription(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        EXPIRED = "EXPIRED", "Expired"
        INVALID = "INVALID", "Invalid"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bazaar_subscriptions",
        db_index=True,
    )
    product_id = models.CharField(max_length=160, db_index=True)
    package_name = models.CharField(max_length=240)
    purchase_token = models.TextField(unique=True)
    order_id = models.CharField(max_length=240, blank=True, db_index=True)
    developer_payload = models.CharField(max_length=512, blank=True)
    starts_at = models.DateTimeField()
    expires_at = models.DateTimeField(db_index=True)
    auto_renewing = models.BooleanField(default=False)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE, db_index=True)
    verified_at = models.DateTimeField(db_index=True)
    provider_response = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-expires_at", "-verified_at"]
        indexes = [models.Index(fields=["user", "status", "expires_at"])]


class BazaarCheckoutNonce(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bazaar_checkout_nonces",
    )
    nonce = models.CharField(max_length=96, unique=True, db_index=True)
    expires_at = models.DateTimeField(db_index=True)
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
