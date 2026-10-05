from rest_framework.permissions import BasePermission

from .exceptions import SubscriptionRequired
from .services import has_premium_access


class HasPremiumAccess(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if not has_premium_access(request.user):
            raise SubscriptionRequired()
        return True
