from datetime import date,timedelta
from django.db import IntegrityError,transaction
from django.test import TestCase
from apps.accounts.models import User
from apps.pregnancies.models import Pregnancy
from apps.pregnancies.services import calculate_age,create_pregnancy
class PregnancyTests(TestCase):
    def setUp(self):self.user=User.objects.create_user('09120000000')
    def test_gestational_age_and_due_date(self):
        today=date(2026,8,19);p=Pregnancy(user=self.user,lmp_date=date(2026,3,1),estimated_due_date=date(2026,12,6));a=calculate_age(p,today);self.assertEqual((a.gestational_age_weeks,a.gestational_age_days),(24,3));self.assertEqual(a.days_remaining,109);self.assertEqual(a.current_trimester,'SECOND')
    def test_only_one_active_pregnancy(self):
        create_pregnancy(self.user,lmp_date=date.today()-timedelta(days=100),status='ACTIVE')
        with self.assertRaises(Exception):create_pregnancy(self.user,lmp_date=date.today()-timedelta(days=200),status='ACTIVE')
