from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone


def get_state_tuples():
    states = [
        ('AL', "AL"),
        ('AK', "AK"),
        ('AZ', "AZ"),
        ('AR', "AR"),
        ('CA', "CA"),
        ('CO', "CO"),
        ('CT', "CT"),
        ('DE', "DE"),
        ('FL', "FL"),
        ('GA', "GA"),
        ('HI', "HI"),
        ('ID', "ID"),
        ('IL', "IL"),
        ('IN', "IN"),
        ('IA', "IA"),
        ('KS', "KS"),
        ('KY', "KY"),
        ('LA', "LA"),
        ('ME', "ME"),
        ('MD', "MD"),
        ('MA', "MA"),
        ('MI', "MI"),
        ('MN', "MN"),
        ('MS', "MS"),
        ('MO', "MO"),
        ('MT', "MT"),
        ('NE', "NE"),
        ('NV', "NV"),
        ('NH', "NH"),
        ('NJ', "NJ"),
        ('NM', "NM"),
        ('NY', "NY"),
        ('NC', "NC"),
        ('ND', "ND"),
        ('OH', "OH"),
        ('OK', "OK"),
        ('OR', "OR"),
        ('PA', "PA"),
        ('RI', "RI"),
        ('SC', "SC"),
        ('SD', "SD"),
        ('TN', "TN"),
        ('TX', "TX"),
        ('UT', "UT"),
        ('VT', "VT"),
        ('VA', "VA"),
        ('WA', "WA"),
        ('WV', "WV"),
        ('WI', "WI"),
        ('WY', "WY")
    ]
    return states


class Doctor(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    Hospital = models.ForeignKey('records.Hospital', blank=False, default=None)

    def __str__(self):
        return self.User.first_name + " " + self.User.last_name


class Patient(models.Model):

    User = models.OneToOneField(User, on_delete=models.CASCADE)
    Phone_Number = models.CharField(validators=[
        RegexValidator(regex=r'^((\(\d{3}\) ?)|(\d{3}-))\d{3}-\d{4}$',
                       message="Phone number must be entered in the format: "
                               "'(111)222-3333 or 111-222-3333'")],
                                    blank=False, max_length=13)
    Street_Address = models.CharField(default='', max_length=50)
    City = models.CharField(default='', max_length=50)
    State = models.CharField(default='', max_length=50, choices=get_state_tuples())
    Zip_Code = models.CharField(default='', max_length=5)
    Date_of_Birth = models.DateField(default=timezone.now)
    Emergency_Contact_First_Name = models.CharField(default='', max_length=50, validators=[
        RegexValidator(regex=r'[a-zA-Z]+',
                       message="Names can only consist of letters")
    ])
    Emergency_Contact_Last_Name = models.CharField(default='', max_length=50, validators=[
        RegexValidator(regex=r'[a-zA-Z]+',
                       message="Names can only consist of letters")
    ])
    Emergency_Contact_Number = models.CharField(validators=[
        RegexValidator(regex=r'^((\(\d{3}\) ?)|(\d{3}-))\d{3}-\d{4}$',
                       message="Phone number must be entered in the format: "
                               "'(111)222-3333 or 111-222-3333'")],
                                    max_length=13, blank=True)
    Emergency_Patient = models.ForeignKey('Patient', blank=True, null=True)

    def __str__(self):
        return self.User.first_name + " " + self.User.last_name




class Nurse(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    Hospital = models.ForeignKey('records.Hospital', blank=False)

    def __str__(self):
        return self.User.first_name + " " + self.User.last_name


class Admin(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    Hospital = models.ForeignKey('records.Hospital', blank=False, default=None)

    def __str__(self):
        return self.User.first_name + " " + self.User.last_name

