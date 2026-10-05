from datetime import timedelta
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.models import User
from apps.pregnancies.models import Pregnancy
class DashboardTests(APITestCase):
    def test_shape(self):
        u=User.objects.create_user('09120000000',display_name='Sara');Pregnancy.objects.create(user=u,lmp_date=timezone.localdate()-timedelta(days=171),estimated_due_date=timezone.localdate()+timedelta(days=109));self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {RefreshToken.for_user(u).access_token}');r=self.client.get('/api/v1/dashboard/today/');self.assertEqual(r.status_code,200);self.assertEqual(set(['user','pregnancy','today_tasks','health_summary','upcoming_events','recommended_article']),set(r.data.keys()))
