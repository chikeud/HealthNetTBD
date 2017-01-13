from .models import *
from datetime import datetime
from accounts.models import *
from accounts.utils import *

def createActivity(user, entry):

    type = get_user_type(user)
    if type == "Patient":
        patient = Patient.objects.get(User_id=user.id)
        hospital = patient.Record.Current_Hospital
    elif type == "Doctor":
        doctor = Doctor.objects.get(User_id=user.id)
        hospital = doctor.Hospital
    elif type == "Nurse":
        nurse = Nurse.objects.get(User_id=user.id)
        hospital = nurse.Hospital
    else:
        admin = Admin.objects.get(User_id=user.id)
        hospital = admin.Hospital


    date = datetime.today()
    log = DailyLog.objects.filter(Hospital=hospital)
    log = log.filter(Date=date)

    if not log:
        log = DailyLog(Date=date, Hospital=hospital)
        log.save()
    else:
        log = log[0]

    activity = Activity(Log=log, User=user, Date=datetime.now(),Entry=entry)
    activity.save()
    return


