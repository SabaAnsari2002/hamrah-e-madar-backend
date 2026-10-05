import json
import secrets
from datetime import timedelta
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import APIException, Throttled, ValidationError

from .models import OTPChallenge, User

OTP_TTL = timedelta(minutes=2)
RESEND_COOLDOWN = timedelta(seconds=60)
MAX_ATTEMPTS = 5


class SMSProvider:
    def send_otp(self, phone_number: str, code: str) -> None:
        raise NotImplementedError


class ConsoleSMSProvider(SMSProvider):
    def send_otp(self, phone_number, code):
        if not settings.DEBUG:
            raise RuntimeError('ConsoleSMSProvider is development-only')
        print(f'[DEV OTP] {phone_number}: {code}')


class GoogleAuthFailed(APIException):
    status_code = 400
    default_detail = 'Google sign-in failed.'


class GoogleTokenVerificationUnavailable(APIException):
    status_code = 503
    default_detail = 'Google token verification service is unavailable.'


def normalize_phone(raw):
    try:
        return User.objects.normalize_phone(raw)
    except ValueError:
        raise ValidationError({'phone_number': ['Enter a valid Iranian mobile number.']})


def _enforce_request_limits(phone, ip):
    now = timezone.now()
    latest = OTPChallenge.objects.filter(phone_number=phone).order_by('-created_at').first()
    if latest and latest.created_at > now - RESEND_COOLDOWN:
        raise Throttled(detail='Please wait before requesting another code.', wait=60)
    if OTPChallenge.objects.filter(phone_number=phone, created_at__gte=now - timedelta(minutes=10)).count() >= 5:
        raise Throttled(detail='Too many OTP requests for this phone number.', wait=600)
    if ip and OTPChallenge.objects.filter(request_ip=ip, created_at__gte=now - timedelta(minutes=10)).count() >= 20:
        raise Throttled(detail='Too many OTP requests from this address.', wait=600)


def request_otp(phone_number, ip=None, provider=None):
    phone = normalize_phone(phone_number)
    _enforce_request_limits(phone, ip)
    code = '123456' if settings.DEBUG else f'{secrets.randbelow(1_000_000):06d}'
    challenge = OTPChallenge.objects.create(
        phone_number=phone,
        code_hash=make_password(code),
        expires_at=timezone.now() + OTP_TTL,
        request_ip=ip,
    )
    (provider or ConsoleSMSProvider()).send_otp(phone, code)
    return challenge


@transaction.atomic
def verify_otp(phone_number, code):
    phone = normalize_phone(phone_number)
    challenge = OTPChallenge.objects.select_for_update().filter(phone_number=phone, is_used=False).order_by('-created_at').first()
    if not challenge:
        raise ValidationError({'code': ['No active code found.']})
    if challenge.expires_at <= timezone.now():
        challenge.is_used = True
        challenge.save(update_fields=['is_used'])
        raise ValidationError({'code': ['The code has expired.']})
    if challenge.attempt_count >= MAX_ATTEMPTS:
        raise ValidationError({'code': ['Maximum verification attempts reached.']})
    challenge.attempt_count += 1
    if not check_password(str(code), challenge.code_hash):
        if challenge.attempt_count >= MAX_ATTEMPTS:
            challenge.is_used = True
        challenge.save(update_fields=['attempt_count', 'is_used'])
        raise ValidationError({'code': ['The verification code is invalid.']})
    challenge.is_used = True
    challenge.save(update_fields=['attempt_count', 'is_used'])
    user, _ = User.objects.get_or_create(
        phone_number=phone,
        defaults={'display_name': '', 'auth_provider': User.AuthProvider.PHONE},
    )
    from apps.subscriptions.services import ensure_profile
    ensure_profile(user)
    return user


def _fetch_google_token_info(id_token: str) -> dict:
    url = 'https://oauth2.googleapis.com/tokeninfo?' + urlencode({'id_token': id_token})
    try:
        with urlopen(url, timeout=10) as response:
            return json.loads(response.read().decode('utf-8'))
    except HTTPError as exc:
        raise GoogleAuthFailed(f'Google token was rejected ({exc.code}).')
    except URLError:
        raise GoogleTokenVerificationUnavailable()


def verify_google_id_token(id_token: str) -> dict:
    data = _fetch_google_token_info(id_token)
    aud = data.get('aud', '').strip()
    if settings.GOOGLE_OAUTH_CLIENT_IDS and aud not in settings.GOOGLE_OAUTH_CLIENT_IDS:
        raise GoogleAuthFailed('Google client id is not allowed for this backend.')
    if str(data.get('email_verified')).lower() not in {'true', '1'}:
        raise GoogleAuthFailed('Google account email is not verified.')
    sub = (data.get('sub') or '').strip()
    email = (data.get('email') or '').strip().lower()
    if not sub or not email:
        raise GoogleAuthFailed('Google token is missing required identity fields.')
    return {
        'sub': sub,
        'email': email,
        'display_name': (data.get('name') or '').strip(),
        'avatar_url': (data.get('picture') or '').strip(),
    }


@transaction.atomic
def login_with_google(id_token: str) -> User:
    identity = verify_google_id_token(id_token)
    user = User.objects.select_for_update().filter(google_sub=identity['sub']).first()
    if user is None:
        user = User.objects.select_for_update().filter(email=identity['email']).first()
    if user is None:
        user = User.objects.create(
            phone_number=None,
            email=identity['email'],
            google_sub=identity['sub'],
            avatar_url=identity['avatar_url'],
            display_name=identity['display_name'],
            auth_provider=User.AuthProvider.GOOGLE,
            is_active=True,
        )
        user.set_unusable_password()
        user.save(update_fields=['password'])
    else:
        update_fields = []
        if not user.google_sub:
            user.google_sub = identity['sub']
            update_fields.append('google_sub')
        if not user.email:
            user.email = identity['email']
            update_fields.append('email')
        if identity['avatar_url'] and user.avatar_url != identity['avatar_url']:
            user.avatar_url = identity['avatar_url']
            update_fields.append('avatar_url')
        if identity['display_name'] and not user.display_name:
            user.display_name = identity['display_name']
            update_fields.append('display_name')
        if user.auth_provider != User.AuthProvider.GOOGLE:
            user.auth_provider = User.AuthProvider.GOOGLE
            update_fields.append('auth_provider')
        if update_fields:
            user.save(update_fields=update_fields)
    from apps.subscriptions.services import ensure_profile
    ensure_profile(user)
    return user


def delete_account(user):
    user.delete()
