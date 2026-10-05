from django.contrib import admin
from .models import Article,ArticleCategory
@admin.register(ArticleCategory)
class CategoryAdmin(admin.ModelAdmin):list_display=('code','title','sort_order');search_fields=('code','title');ordering=('sort_order',)
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):list_display=('title','category','week_from','week_to','is_published','published_at','last_medically_reviewed_at');search_fields=('title','summary','slug');list_filter=('category','is_published');prepopulated_fields={'slug':('title',)};readonly_fields=('created_at','updated_at')
