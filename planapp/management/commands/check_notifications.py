from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from planapp.models import Plan
from django.conf import settings

class Command(BaseCommand):
    help = 'Check for upcoming deadlines and send notifications'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        upcoming_plans = Plan.objects.filter(deadline__lte=now + timezone.timedelta(days=1), is_completed=False)
        for plan in upcoming_plans:
            send_mail(
                'Upcoming Deadline for Your Plan',
                f'Your plan "{plan.name}" is due soon!',
                settings.DEFAULT_FROM_EMAIL,
                [plan.user.email],
                fail_silently=False,
            )
        self.stdout.write(self.style.SUCCESS('Notifications sent for upcoming deadlines.'))