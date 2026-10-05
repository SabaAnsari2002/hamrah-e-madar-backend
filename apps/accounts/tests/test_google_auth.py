from unittest.mock import patch

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()


class GoogleAuthTests(APITestCase):
    @patch('apps.accounts.services._fetch_google_token_info')
    def test_google_login_creates_and_returns_jwt(self, fetch_info):
        fetch_info.return_value = {
            'aud': 'allowed-client.apps.googleusercontent.com',
            'email_verified': 'true',
            'sub': 'google-sub-1',
            'email': 'sara@example.com',
            'name': 'Sara',
            'picture': 'https://example.com/avatar.png',
        }
        with self.settings(GOOGLE_OAUTH_CLIENT_IDS=['allowed-client.apps.googleusercontent.com']):
            response = self.client.post('/api/v1/auth/google/', {'id_token': 'token-1'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        user = User.objects.get(email='sara@example.com')
        self.assertEqual(user.google_sub, 'google-sub-1')
        self.assertEqual(user.auth_provider, User.AuthProvider.GOOGLE)

    @patch('apps.accounts.services._fetch_google_token_info')
    def test_google_login_links_existing_email_user(self, fetch_info):
        user = User.objects.create(phone_number='+989121111111', email='mina@example.com', display_name='Mina')
        fetch_info.return_value = {
            'aud': 'allowed-client.apps.googleusercontent.com',
            'email_verified': 'true',
            'sub': 'google-sub-2',
            'email': 'mina@example.com',
            'name': 'Mina G',
            'picture': '',
        }
        with self.settings(GOOGLE_OAUTH_CLIENT_IDS=['allowed-client.apps.googleusercontent.com']):
            response = self.client.post('/api/v1/auth/google/', {'id_token': 'token-2'}, format='json')
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertEqual(user.google_sub, 'google-sub-2')
        self.assertEqual(user.auth_provider, User.AuthProvider.GOOGLE)
