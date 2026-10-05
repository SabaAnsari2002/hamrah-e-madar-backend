from rest_framework import serializers
from .models import User


class OTPRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)


class OTPVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    code = serializers.RegexField(r'^\d{6}$')


class GoogleLoginSerializer(serializers.Serializer):
    id_token = serializers.CharField()


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'phone_number',
            'email',
            'display_name',
            'avatar_url',
            'auth_provider',
            'date_joined',
            'last_login',
        ]
        read_only_fields = [
            'id',
            'phone_number',
            'email',
            'avatar_url',
            'auth_provider',
            'date_joined',
            'last_login',
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['display_name']

    def validate_display_name(self, v):
        v = v.strip()
        if len(v) < 2:
            raise serializers.ValidationError('Display name is too short.')
        return v
