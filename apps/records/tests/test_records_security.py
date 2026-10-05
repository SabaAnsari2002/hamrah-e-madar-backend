from datetime import timedelta
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.models import User
from apps.pregnancies.models import Pregnancy
from apps.records.models import PrenatalVisit,LabRecord,UltrasoundRecord
class RecordOwnershipTests(APITestCase):
    def setUp(self):
        self.a=User.objects.create_user('09120000000');self.b=User.objects.create_user('09121111111');self.pa=Pregnancy.objects.create(user=self.a,lmp_date=timezone.localdate()-timedelta(days=100),estimated_due_date=timezone.localdate()+timedelta(days=180));self.pb=Pregnancy.objects.create(user=self.b,lmp_date=timezone.localdate()-timedelta(days=100),estimated_due_date=timezone.localdate()+timedelta(days=180));self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {RefreshToken.for_user(self.a).access_token}')
    def test_cannot_read_other_user_visit_lab_ultrasound(self):
        v=PrenatalVisit.objects.create(pregnancy=self.pb,provider_name='Other',provider_type='DOCTOR',scheduled_at=timezone.now(),status='UPCOMING');l=LabRecord.objects.create(pregnancy=self.pb,title='CBC',performed_at=timezone.now(),status='COMPLETED');u=UltrasoundRecord.objects.create(pregnancy=self.pb,title='US',performed_at=timezone.now(),gestational_week=20)
        self.assertEqual(self.client.get(f'/api/v1/visits/{v.id}/').status_code,404);self.assertEqual(self.client.get(f'/api/v1/labs/{l.id}/').status_code,404);self.assertEqual(self.client.get(f'/api/v1/ultrasounds/{u.id}/').status_code,404)
