from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.models import User
from apps.content.models import ArticleCategory,Article
class ArticleVisibilityTests(APITestCase):
    def test_only_published_articles_are_visible(self):
        u=User.objects.create_user('09120000000');self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {RefreshToken.for_user(u).access_token}');c=ArticleCategory.objects.create(code='PREGNANCY',title='Pregnancy');Article.objects.create(title='Published',slug='published',summary='x',body='x',category=c,is_published=True,published_at=timezone.now());Article.objects.create(title='Draft',slug='draft',summary='x',body='x',category=c,is_published=False)
        r=self.client.get('/api/v1/articles/');self.assertEqual(r.status_code,200);titles=[x['title'] for x in r.data['results']];self.assertIn('Published',titles);self.assertNotIn('Draft',titles);self.assertEqual(self.client.get('/api/v1/articles/draft/').status_code,404)
