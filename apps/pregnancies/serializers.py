from rest_framework import serializers
from .models import Pregnancy,PregnancyWeek
from .services import calculate_age,create_pregnancy
class PregnancySerializer(serializers.ModelSerializer):
    gestational_age_weeks=serializers.SerializerMethodField();gestational_age_days=serializers.SerializerMethodField();days_remaining=serializers.SerializerMethodField();current_trimester=serializers.SerializerMethodField()
    class Meta: model=Pregnancy; fields=['id','status','lmp_date','estimated_due_date','actual_delivery_date','is_multiple','is_first_pregnancy','provider_status','gestational_age_weeks','gestational_age_days','days_remaining','current_trimester','created_at','updated_at'];read_only_fields=['id','created_at','updated_at']
    def _age(self,o):
        try:return calculate_age(o)
        except Exception:return None
    def get_gestational_age_weeks(self,o): a=self._age(o);return a.gestational_age_weeks if a else None
    def get_gestational_age_days(self,o): a=self._age(o);return a.gestational_age_days if a else None
    def get_days_remaining(self,o): a=self._age(o);return a.days_remaining if a else None
    def get_current_trimester(self,o): a=self._age(o);return a.current_trimester if a else None
    def create(self,validated): return create_pregnancy(self.context['request'].user,**validated)
    def validate(self,attrs):
        if self.instance is None and not attrs.get('lmp_date') and not attrs.get('estimated_due_date'):
            raise serializers.ValidationError('Provide lmp_date or estimated_due_date.')
        status=attrs.get('status',getattr(self.instance,'status',None))
        if self.instance is not None and status==Pregnancy.Status.ACTIVE:
            if Pregnancy.objects.filter(user=self.instance.user,status=Pregnancy.Status.ACTIVE).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError({'status':'Only one active pregnancy is allowed.'})
        return attrs
class PregnancyWeekSerializer(serializers.ModelSerializer):
    class Meta: model=PregnancyWeek; fields=['week_number','baby_summary','mother_summary','baby_size_text','baby_weight_text','nutrition_summary','activity_summary','care_summary','attention_summary','medical_reviewer','source_information','updated_at']
