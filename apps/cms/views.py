from datetime import timedelta

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
from apps.subscriptions.models import BazaarSubscription, SubscriptionProfile


def _percent(part: int, total: int) -> int:
    if not total:
        return 0
    return round((part / total) * 100)


@method_decorator(staff_member_required(login_url='/admin/login/'), name='dispatch')
class CmsDashboardView(View):
    template_name = 'cms/dashboard.html'

    def get(self, request):
        now = timezone.now()
        week_ago = now - timedelta(days=7)

        total_users = User.objects.count()
        new_users_week = User.objects.filter(date_joined__gte=week_ago).count()
        google_users = User.objects.filter(auth_provider=User.AuthProvider.GOOGLE).count()
        phone_users = total_users - google_users

        active_pregnancies = Pregnancy.objects.filter(status=Pregnancy.Status.ACTIVE).count()
        published_articles = Article.objects.filter(is_published=True).count()
        draft_articles = Article.objects.filter(is_published=False).count()
        pending_reminders = Reminder.objects.filter(scheduled_at__gte=now, is_completed=False).count()
        active_subscriptions = BazaarSubscription.objects.filter(
            status=BazaarSubscription.Status.ACTIVE,
            expires_at__gt=now,
        ).count()
        active_trials = SubscriptionProfile.objects.filter(trial_ends_at__gt=now).count()

        stats = {
            'users': total_users,
            'new_users_week': new_users_week,
            'active_pregnancies': active_pregnancies,
            'published_articles': published_articles,
            'draft_articles': draft_articles,
            'pending_reminders': pending_reminders,
            'active_subscriptions': active_subscriptions,
            'active_trials': active_trials,
        }

        auth_mix = {
            'google': google_users,
            'phone': phone_users,
            'google_percent': _percent(google_users, total_users),
            'phone_percent': _percent(phone_users, total_users),
        }

        subscription_rows = list(
            BazaarSubscription.objects.values('status').annotate(total=Count('id')).order_by('-total')
        )
        subscription_total = sum(row['total'] for row in subscription_rows)
        for row in subscription_rows:
            row['percent'] = _percent(row['total'], subscription_total)

        recent_users = User.objects.order_by('-date_joined')[:6]
        upcoming_reminders = Reminder.objects.filter(
            scheduled_at__gte=now,
            is_completed=False,
        ).select_related('user').order_by('scheduled_at')[:7]
        latest_subscriptions = BazaarSubscription.objects.select_related('user').order_by('-verified_at')[:7]
        recent_audits = AuditLog.objects.select_related('user').order_by('-created_at')[:7]

        management_sections = [
            {
                'title': 'کاربران',
                'subtitle': 'حساب‌ها، نقش‌ها و وضعیت دسترسی',
                'url': reverse('admin:accounts_user_changelist'),
                'icon': 'users',
                'tone': 'rose',
            },
            {
                'title': 'بارداری‌ها',
                'subtitle': 'پرونده‌ها و هفته‌های بارداری',
                'url': reverse('admin:pregnancies_pregnancy_changelist'),
                'icon': 'pregnancy',
                'tone': 'violet',
            },
            {
                'title': 'سلامت مادر',
                'subtitle': 'وزن، فشار خون، قند و علائم',
                'url': reverse('admin:health_weightmeasurement_changelist'),
                'icon': 'health',
                'tone': 'mint',
            },
            {
                'title': 'سوابق پزشکی',
                'subtitle': 'ویزیت، آزمایش، سونوگرافی و دارو',
                'url': reverse('admin:records_prenatalvisit_changelist'),
                'icon': 'records',
                'tone': 'blue',
            },
            {
                'title': 'محتوا',
                'subtitle': 'مقالات، دسته‌بندی و انتشار',
                'url': reverse('admin:content_article_changelist'),
                'icon': 'articles',
                'tone': 'amber',
            },
            {
                'title': 'مراقبت‌ها',
                'subtitle': 'تسک‌های مراقبتی و برنامه هفتگی',
                'url': reverse('admin:care_usercaretask_changelist'),
                'icon': 'care',
                'tone': 'peach',
            },
            {
                'title': 'یادآوری‌ها',
                'subtitle': 'زمان‌بندی و وضعیت انجام',
                'url': reverse('admin:reminders_reminder_changelist'),
                'icon': 'reminder',
                'tone': 'sky',
            },
            {
                'title': 'اشتراک‌ها',
                'subtitle': 'Trial، خرید بازار و اعتبار اشتراک',
                'url': reverse('admin:subscriptions_bazaarsubscription_changelist'),
                'icon': 'diamond',
                'tone': 'indigo',
            },
            {
                'title': 'گزارش فعالیت',
                'subtitle': 'لاگ ورود و رویدادهای مدیریتی',
                'url': reverse('admin:audit_auditlog_changelist'),
                'icon': 'audit',
                'tone': 'slate',
            },
        ]

        context = {
            'now': now,
            'stats': stats,
            'auth_mix': auth_mix,
            'recent_users': recent_users,
            'upcoming_reminders': upcoming_reminders,
            'latest_subscriptions': latest_subscriptions,
            'recent_audits': recent_audits,
            'management_sections': management_sections,
            'subscription_mix': subscription_rows,
        }
        return render(request, self.template_name, context)
