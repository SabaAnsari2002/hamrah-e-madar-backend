from rest_framework import viewsets
from .models import Article
from .serializers import ArticleListSerializer,ArticleDetailSerializer
from .filters import ArticleFilter
class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field='slug';filterset_class=ArticleFilter;ordering_fields=['published_at','reading_time'];ordering=['-published_at']
    def get_queryset(self):return Article.objects.select_related('category').filter(is_published=True)
    def get_serializer_class(self):return ArticleDetailSerializer if self.action=='retrieve' else ArticleListSerializer
