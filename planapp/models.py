from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User

class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plans')
    name = models.CharField(max_length=225)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    priority = models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=2)
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('completed', 'Completed')], default='active')

    def __str__(self):
        return f'{self.name} - {self.user.username}'
