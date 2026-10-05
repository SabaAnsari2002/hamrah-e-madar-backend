from rest_framework import serializers
from .models import Article,ArticleCategory
class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:model=ArticleCategory;fields=['id','code','title']
class ArticleListSerializer(serializers.ModelSerializer):
    category=ArticleCategorySerializer(read_only=True)
    class Meta:model=Article;fields=['id','slug','title','summary','category','reading_time','week_from','week_to','medical_reviewer','last_medically_reviewed_at','source_notes','published_at']
class ArticleDetailSerializer(ArticleListSerializer):
    class Meta(ArticleListSerializer.Meta):fields=ArticleListSerializer.Meta.fields+['body']
