from django.urls import path

from .views import BazaarCheckoutView, BazaarVerifyView, SubscriptionStatusView

urlpatterns = [
    path("subscription/status/", SubscriptionStatusView.as_view()),
    path("subscription/bazaar/checkout/", BazaarCheckoutView.as_view()),
    path("subscription/bazaar/verify/", BazaarVerifyView.as_view()),
]
