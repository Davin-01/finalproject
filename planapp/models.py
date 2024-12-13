from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', blank=True, null=True, default='profile_pics/default.jpg'
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plans')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    @property
    def is_overdue(self):
        if self.deadline and self.deadline < timezone.now().date():
            return True
        return False

    def __str__(self):
        return self.name


class Event(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    event_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_past_event(self):
        return self.event_date < timezone.now()

    def __str__(self):
        return self.title


@receiver(post_save, sender=User)
def manage_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
