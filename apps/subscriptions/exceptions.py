from rest_framework.exceptions import APIException


class SubscriptionRequired(APIException):
    status_code = 402
    default_detail = "An active trial or subscription is required for this feature."
    default_code = "subscription_required"
