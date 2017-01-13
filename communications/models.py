from django.db import models
from accounts.models import Patient, Doctor
from records.models import Hospital
from django.contrib.auth.models import User
from django.utils import timezone

class Appointment(models.Model):

    Patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="Appointments")
    Doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="Appointments")
    Hospital = models.ForeignKey(Hospital)

    Date = models.DateField()
    Time = models.TimeField()
    Purpose = models.TextField(max_length=250)

    def __str__(self):
        return "Doctor: " + str(self.Doctor) + ", Patient: " + str(self.Patient)


class Message(models.Model):
    Sender = models.ForeignKey(User, related_name='Sender')
    Receiver = models.ForeignKey(User, related_name='Receiver')
    Subject = models.CharField(max_length=100)
    Text = models.TextField(max_length=500)
    Date = models.DateTimeField(default=timezone.now)
    Viewed = models.BooleanField(default=False)

    def __str__(self):
        return self.Subject

