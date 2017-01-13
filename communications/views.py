from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from .forms import *
from django.contrib.auth.decorators import login_required
from accounts.utils import *
from .utils import *
from logger.utils import createActivity

def viewAppointments(request):
    context = RequestContext(request)
    user = request.user
    type = get_user_type(user)

    if type == "Doctor":
        profile = Doctor.objects.get(User__id=user.id)
        appointments = profile.Appointments.all()
    elif type == "Patient":
        profile = Patient.objects.get(User__id=user.id)
        appointments = profile.Appointments.all()
    elif type == "Nurse":
        profile = Nurse.objects.get(User__id=user.id)
        start_date, end_date = week_range(datetime.now())
        print(start_date)
        print(end_date)
        appointments = Appointment.objects.filter(Date__range=[start_date, end_date])
    else:
        return HttpResponseRedirect(reverse('accounts:home'))

    return render_to_response(
        'communications/view_appointments.html', {'appointments': appointments, 'type': type}, context)


def appointmentDetail(request, appointment_id):
    context = RequestContext(request)
    appointment = get_object_or_404(Appointment, id=int(appointment_id))

    return render_to_response(
        'communications/appointment_detail.html',
        {'appointment': appointment}, context)


@login_required()
def addAppointment(request):
    type = get_user_type(request.user)
    if type == "Patient":
        return addAppointmentPatient(request)
    elif type == "Doctor":
        return addAppointmentDoctor(request)
    elif type == "Nurse":
        return addAppointmentNurse(request)
    else:
        return HttpResponseRedirect(reverse('accounts:home'))


@login_required()
def addAppointmentPatient(request):
    context = RequestContext(request)
    type = get_user_type(request.user)
    if type != "Patient":
        return HttpResponseRedirect(reverse('accounts:home'))

    patient = Patient.objects.get(User__id=request.user.id)
    hospital = patient.Record.Current_Hospital
    doctor_qs = hospital.doctor_set

    appointment_form = AppointmentFormPatient(doctors=doctor_qs)
    if request.method == 'POST':
        appointment_form = AppointmentFormPatient(request.POST, doctors=doctor_qs)
        if appointment_form.is_valid():

            appointment = appointment_form.save(commit=False)
            appointment.Patient = patient
            appointment.Hospital = hospital

            doctor = appointment.Doctor
            doctors_appointments = doctor.Appointments.all()
            time = appointment.Time
            date = appointment.Date

            for appt in doctors_appointments:
                appt_time = appt.Time
                appt_date = appt.Date

                if date == appt_date:
                    if time == appt_time:
                        return render_to_response(
                            'communications/add_appointment.html',
                            {'type': type, 'appointment_form': appointment_form,
                             'error': "Doctor already has appointment at that time"}, context)
                    else:
                        pass
                else:
                    pass

            patient_appointments = patient.Appointments.all()

            for appt in patient_appointments:
                appt_time = appt.Time
                appt_date = appt.Date
                if date == appt_date:
                    if time == appt_time:
                        return render_to_response(
                            'communications/add_appointment.html',
                            {'type': type, 'appointment_form': appointment_form,
                             'error': "You already has appointment at that time"}, context)
                    else:
                        pass
                else:
                    pass

            appointment.save()

            createActivity(request.user,
                           type + " " + str(patient) + " created appointment with Doctor " + str(appointment.Doctor))

            return HttpResponseRedirect(reverse('communications:view_appointments'))

    return render_to_response(
        'communications/add_appointment.html', {'type': type, 'appointment_form': appointment_form, 'error': ""}, context)


