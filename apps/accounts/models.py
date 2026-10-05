import uuid
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def normalize_phone(self, phone):
        digits = ''.join(ch for ch in str(phone) if ch.isdigit())
        if digits.startswith('0098'):
            digits = digits[4:]
        elif digits.startswith('98'):
            digits = digits[2:]
        if digits.startswith('0'):
            digits = digits[1:]
        if len(digits) != 10 or not digits.startswith('9'):
            raise ValueError('Invalid Iranian mobile number')
        return '+98' + digits

    def create_user(self, phone_number, display_name='', password=None, **extra):
        if not phone_number:
            raise ValueError('phone_number is required')
        user = self.model(
            phone_number=self.normalize_phone(phone_number),
            display_name=display_name.strip(),
            auth_provider=User.AuthProvider.PHONE,
            **extra,
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra):
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        extra.setdefault('is_active', True)
        extra.setdefault('auth_provider', User.AuthProvider.PHONE)
        if extra['is_staff'] is not True or extra['is_superuser'] is not True:
            raise ValueError('Superuser must be staff/superuser')
        return self.create_user(phone_number, password=password, **extra)


class User(AbstractBaseUser, PermissionsMixin):
    class AuthProvider(models.TextChoices):
        PHONE = 'PHONE', 'Phone'
        GOOGLE = 'GOOGLE', 'Google'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=16, unique=True, db_index=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    google_sub = models.CharField(max_length=128, unique=True, null=True, blank=True, db_index=True)
    avatar_url = models.URLField(blank=True)
    auth_provider = models.CharField(max_length=16, choices=AuthProvider.choices, default=AuthProvider.PHONE)
    display_name = models.CharField(max_length=80, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if self.phone_number:
            self.phone_number = User.objects.normalize_phone(self.phone_number)
        if self.email:
            self.email = self.email.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.phone_number or self.email or self.display_name or str(self.id)


class OTPChallenge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=16, db_index=True)
    code_hash = models.CharField(max_length=128)
    expires_at = models.DateTimeField(db_index=True)
    attempt_count = models.PositiveSmallIntegerField(default=0)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    request_ip = models.GenericIPAddressField(null=True, blank=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['phone_number', 'created_at'])]
