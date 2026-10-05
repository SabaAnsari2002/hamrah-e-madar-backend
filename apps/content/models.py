import uuid
from django.db import models

class ArticleCategory(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); code=models.CharField(max_length=40,unique=True); title=models.CharField(max_length=100); sort_order=models.PositiveIntegerField(default=0)
    class Meta: ordering=['sort_order','title']
    def __str__(self): return self.title

class Article(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); title=models.CharField(max_length=240); slug=models.SlugField(max_length=260,unique=True); summary=models.TextField(); body=models.TextField(); category=models.ForeignKey(ArticleCategory,on_delete=models.PROTECT,related_name='articles'); cover_image=models.ImageField(upload_to='article-covers/',blank=True); reading_time=models.PositiveSmallIntegerField(default=5); week_from=models.PositiveSmallIntegerField(null=True,blank=True,db_index=True); week_to=models.PositiveSmallIntegerField(null=True,blank=True); medical_reviewer=models.CharField(max_length=160,blank=True); last_medically_reviewed_at=models.DateField(null=True,blank=True); source_notes=models.TextField(blank=True,default='Demo content — source not added.'); is_published=models.BooleanField(default=False,db_index=True); published_at=models.DateTimeField(null=True,blank=True,db_index=True); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['-published_at','title']
