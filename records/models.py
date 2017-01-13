from django.db import models
from accounts.models import Patient, Doctor
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.utils import timezone

class Hospital(models.Model):
    Name = models.CharField(max_length=50)
    Number_Of_Patients = models.IntegerField(default=0)
    Average_Length_Of_Stay = models.IntegerField(default=0)

    def __str__(self):
        return self.Name


class Record(models.Model):

    Patient_Profile = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name="Record")
    Sex = models.CharField(max_length=10, blank=False, choices=(
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other")
    ))
    Weight = models.CharField(validators=[
        RegexValidator('\d{1,3}', message="Weight must contain digits")
    ], blank=False, max_length=3)
    Height_Feet = models.IntegerField(default=0, validators=[
        MaxValueValidator(9, message="Feet must not exceed 9 ft"),
        MinValueValidator(0, message="Feet must not be less than 0 ft")
    ], blank=False)

    Height_Inches = models.IntegerField(default=0, validators=[
        MaxValueValidator(11, message="Inches must not exceed 11 in"),
        MinValueValidator(0, message="Inches must not be less than 0 in")
    ], blank=False)
    Insurance_ID = models.CharField(default=0,validators=[
        RegexValidator('\d{12}', message="ID must be 12 digits")
    ], blank=False, max_length=12)
    Current_Hospital = models.ForeignKey(Hospital, blank=False, null=True)

    Admitted = models.BooleanField(default=False)
    Time_Of_Admission = models.DateTimeField(blank=True, null=True)
    Time_Of_Discharge = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.Patient_Profile.User.first_name + "'s Record"


class Prescription(models.Model):
    Patient_Record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name="Prescriptions")
    Doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    Date_Of_Issue = models.DateTimeField(default=timezone.now, blank=False)
    Drug_Name = models.CharField(default='', max_length=40)
    Drug_Strength = models.CharField(default='', max_length=6)
    Dosage_Form = models.CharField(default='', max_length=20)
    Quantity = models.IntegerField(validators=[
        MinValueValidator(1, message="Quantity must be at least 1")
    ], default=0)
    Number_Of_Refills = models.IntegerField(validators=[
        MinValueValidator(0, message="Refills must be at least 0")
    ], default=0)

    def __str__(self):
        return self.Drug_Name + ": " + self.Drug_Strength


class Test(models.Model):
    Test_Name = models.CharField(max_length=100, blank=False)
    Notes = models.TextField(max_length=500, blank=True)
    Patient_Record = models.ForeignKey(Record, on_delete=models.CASCADE, blank=False, related_name="Tests")
    Doctor = models.ForeignKey(Doctor, blank=False, related_name="Tests")
    Date = models.DateTimeField(default=timezone.now, blank=False, null=False)
    Released = models.BooleanField(default=False)

    Files = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.Test_Name
