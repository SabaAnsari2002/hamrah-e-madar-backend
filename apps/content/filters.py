import django_filters
from .models import Article
class ArticleFilter(django_filters.FilterSet):
    category=django_filters.CharFilter(field_name='category__code')
    week=django_filters.NumberFilter(method='filter_week')
    def filter_week(self,qs,name,value):
        return qs.filter(week_from__lte=value,week_to__gte=value)
    class Meta:model=Article;fields=['category','week']
