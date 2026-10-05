from rest_framework import serializers
from .models import UserCareTask
class UserCareTaskSerializer(serializers.ModelSerializer):
    title=serializers.CharField(source='template.title',read_only=True);description=serializers.CharField(source='template.description',read_only=True);category=serializers.CharField(source='template.category',read_only=True);week_from=serializers.IntegerField(source='template.week_from',read_only=True);week_to=serializers.IntegerField(source='template.week_to',read_only=True)
    class Meta:model=UserCareTask;fields=['id','pregnancy','template','title','description','category','week_from','week_to','scheduled_date','status','completed_at','created_at','updated_at'];read_only_fields=['id','pregnancy','template','title','description','category','week_from','week_to','scheduled_date','completed_at','created_at','updated_at']
