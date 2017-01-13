from datetime import datetime
from .models import *


def get_year_list():
    year = datetime.today().year
    year_list = range(year, year - 125, -1)
    return year_list


def get_user_type(user):

    if Doctor.objects.filter(User__id=user.id):
        return "Doctor"
    elif Patient.objects.filter(User__id=user.id):
        return "Patient"
    elif Nurse.objects.filter(User__id=user.id):
        return "Nurse"
    elif Admin.objects.filter(User__id=user.id):
        return "Admin"
    else:
        return "None"