@login_required()
def addAppointmentDoctor(request):
    context = RequestContext(request)
    type = get_user_type(request.user)
    if type != "Doctor":
        return HttpResponseRedirect(reverse('accounts:home'))

    doctor = Doctor.objects.get(User__id=request.user.id)

    appointment_form = AppointmentFormDoctor()
    if request.method == 'POST':
        appointment_form = AppointmentFormDoctor(request.POST)
        if appointment_form.is_valid():
            appointment = appointment_form.save(commit=False)
            appointment.Doctor = doctor
            appointment.Hospital = doctor.Hospital

            patient = appointment.Patient
            patient_appointments = patient.Appointments.all()
            time = appointment.Time
            date = appointment.Date

            for appt in patient_appointments:
                appt_time = appt.Time
                appt_date = appt.Date

                if date == appt_date:
                    if time == appt_time:
                        return render_to_response(
                            'communications/add_appointment.html',
                            {'type': type, 'appointment_form': appointment_form,
                             'error': "Patient already has appointment at that time"}, context)
                    else:
                        pass
                else:
                    pass

            doctor_appointments = doctor.Appointments.all()

            for appt in doctor_appointments:
                appt_time = appt.Time
                appt_date = appt.Date
                if date == appt_date:
                    if time == appt_time:
                        return render_to_response(
                            'communications/add_appointment.html',
                            {'type': type, 'appointment_form': appointment_form,
                             'error': "You already has appointment at that time"}, context)
                    else:
                        pass
                else:
                    pass

            appointment.save()

            createActivity(request.user,
                           type + " " + str(doctor) + " created appointment with Patient " + str(appointment.Patient))

            return HttpResponseRedirect(reverse('communications:view_appointments'))

    return render_to_response(
        'communications/add_appointment.html', {'appointment_form': appointment_form}, context)


@login_required()
def addAppointmentNurse(request):
    context = RequestContext(request)
    type = get_user_type(request.user)
    if type != "Nurse":
        return HttpResponseRedirect(reverse('accounts:home'))

    nurse = Nurse.objects.get(User__id=request.user.id)

    doctor_qs = Doctor.objects.filter(Hospital=nurse.Hospital)
    patient_qs = Patient.objects.filter(Record__Current_Hospital=nurse.Hospital)

    appointment_form = AppointmentFormNurse(doctors=doctor_qs, patients=patient_qs)
    if request.method == 'POST':
        appointment_form = AppointmentFormNurse(request.POST, doctors=doctor_qs, patients=patient_qs)
        if appointment_form.is_valid():
            appointment = appointment_form.save(commit=False)
            appointment.Hospital = nurse.Hospital

            doctor = appointment.Doctor
            doctors_appointments = doctor.Appointments.all()
            time = appointment.Time
            date = appointment.Date

            for appt in doctors_appointments:
                appt_time = appt.Time
                appt_date = appt.Date

                if date == appt_date:
                    if time == appt_time:
                        return render_to_response(
                            'communications/add_appointment.html',
                            {'type': type, 'appointment_form': appointment_form,
                             'error': "Doctor already has appointment at that time"}, context)
                    else:
                        pass
                else:
                    pass

            patient = appointment.Patient
            patient_appointments = patient.Appointments.all()

            for appt in patient_appointments:
                appt_time = appt.Time
                appt_date = appt.Date
                if date == appt_date:
                    if time == appt_time:
                        return render_to_response(
                            'communications/add_appointment.html',
                            {'type': type, 'appointment_form': appointment_form,
                             'error': "Patient already has appointment at that time"}, context)
                    else:
                        pass
                else:
                    pass

            appointment.save()

            createActivity(request.user,
                           type + " " + str(nurse) + " created appointment for Patient " + str(appointment.Patient)
                           + " with Doctor " + str(appointment.Doctor))

            return HttpResponseRedirect(reverse('communications:view_appointments'))

    return render_to_response(
        'communications/add_appointment.html', {'appointment_form': appointment_form}, context)


@login_required()
def editAppointment(request, appointment_id):
    type = get_user_type(request.user)
    if type == "Patient":
        return editAppointmentPatient(request, appointment_id)
    elif type == "Doctor":
        return editAppointmentDoctor(request, appointment_id)
    elif type == "Nurse":
        return editAppointmentNurse(request, appointment_id)
    else:
        return HttpResponseRedirect(reverse('accounts:home'))


@login_required()
def editAppointmentPatient(request, appointment_id):
    context = RequestContext(request)
    type = get_user_type(request.user)
    if type != "Patient":
        return HttpResponseRedirect(reverse('accounts:home'))

    patient = Patient.objects.get(User__id=request.user.id)
    hospital = patient.Record.Current_Hospital
    doctor_qs = hospital.doctor_set


    appointment = get_object_or_404(Appointment, id=int(appointment_id))
    appointment_form = AppointmentFormPatient(instance=appointment, doctors=doctor_qs)
    if request.method == 'POST':
        appointment_form = AppointmentFormPatient(request.POST, instance=appointment, doctors=doctor_qs)
        if appointment_form.is_valid():
            appointment = appointment_form.save(commit=False)
            appointment.save()

            createActivity(request.user, type + " " + str(patient) + " edited appointment")

            return HttpResponseRedirect(reverse('communications:view_appointments'))

    return render_to_response(
        'communications/edit_appointment.html', {'appointment_form': appointment_form, 'appt': appointment}, context)


