import secrets
from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from .bazaar import BazaarDeveloperApi, BazaarVerificationError
from .models import BazaarCheckoutNonce, BazaarSubscription, SubscriptionProfile


def ensure_profile(user) -> SubscriptionProfile:
    try:
        return user.subscription_profile
    except SubscriptionProfile.DoesNotExist:
        now = timezone.now()
        profile, _ = SubscriptionProfile.objects.get_or_create(
            user=user,
            defaults={
                "trial_started_at": now,
                "trial_ends_at": now + timedelta(days=settings.SUBSCRIPTION_TRIAL_DAYS),
            },
        )
        return profile


def _refresh_subscription_from_bazaar(subscription: BazaarSubscription) -> BazaarSubscription:
    now = timezone.now()
    # Avoid hammering Bazaar. Recheck stale records and always recheck once expiry is reached.
    stale = subscription.verified_at <= now - timedelta(hours=12)
    if settings.BAZAAR_VERIFICATION_MODE == "mock" or (subscription.expires_at > now and not stale):
        return subscription
    try:
        verified = BazaarDeveloperApi().validate_subscription(
            subscription_id=subscription.product_id,
            purchase_token=subscription.purchase_token,
            client_purchase_time_ms=int(subscription.starts_at.timestamp() * 1000),
            client_order_id=subscription.order_id,
            client_developer_payload=subscription.developer_payload,
        )
    except BazaarVerificationError:
        return subscription
    subscription.starts_at = verified.starts_at
    subscription.expires_at = verified.expires_at
    subscription.auto_renewing = verified.auto_renewing
    subscription.order_id = verified.order_id or subscription.order_id
    subscription.provider_response = verified.raw
    subscription.verified_at = now
    subscription.status = (
        BazaarSubscription.Status.ACTIVE
        if verified.expires_at > now
        else BazaarSubscription.Status.EXPIRED
    )
    subscription.save(update_fields=[
        "starts_at", "expires_at", "auto_renewing", "order_id",
        "provider_response", "verified_at", "status", "updated_at",
    ])
    return subscription


def active_paid_subscription(user):
    now = timezone.now()
    subscription = (
        BazaarSubscription.objects.filter(
            user=user,
            product_id=settings.BAZAAR_ANNUAL_SUBSCRIPTION_ID,
        )
        .order_by("-expires_at")
        .first()
    )
    if not subscription:
        return None

    subscription = _refresh_subscription_from_bazaar(subscription)
    desired_status = (
        BazaarSubscription.Status.ACTIVE
        if subscription.expires_at > now
        else BazaarSubscription.Status.EXPIRED
    )
    if subscription.status != desired_status:
        subscription.status = desired_status
        subscription.save(update_fields=["status", "updated_at"])
    return subscription if desired_status == BazaarSubscription.Status.ACTIVE else None


def has_premium_access(user) -> bool:
    profile = ensure_profile(user)
    if profile.trial_ends_at > timezone.now():
        return True
    return active_paid_subscription(user) is not None


def entitlement_payload(user) -> dict:
    profile = ensure_profile(user)
    now = timezone.now()
    subscription = active_paid_subscription(user)
    trial_active = profile.trial_ends_at > now
    source = "bazaar_subscription" if subscription else ("trial" if trial_active else "none")
    trial_seconds = max(0, int((profile.trial_ends_at - now).total_seconds()))
    return {
        "has_premium_access": bool(subscription or trial_active),
        "source": source,
        "annual_product_id": settings.BAZAAR_ANNUAL_SUBSCRIPTION_ID,
        "trial": {
            "started_at": profile.trial_started_at,
            "ends_at": profile.trial_ends_at,
            "is_active": trial_active,
            "seconds_remaining": trial_seconds,
        },
        "subscription": None
        if not subscription
        else {
            "product_id": subscription.product_id,
            "order_id": subscription.order_id,
            "starts_at": subscription.starts_at,
            "expires_at": subscription.expires_at,
            "auto_renewing": subscription.auto_renewing,
            "verified_at": subscription.verified_at,
        },
    }


def create_checkout_payload(user) -> BazaarCheckoutNonce:
    now = timezone.now()
    # Keep old unused payload rows so a purchase can still be restored after an app crash
    # or delayed callback. The Bazaar-verified purchase timestamp is checked against the
    # payload validity window before the payload is accepted.
    BazaarCheckoutNonce.objects.filter(
        user=user,
        used_at__isnull=False,
        created_at__lt=now - timedelta(days=400),
    ).delete()
    return BazaarCheckoutNonce.objects.create(
        user=user,
        nonce=secrets.token_urlsafe(32),
        expires_at=now + timedelta(minutes=15),
    )


@transaction.atomic
def verify_bazaar_subscription(
    *,
    user,
    product_id: str,
    package_name: str,
    purchase_token: str,
    order_id: str,
    developer_payload: str,
    purchase_time: int | None,
) -> BazaarSubscription:
    if product_id != settings.BAZAAR_ANNUAL_SUBSCRIPTION_ID:
        raise ValueError("Unexpected Bazaar subscription product id.")
    if package_name != settings.BAZAAR_PACKAGE_NAME:
        raise ValueError("Unexpected application package name.")

    existing = BazaarSubscription.objects.select_for_update().filter(purchase_token=purchase_token).first()
    if existing is not None and existing.user_id != user.id:
        raise ValueError("This Bazaar purchase token is already linked to another account.")

    nonce = None
    if existing is None:
        nonce = (
            BazaarCheckoutNonce.objects.select_for_update()
            .filter(user=user, nonce=developer_payload, used_at__isnull=True)
            .first()
        )
        if nonce is None:
            raise ValueError("The checkout payload is missing or has already been used.")
    elif existing.developer_payload and developer_payload != existing.developer_payload:
        raise ValueError("The checkout payload does not match the stored purchase.")

    verified = BazaarDeveloperApi().validate_subscription(
        subscription_id=product_id,
        purchase_token=purchase_token,
        client_purchase_time_ms=purchase_time,
        client_order_id=order_id,
        client_developer_payload=developer_payload,
    )
    if verified.developer_payload and verified.developer_payload != developer_payload:
        raise ValueError("Cafe Bazaar developer payload does not match this checkout.")
    if nonce is not None:
        # An expired payload may be restored later, but it is accepted only if the
        # provider-verified purchase actually started during that payload window.
        grace = timedelta(minutes=5)
        if verified.starts_at < nonce.created_at - grace or verified.starts_at > nonce.expires_at + grace:
            raise ValueError("The Bazaar purchase time does not match this checkout payload.")
    if verified.expires_at <= verified.starts_at:
        raise ValueError("Cafe Bazaar returned an invalid subscription validity window.")

    now = timezone.now()
    defaults = {
        "user": user,
        "product_id": product_id,
        "package_name": package_name,
        "order_id": verified.order_id or order_id,
        "developer_payload": developer_payload,
        "starts_at": verified.starts_at,
        "expires_at": verified.expires_at,
        "auto_renewing": verified.auto_renewing,
        "status": BazaarSubscription.Status.ACTIVE if verified.expires_at > now else BazaarSubscription.Status.EXPIRED,
        "verified_at": now,
        "provider_response": verified.raw,
    }
    subscription, _ = BazaarSubscription.objects.update_or_create(
        purchase_token=purchase_token,
        defaults=defaults,
    )
    if nonce is not None:
        nonce.used_at = now
        nonce.save(update_fields=["used_at"])
    return subscription
