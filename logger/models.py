from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from records.models import Hospital


class DailyLog(models.Model):
    Date = models.DateField(default=timezone.now)
    Hospital = models.ForeignKey(Hospital, null=True, related_name="DailyLogs")

    def __str__(self):
        return str(self.Hospital) + ": " + str(self.Date)


class Activity(models.Model):
    Log = models.ForeignKey(DailyLog, related_name="Activities")
    User = models.ForeignKey(User)
    Date = models.DateTimeField(default=timezone.now)
    Entry = models.TextField(max_length=100)

    def __str__(self):
        return self.Entry