@login_required()
def editAppointmentDoctor(request, appointment_id):
    context = RequestContext(request)
    type = get_user_type(request.user)
    if type != "Doctor":
        return HttpResponseRedirect(reverse('accounts:home'))

    doctor = Doctor.objects.get(User__id=request.user.id)
    hospital = Doctor.Hospital


    appointment = get_object_or_404(Appointment, id=int(appointment_id))
    appointment_form = AppointmentFormDoctor(instance=appointment)
    if request.method == 'POST':
        appointment_form = AppointmentFormDoctor(request.POST, instance=appointment)
        if appointment_form.is_valid():
            appointment = appointment_form.save(commit=False)
            appointment.save()

            createActivity(request.user, type + " " + str(doctor) + " edited appointment")

            return HttpResponseRedirect(reverse('communications:view_appointments'))

    return render_to_response(
        'communications/edit_appointment.html', {'appointment_form': appointment_form, 'appt': appointment}, context)


@login_required()
def editAppointmentNurse(request, appointment_id):
    context = RequestContext(request)
    type = get_user_type(request.user)
    if type != "Nurse":
        return HttpResponseRedirect(reverse('accounts:home'))

    nurse = Nurse.objects.get(User__id=request.user.id)
    hospital = Nurse.Hospital
    doctor_qs = Doctor.objects.filter(Hospital=nurse.Hospital)
    patient_qs = Patient.objects.filter(Record__Current_Hospital=nurse.Hospital)

    appointment = get_object_or_404(Appointment, id=int(appointment_id))
    appointment_form = AppointmentFormNurse(instance=appointment, doctors=doctor_qs, patients=patient_qs)
    if request.method == 'POST':
        appointment_form = AppointmentFormNurse(request.POST, instance=appointment, doctors=doctor_qs, patients=patient_qs)
        if appointment_form.is_valid():
            appointment = appointment_form.save(commit=False)
            appointment.save()

            createActivity(request.user, type + " " + str(nurse) + " edited appointment")

            return HttpResponseRedirect(reverse('communications:view_appointments'))

    return render_to_response(
        'communications/edit_appointment.html', {'appointment_form': appointment_form, 'appt': appointment},
        context)


@login_required()
def deleteAppointment(request, appointment_id):
    context = RequestContext(request)
    if request.method == "POST":
        return deleteAppt(request, appointment_id)
    return render_to_response(
        'communications/delete_confirmation.html', {'appt_id': appointment_id}, context)

@login_required()
def deleteAppt(request, appointment_id):
    type = get_user_type(request.user)

    if type == "Nurse" or type == "Admin":
        return HttpResponseRedirect(reverse('accounts:home'))

    appointment = get_object_or_404(Appointment, id=int(appointment_id))
    appointment.delete()

    createActivity(request.user,
                   type + " " + request.user.first_name + " " + request.user.last_name + " deleted appointment")

    return HttpResponseRedirect(reverse('communications:view_appointments'))


@login_required()
def sendMessage(request):
    type = get_user_type(request.user)
    context = RequestContext(request)
    message_form = MessageForm(users=User.objects.exclude(username=request.user.username))
    if request.method == 'POST':
        message_form = MessageForm(request.POST, users=User.objects.exclude(username=request.user.username))
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.Date = datetime.today()
            message.Sender = request.user
            message.save()

            createActivity(request.user,
                           str(request.user) + " sent a message to " + str(message.Receiver))

            return HttpResponseRedirect(reverse('accounts:home'))

    return render_to_response(
        'communications/send_message.html', {'type':type,'message_form': message_form}, context)


@login_required()
def viewMessages(request):
    context = RequestContext(request)
    messages = request.user.Receiver.all()
    type = get_user_type(request.user)

    new_messages = messages.filter(Viewed=False)
    viewed_messages = messages.filter(Viewed=True)

    return render_to_response(
        'communications/view_messages.html', {'type': type, 'new_messages': new_messages, 'viewed_messages': viewed_messages}, context)


@login_required()
def messageDetail(request, message_id):
    context = RequestContext(request)
    type = get_user_type(request.user)
    message = get_object_or_404(Message, id=int(message_id))
    message.Viewed = True
    message.save()
    return render_to_response(
        'communications/message_detail.html', {'message': message, 'type': type}, context)
