from django.contrib import admin

from .models import BazaarCheckoutNonce, BazaarSubscription, SubscriptionProfile


@admin.register(SubscriptionProfile)
class SubscriptionProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "trial_started_at", "trial_ends_at", "updated_at")
    search_fields = ("user__phone_number",)


@admin.register(BazaarSubscription)
class BazaarSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "product_id", "status", "expires_at", "auto_renewing", "verified_at")
    list_filter = ("status", "product_id", "auto_renewing")
    search_fields = ("user__phone_number", "order_id")
    readonly_fields = ("purchase_token", "provider_response", "created_at", "updated_at")


@admin.register(BazaarCheckoutNonce)
class BazaarCheckoutNonceAdmin(admin.ModelAdmin):
    list_display = ("user", "expires_at", "used_at", "created_at")
    search_fields = ("user__phone_number", "nonce")
