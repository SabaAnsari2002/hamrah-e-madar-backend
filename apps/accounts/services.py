import secrets
from datetime import timedelta
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import Throttled, ValidationError
from .models import OTPChallenge, User

OTP_TTL=timedelta(minutes=2); RESEND_COOLDOWN=timedelta(seconds=60); MAX_ATTEMPTS=5

class SMSProvider:
    def send_otp(self, phone_number:str, code:str)->None: raise NotImplementedError
class ConsoleSMSProvider(SMSProvider):
    def send_otp(self,phone_number,code):
        if not settings.DEBUG: raise RuntimeError('ConsoleSMSProvider is development-only')
        print(f'[DEV OTP] {phone_number}: {code}')

def normalize_phone(raw):
    try: return User.objects.normalize_phone(raw)
    except ValueError: raise ValidationError({'phone_number':['Enter a valid Iranian mobile number.']})

def _enforce_request_limits(phone, ip):
    now=timezone.now()
    latest=OTPChallenge.objects.filter(phone_number=phone).order_by('-created_at').first()
    if latest and latest.created_at > now-RESEND_COOLDOWN: raise Throttled(detail='Please wait before requesting another code.', wait=60)
    if OTPChallenge.objects.filter(phone_number=phone,created_at__gte=now-timedelta(minutes=10)).count()>=5: raise Throttled(detail='Too many OTP requests for this phone number.',wait=600)
    if ip and OTPChallenge.objects.filter(request_ip=ip,created_at__gte=now-timedelta(minutes=10)).count()>=20: raise Throttled(detail='Too many OTP requests from this address.',wait=600)

def request_otp(phone_number, ip=None, provider=None):
    phone=normalize_phone(phone_number); _enforce_request_limits(phone,ip)
    code='123456' if settings.DEBUG else f'{secrets.randbelow(1_000_000):06d}'
    challenge=OTPChallenge.objects.create(phone_number=phone,code_hash=make_password(code),expires_at=timezone.now()+OTP_TTL,request_ip=ip)
    (provider or ConsoleSMSProvider()).send_otp(phone,code)
    return challenge

@transaction.atomic
def verify_otp(phone_number, code):
    phone=normalize_phone(phone_number)
    challenge=OTPChallenge.objects.select_for_update().filter(phone_number=phone,is_used=False).order_by('-created_at').first()
    if not challenge: raise ValidationError({'code':['No active code found.']})
    if challenge.expires_at <= timezone.now(): challenge.is_used=True; challenge.save(update_fields=['is_used']); raise ValidationError({'code':['The code has expired.']})
    if challenge.attempt_count>=MAX_ATTEMPTS: raise ValidationError({'code':['Maximum verification attempts reached.']})
    challenge.attempt_count+=1
    if not check_password(str(code),challenge.code_hash):
        if challenge.attempt_count>=MAX_ATTEMPTS: challenge.is_used=True
        challenge.save(update_fields=['attempt_count','is_used']); raise ValidationError({'code':['The verification code is invalid.']})
    challenge.is_used=True; challenge.save(update_fields=['attempt_count','is_used'])
    user,_=User.objects.get_or_create(phone_number=phone,defaults={'display_name':''})
    return user

def delete_account(user):
    # Actual deletion: user-owned pregnancy/health/record/reminder rows cascade.
    user.delete()
