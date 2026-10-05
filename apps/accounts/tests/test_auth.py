from datetime import timedelta
from django.test import override_settings
from django.utils import timezone
from rest_framework.test import APITestCase
from django.contrib.auth.hashers import make_password
from apps.accounts.models import OTPChallenge,User

@override_settings(DEBUG=True)
class OTPTests(APITestCase):
    phone='09120000000'
    def request_code(self): return self.client.post('/api/v1/auth/otp/request/',{'phone_number':self.phone},format='json')
    def test_request_and_successful_verify_returns_jwt(self):
        self.assertEqual(self.request_code().status_code,200)
        r=self.client.post('/api/v1/auth/otp/verify/',{'phone_number':self.phone,'code':'123456'},format='json')
        self.assertEqual(r.status_code,200);self.assertIn('access',r.data);self.assertIn('refresh',r.data);self.assertTrue(User.objects.filter(phone_number='+989120000000').exists())
        challenge=OTPChallenge.objects.latest('created_at');self.assertTrue(challenge.is_used);self.assertNotEqual(challenge.code_hash,'123456')
    def test_wrong_expired_used_and_attempt_limit(self):
        self.request_code(); wrong=self.client.post('/api/v1/auth/otp/verify/',{'phone_number':self.phone,'code':'000000'},format='json');self.assertEqual(wrong.status_code,400)
        c=OTPChallenge.objects.latest('created_at');c.expires_at=timezone.now()-timedelta(seconds=1);c.save(update_fields=['expires_at']);expired=self.client.post('/api/v1/auth/otp/verify/',{'phone_number':self.phone,'code':'123456'},format='json');self.assertEqual(expired.status_code,400)
        OTPChallenge.objects.create(phone_number='+989120000000',code_hash=make_password('123456'),expires_at=timezone.now()+timedelta(minutes=2),attempt_count=5,is_used=False)
        limited=self.client.post('/api/v1/auth/otp/verify/',{'phone_number':self.phone,'code':'123456'},format='json');self.assertEqual(limited.status_code,400)
    def test_refresh_logout_and_account_delete(self):
        self.request_code();login=self.client.post('/api/v1/auth/otp/verify/',{'phone_number':self.phone,'code':'123456'},format='json');access=login.data['access'];refresh=login.data['refresh'];self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        self.assertEqual(self.client.get('/api/v1/me/').status_code,200);self.assertEqual(self.client.patch('/api/v1/me/',{'display_name':'Sara'},format='json').status_code,200)
        self.assertEqual(self.client.post('/api/v1/auth/logout/',{'refresh':refresh},format='json').status_code,204)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}');self.assertEqual(self.client.delete('/api/v1/me/').status_code,204);self.assertFalse(User.objects.filter(phone_number='+989120000000').exists())
