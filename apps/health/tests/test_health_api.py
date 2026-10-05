from datetime import timedelta
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.models import User
from apps.pregnancies.models import Pregnancy
class HealthOwnershipTests(APITestCase):
    def setUp(self):
        self.a=User.objects.create_user('09120000000');self.b=User.objects.create_user('09121111111');self.pa=Pregnancy.objects.create(user=self.a,lmp_date=timezone.localdate()-timedelta(days=100),estimated_due_date=timezone.localdate()+timedelta(days=180));self.pb=Pregnancy.objects.create(user=self.b,lmp_date=timezone.localdate()-timedelta(days=100),estimated_due_date=timezone.localdate()+timedelta(days=180));self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {RefreshToken.for_user(self.a).access_token}')
    def test_create_list_order_and_cross_user_block(self):
        now=timezone.now();r=self.client.post('/api/v1/health/weights/',{'pregnancy':str(self.pa.id),'value_kg':'67.40','measured_at':now.isoformat(),'note':'demo'},format='json');self.assertEqual(r.status_code,201);own_id=r.data['id']
        blocked=self.client.post('/api/v1/health/weights/',{'pregnancy':str(self.pb.id),'value_kg':'70','measured_at':now.isoformat()},format='json');self.assertEqual(blocked.status_code,400)
        self.assertEqual(self.client.get('/api/v1/health/weights/?ordering=-measured_at').status_code,200);reassign=self.client.patch(f'/api/v1/health/weights/{own_id}/',{'pregnancy':str(self.pb.id)},format='json');self.assertEqual(reassign.status_code,400)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {RefreshToken.for_user(self.b).access_token}');self.assertEqual(self.client.get(f'/api/v1/health/weights/{own_id}/').status_code,404)
    def test_other_health_resources(self):
        now=timezone.now().isoformat();self.assertEqual(self.client.post('/api/v1/health/blood-pressures/',{'pregnancy':str(self.pa.id),'systolic':112,'diastolic':72,'pulse':78,'measured_at':now},format='json').status_code,201);self.assertEqual(self.client.post('/api/v1/health/blood-glucose/',{'pregnancy':str(self.pa.id),'value':'92','measurement_type':'FASTING','measured_at':now},format='json').status_code,201);self.assertEqual(self.client.post('/api/v1/health/symptoms/',{'pregnancy':str(self.pa.id),'symptom_type':'FATIGUE','severity':'MILD','occurred_at':now},format='json').status_code,201);summary=self.client.get('/api/v1/health/summary/');self.assertEqual(summary.status_code,200);self.assertEqual(summary.data['symptoms_count_today'],1)
