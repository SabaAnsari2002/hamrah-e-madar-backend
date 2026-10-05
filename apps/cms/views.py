from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View

from apps.accounts.models import User
from apps.audit.models import AuditLog
from apps.content.models import Article
from apps.pregnancies.models import Pregnancy
from apps.reminders.models import Reminder
from apps.subscriptions.models import BazaarSubscription


@method_decorator(staff_member_required(login_url='/admin/login/'), name='dispatch')
class CmsDashboardView(View):
    template_name = 'cms/dashboard.html'

    def get(self, request):
        now = timezone.now()
        stats = {
            'users': User.objects.count(),
            'active_pregnancies': Pregnancy.objects.filter(status=Pregnancy.Status.ACTIVE).count(),
            'published_articles': Article.objects.filter(is_published=True).count(),
            'active_subscriptions': BazaarSubscription.objects.filter(
                status=BazaarSubscription.Status.ACTIVE,
                expires_at__gt=now,
            ).count(),
        }
        recent_users = User.objects.order_by('-date_joined')[:5]
        upcoming_reminders = Reminder.objects.filter(
            scheduled_at__gte=now,
            is_completed=False,
        ).select_related('user').order_by('scheduled_at')[:6]
        latest_subscriptions = BazaarSubscription.objects.select_related('user').order_by('-verified_at')[:6]
        recent_audits = AuditLog.objects.select_related('user').order_by('-created_at')[:6]
        subscription_mix = BazaarSubscription.objects.values('status').annotate(total=Count('id')).order_by('-total')
        management_sections = [
            {'title': 'کاربران', 'subtitle': 'مدیریت حساب‌ها و نقش‌ها', 'url': reverse('admin:accounts_user_changelist'), 'icon': '👤'},
            {'title': 'بارداری‌ها', 'subtitle': 'پرونده‌های فعال و وضعیت کاربران', 'url': reverse('admin:pregnancies_pregnancy_changelist'), 'icon': '🤰'},
            {'title': 'محتوا', 'subtitle': 'مدیریت مقالات و دسته‌بندی‌ها', 'url': reverse('admin:content_article_changelist'), 'icon': '📰'},
            {'title': 'یادآوری‌ها', 'subtitle': 'پیگیری reminderها', 'url': reverse('admin:reminders_reminder_changelist'), 'icon': '⏰'},
            {'title': 'اشتراک‌ها', 'subtitle': 'کنترل trial و اشتراک بازار', 'url': reverse('admin:subscriptions_bazaarsubscription_changelist'), 'icon': '💎'},
            {'title': 'ورودها', 'subtitle': 'پیگیری لاگ‌ها و audit', 'url': reverse('admin:audit_auditlog_changelist'), 'icon': '📋'},
        ]
        context = {
            'stats': stats,
            'recent_users': recent_users,
            'upcoming_reminders': upcoming_reminders,
            'latest_subscriptions': latest_subscriptions,
            'recent_audits': recent_audits,
            'management_sections': management_sections,
            'subscription_mix': subscription_mix,
        }
        return render(request, self.template_name, context)
