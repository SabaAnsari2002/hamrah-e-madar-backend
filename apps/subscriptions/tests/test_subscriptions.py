from datetime import timedelta

from django.test import override_settings
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import User
from apps.health.models import WeightMeasurement
from apps.pregnancies.models import Pregnancy
from apps.reminders.models import Reminder
from apps.subscriptions.models import SubscriptionProfile


@override_settings(
    DEBUG=True,
    SUBSCRIPTION_TRIAL_DAYS=7,
    BAZAAR_VERIFICATION_MODE="mock",
    BAZAAR_PACKAGE_NAME="com.hamrahemadar.app",
    BAZAAR_ANNUAL_SUBSCRIPTION_ID="hamrah_madar_premium_annual",
)
class SubscriptionEntitlementTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("09120000000", display_name="Sara")
        self.pregnancy = Pregnancy.objects.create(
            user=self.user,
            lmp_date=timezone.localdate() - timedelta(days=100),
            estimated_due_date=timezone.localdate() + timedelta(days=180),
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {RefreshToken.for_user(self.user).access_token}")

    def test_trial_allows_premium_and_expiry_blocks_it(self):
        status = self.client.get("/api/v1/subscription/status/")
        self.assertEqual(status.status_code, 200)
        self.assertTrue(status.data["has_premium_access"])
        self.assertEqual(status.data["source"], "trial")

        create = self.client.post(
            "/api/v1/health/weights/",
            {
                "pregnancy": str(self.pregnancy.id),
                "value_kg": "65.20",
                "measured_at": timezone.now().isoformat(),
            },
            format="json",
        )
        self.assertEqual(create.status_code, 201)

        profile = SubscriptionProfile.objects.get(user=self.user)
        profile.trial_ends_at = timezone.now() - timedelta(seconds=1)
        profile.save(update_fields=["trial_ends_at"])
        blocked = self.client.get("/api/v1/health/weights/")
        self.assertEqual(blocked.status_code, 402)
        self.assertEqual(blocked.data["code"], "subscription_required")

    def test_mock_bazaar_purchase_activates_annual_subscription(self):
        profile = SubscriptionProfile.objects.create(
            user=self.user,
            trial_started_at=timezone.now() - timedelta(days=8),
            trial_ends_at=timezone.now() - timedelta(days=1),
        )
        checkout = self.client.post("/api/v1/subscription/bazaar/checkout/", {}, format="json")
        self.assertEqual(checkout.status_code, 200)
        purchase_time = int(timezone.now().timestamp() * 1000)
        verified = self.client.post(
            "/api/v1/subscription/bazaar/verify/",
            {
                "product_id": checkout.data["product_id"],
                "package_name": checkout.data["package_name"],
                "purchase_token": "test-token-annual-1",
                "order_id": "test-order-1",
                "developer_payload": checkout.data["developer_payload"],
                "purchase_time": purchase_time,
            },
            format="json",
        )
        self.assertEqual(verified.status_code, 200)
        self.assertTrue(verified.data["has_premium_access"])
        self.assertEqual(verified.data["source"], "bazaar_subscription")
        self.assertEqual(self.client.get("/api/v1/health/weights/").status_code, 200)

    def test_checkout_payload_cannot_be_reused_for_different_token(self):
        SubscriptionProfile.objects.create(
            user=self.user,
            trial_started_at=timezone.now() - timedelta(days=8),
            trial_ends_at=timezone.now() - timedelta(days=1),
        )
        checkout = self.client.post("/api/v1/subscription/bazaar/checkout/", {}, format="json").data
        base = {
            "product_id": checkout["product_id"],
            "package_name": checkout["package_name"],
            "order_id": "order",
            "developer_payload": checkout["developer_payload"],
            "purchase_time": int(timezone.now().timestamp() * 1000),
        }
        self.assertEqual(self.client.post("/api/v1/subscription/bazaar/verify/", {**base, "purchase_token": "token-a"}, format="json").status_code, 200)
        reused = self.client.post("/api/v1/subscription/bazaar/verify/", {**base, "purchase_token": "token-b"}, format="json")
        self.assertEqual(reused.status_code, 400)

    def test_expired_checkout_payload_can_restore_provider_verified_purchase(self):
        SubscriptionProfile.objects.create(
            user=self.user,
            trial_started_at=timezone.now() - timedelta(days=8),
            trial_ends_at=timezone.now() - timedelta(days=1),
        )
        checkout = self.client.post("/api/v1/subscription/bazaar/checkout/", {}, format="json").data
        from apps.subscriptions.models import BazaarCheckoutNonce
        nonce = BazaarCheckoutNonce.objects.get(nonce=checkout["developer_payload"])
        old_created_at = timezone.now() - timedelta(hours=2)
        old_expires_at = old_created_at + timedelta(minutes=15)
        BazaarCheckoutNonce.objects.filter(pk=nonce.pk).update(
            created_at=old_created_at,
            expires_at=old_expires_at,
        )
        purchase_time = int((old_created_at + timedelta(minutes=1)).timestamp() * 1000)
        restored = self.client.post(
            "/api/v1/subscription/bazaar/verify/",
            {
                "product_id": checkout["product_id"],
                "package_name": checkout["package_name"],
                "purchase_token": "restore-token-1",
                "order_id": "restore-order-1",
                "developer_payload": checkout["developer_payload"],
                "purchase_time": purchase_time,
            },
            format="json",
        )
        self.assertEqual(restored.status_code, 200)
        self.assertEqual(restored.data["source"], "bazaar_subscription")


@override_settings(DEBUG=True, BAZAAR_VERIFICATION_MODE="mock", SUBSCRIPTION_TRIAL_DAYS=7)
class CrossUserOwnershipRegressionTests(APITestCase):
    def setUp(self):
        self.a = User.objects.create_user("09120000000")
        self.b = User.objects.create_user("09121111111")
        self.pa = Pregnancy.objects.create(user=self.a, lmp_date=timezone.localdate() - timedelta(days=100), estimated_due_date=timezone.localdate() + timedelta(days=180))
        self.pb = Pregnancy.objects.create(user=self.b, lmp_date=timezone.localdate() - timedelta(days=100), estimated_due_date=timezone.localdate() + timedelta(days=180))
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {RefreshToken.for_user(self.a).access_token}")

    def test_pregnancy_health_and_reminders_are_account_scoped(self):
        other_weight = WeightMeasurement.objects.create(pregnancy=self.pb, value_kg="70", measured_at=timezone.now())
        other_reminder = Reminder.objects.create(user=self.b, pregnancy=self.pb, title="Other", type="PERSONAL", scheduled_at=timezone.now())
        pregnancies = self.client.get("/api/v1/pregnancies/")
        self.assertEqual(pregnancies.status_code, 200)
        ids = {row["id"] for row in pregnancies.data["results"]}
        self.assertEqual(ids, {str(self.pa.id)})
        self.assertEqual(self.client.get(f"/api/v1/health/weights/{other_weight.id}/").status_code, 404)
        self.assertEqual(self.client.get(f"/api/v1/reminders/{other_reminder.id}/").status_code, 404)
        blocked = self.client.post(
            "/api/v1/reminders/",
            {"pregnancy": str(self.pb.id), "title": "Bad", "type": "PERSONAL", "scheduled_at": timezone.now().isoformat()},
            format="json",
        )
        self.assertEqual(blocked.status_code, 400)
