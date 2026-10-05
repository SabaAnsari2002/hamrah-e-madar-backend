from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .bazaar import BazaarVerificationError
from .serializers import BazaarVerifySerializer
from .services import create_checkout_payload, entitlement_payload, verify_bazaar_subscription


class SubscriptionStatusView(APIView):
    def get(self, request):
        return Response(entitlement_payload(request.user))


class BazaarCheckoutView(APIView):
    def post(self, request):
        checkout = create_checkout_payload(request.user)
        return Response(
            {
                "product_id": settings.BAZAAR_ANNUAL_SUBSCRIPTION_ID,
                "package_name": settings.BAZAAR_PACKAGE_NAME,
                "developer_payload": checkout.nonce,
                "payload_expires_at": checkout.expires_at,
            }
        )


class BazaarVerifyView(APIView):
    def post(self, request):
        serializer = BazaarVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            verify_bazaar_subscription(user=request.user, **serializer.validated_data)
        except (ValueError, BazaarVerificationError) as exc:
            return Response(
                {
                    "code": "bazaar_verification_failed",
                    "message": str(exc),
                    "errors": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(entitlement_payload(request.user))
