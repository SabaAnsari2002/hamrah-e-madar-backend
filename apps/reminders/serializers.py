from rest_framework import serializers
from .models import Reminder
class ReminderSerializer(serializers.ModelSerializer):
    class Meta:model=Reminder;fields=['id','pregnancy','title','type','scheduled_at','is_completed','note','created_at','updated_at'];read_only_fields=['id','created_at','updated_at']
    def validate_pregnancy(self,p):
        if p and p.user_id!=self.context['request'].user.id:raise serializers.ValidationError('Invalid pregnancy.')
        return p
