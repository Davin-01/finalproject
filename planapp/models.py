from django.db import models
import json

class StudyPlan(models.Model):
    title = models.CharField(max_length=100)
    references = models.JSONField()  # Store list of references
    interval = models.CharField(max_length=20)
    duration = models.IntegerField()
    events = models.JSONField()  # Store list of courses

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=200)
    time = models.DateTimeField()

    def __str__(self):
        return self.title
