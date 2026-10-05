import json
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone as dt_timezone

from django.conf import settings
from django.utils import timezone


class BazaarVerificationError(Exception):
    pass


@dataclass(frozen=True)
class VerifiedBazaarSubscription:
    starts_at: datetime
    expires_at: datetime
    auto_renewing: bool
    order_id: str
    developer_payload: str
    raw: dict


def _to_datetime_millis(value) -> datetime | None:
    if value in (None, ""):
        return None
    try:
        return datetime.fromtimestamp(int(value) / 1000, tz=dt_timezone.utc)
    except (TypeError, ValueError, OSError):
        return None


def _http_json(url: str, *, method: str = "GET", data: dict | None = None, timeout: int = 12) -> dict:
    body = None
    headers = {"Accept": "application/json"}
    if data is not None:
        body = urllib.parse.urlencode(data).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    request = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw or "{}")
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise BazaarVerificationError(f"Cafe Bazaar API returned HTTP {exc.code}: {raw[:200]}") from exc
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise BazaarVerificationError("Cafe Bazaar API could not be reached or returned invalid JSON.") from exc


class BazaarDeveloperApi:
    """Minimal Cafe Bazaar Developer API v2 client for subscription verification."""

    token_url = "https://pardakht.cafebazaar.ir/devapi/v2/auth/token/"
    subscription_url = (
        "https://pardakht.cafebazaar.ir/devapi/v2/api/applications/"
        "{package_name}/subscriptions/{subscription_id}/purchases/{purchase_token}/"
    )

    def __init__(self):
        self.client_id = settings.BAZAAR_CLIENT_ID
        self.client_secret = settings.BAZAAR_CLIENT_SECRET
        self.refresh_token = settings.BAZAAR_REFRESH_TOKEN
        self.package_name = settings.BAZAAR_PACKAGE_NAME

    @property
    def configured(self) -> bool:
        return all([self.client_id, self.client_secret, self.refresh_token, self.package_name])

    def _access_token(self) -> str:
        if not self.configured:
            raise BazaarVerificationError("Cafe Bazaar Developer API credentials are not configured.")
        payload = _http_json(
            self.token_url,
            method="POST",
            data={
                "grant_type": "refresh_token",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
            },
        )
        token = payload.get("access_token")
        if not token:
            raise BazaarVerificationError("Cafe Bazaar did not return an access token.")
        return str(token)

    def validate_subscription(
        self,
        *,
        subscription_id: str,
        purchase_token: str,
        client_purchase_time_ms: int | None = None,
        client_order_id: str = "",
        client_developer_payload: str = "",
    ) -> VerifiedBazaarSubscription:
        if settings.BAZAAR_VERIFICATION_MODE == "mock":
            if not settings.DEBUG:
                raise BazaarVerificationError("Mock Bazaar verification is forbidden when DEBUG is false.")
            starts_at = _to_datetime_millis(client_purchase_time_ms) or timezone.now()
            return VerifiedBazaarSubscription(
                starts_at=starts_at,
                expires_at=starts_at + timedelta(days=365),
                auto_renewing=True,
                order_id=client_order_id,
                developer_payload=client_developer_payload,
                raw={"mode": "mock", "subscriptionId": subscription_id},
            )

        token = self._access_token()
        url = self.subscription_url.format(
            package_name=urllib.parse.quote(self.package_name, safe=""),
            subscription_id=urllib.parse.quote(subscription_id, safe=""),
            purchase_token=urllib.parse.quote(purchase_token, safe=""),
        )
        url = f"{url}?{urllib.parse.urlencode({'access_token': token})}"
        raw = _http_json(url)

        starts_at = (
            _to_datetime_millis(raw.get("startTimeMillis"))
            or _to_datetime_millis(raw.get("initiationTimestampMsec"))
            or _to_datetime_millis(client_purchase_time_ms)
        )
        expires_at = (
            _to_datetime_millis(raw.get("expiryTimeMillis"))
            or _to_datetime_millis(raw.get("validUntilTimestampMsec"))
        )
        if starts_at is None or expires_at is None:
            raise BazaarVerificationError("Cafe Bazaar subscription response did not contain valid start/expiry timestamps.")

        return VerifiedBazaarSubscription(
            starts_at=starts_at,
            expires_at=expires_at,
            auto_renewing=bool(raw.get("autoRenewing", False)),
            order_id=str(raw.get("orderId") or client_order_id or ""),
            developer_payload=str(raw.get("developerPayload") or client_developer_payload or ""),
            raw=raw,
        )
