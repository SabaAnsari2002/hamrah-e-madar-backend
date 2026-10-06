from django.test import TestCase

from apps.accounts.models import User


class CmsDashboardTests(TestCase):
    def test_dashboard_redirects_anonymous_user_to_admin_login(self):
        response = self.client.get('/cms/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)

    def test_staff_user_can_render_modern_dashboard(self):
        user = User.objects.create_user(
            phone_number='09125550000',
            display_name='مدیر تست',
            is_staff=True,
        )
        self.client.force_login(user)
        response = self.client.get('/cms/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'داشبورد مدیریت')
        self.assertContains(response, 'بخش‌های مدیریتی')
        self.assertContains(response, 'همراه‌مادر')
