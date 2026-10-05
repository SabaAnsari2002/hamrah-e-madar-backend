from rest_framework import serializers


class BazaarVerifySerializer(serializers.Serializer):
    product_id = serializers.CharField(max_length=160)
    package_name = serializers.CharField(max_length=240)
    purchase_token = serializers.CharField(max_length=4096)
    order_id = serializers.CharField(max_length=240, allow_blank=True, required=False, default="")
    developer_payload = serializers.CharField(max_length=512)
    purchase_time = serializers.IntegerField(min_value=0, required=False, allow_null=True)
