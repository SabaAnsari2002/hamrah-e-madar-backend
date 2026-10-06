from django.test import TestCase

from apps.accounts.models import User
from apps.pregnancies.models import Pregnancy


class ModernAdminWorkspaceTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            phone_number='09121112233',
            password='StrongPass123!',
            display_name='مدیر تست',
        )
        self.client.force_login(self.admin)

    def test_user_changelist_renders_persistent_sidebar_and_header(self):
        response = self.client.get('/admin/accounts/user/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="nav-sidebar"')
        self.assertContains(response, 'hamrah-admin-brand')
        self.assertContains(response, 'hamrah-page-hero')
        self.assertContains(response, 'مدیریت')

    def test_pregnancy_changelist_renders_modern_workspace(self):
        Pregnancy.objects.create(user=self.admin, status=Pregnancy.Status.ACTIVE)
        response = self.client.get('/admin/pregnancies/pregnancy/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'hamrah-filter-panel')
        self.assertContains(response, 'hamrah-result-table')
        self.assertContains(response, 'hamrah-admin-identity')

    def test_user_change_form_keeps_workspace_chrome(self):
        response = self.client.get(f'/admin/accounts/user/{self.admin.pk}/change/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="nav-sidebar"')
        self.assertContains(response, 'hamrah-form-hero')
        self.assertContains(response, 'hamrah-submit-row')
