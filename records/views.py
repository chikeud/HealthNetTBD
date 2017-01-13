from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from .forms import*
from records.forms import RecordForm
from django.contrib.auth.decorators import login_required
from accounts.utils import *
from logger.utils import createActivity



@login_required()
def viewPatientRecord(request, user_id):
    context = RequestContext(request)
    type = get_user_type(request.user)
    if request.user.id != int(user_id):
        if type == "Nurse":
            nurse = Nurse.objects.get(User__id=request.user.id)

            user = get_object_or_404(User, id= int(user_id))
            patient = Patient.objects.get(User__id=user.id)

            if patient.Record.Current_Hospital != nurse.Hospital:
                return HttpResponseRedirect(reverse('accounts:home'))
        elif type == "Doctor":
            pass
        else:
            return HttpResponseRedirect(reverse('accounts:home'))

    user = get_object_or_404(User, id=int(user_id))
    patient = Patient.objects.get(User__id=user.id)
    record = patient.Record
    prescriptions = record.Prescriptions.all()
    tests = record.Tests.all()

    return render_to_response(
        'records/patient_detail.html',
        {'record': record, 'prescriptions': prescriptions, 'tests': tests, 'type': type},
        context)


@login_required()
def updateRecord(request, record_id):
    context = RequestContext(request)
    record = get_object_or_404(Record, id=int(record_id))
    record_form = RecordForm(instance=record)
    if request.method == 'POST':
        record_form = RecordForm(request.POST, instance=record)
        if record_form.is_valid():
            record = record_form.save(commit=False)
            record.save()

            type = get_user_type(request.user)

            createActivity(request.user,
                           type + " " + request.user.first_name + " " + request.user.last_name + " updated Patient "
                           + str(record.Patient_Profile) + "'s Record")

            return HttpResponseRedirect(reverse('records:view_patient_record',
                                                kwargs={'user_id': record.Patient_Profile.User.id}))

    return render_to_response(
        'records/update_record.html', {'record_form': record_form, 'record': record}, context)


@login_required()
def addPrescription(request, record_id):

    type = get_user_type(request.user)
    if type != "Doctor":
        return HttpResponseRedirect(reverse('accounts:home'))

    context = RequestContext(request)
    rx_form = PrescriptionForm()
    record = get_object_or_404(Record, id=int(record_id))
    if request.method == 'POST':
        rx_form = PrescriptionForm(data=request.POST)
        if rx_form.is_valid():
            prescription = rx_form.save(commit=False)
            prescription.Patient_Record = record
            prescription.Doctor = Doctor.objects.get(User__id=request.user.id)
            prescription.Date_Of_Issue = datetime.now()
            prescription.save()

            createActivity(request.user,
                           type + " " + str(prescription.Doctor) + " added a prescription for Patient "
                           + str(prescription.Patient_Record.Patient_Profile))

            return HttpResponseRedirect(reverse('records:view_patient_record',
                                                kwargs={'user_id': record.Patient_Profile.User.id}))

    return render_to_response(
        'records/add_prescription.html', {'rx_form': rx_form, 'record': record}, context)


@login_required()
def prescriptionDetail(request, rx_id):
    context = RequestContext(request)
    prescription = get_object_or_404(Prescription, id=int(rx_id))

    type = get_user_type(request.user)

    if type == "Patient":
        if request.user.id != prescription.Patient_Record.Patient_Profile.User.id:
            return HttpResponseRedirect(reverse('accounts:home'))

    return render_to_response(
        'records/prescription_detail.html',
        {'prescription': prescription, 'type': type},
        context)


@login_required()
def editPrescription(request, rx_id):

    type = get_user_type(request.user)
    if type != "Doctor":
        return HttpResponseRedirect(reverse('accounts:home'))

    context = RequestContext(request)
    prescription = get_object_or_404(Prescription, id=int(rx_id))
    rx_form = PrescriptionForm(instance=prescription)
    if request.method == 'POST':
        rx_form = PrescriptionForm(request.POST, instance=prescription)
        if rx_form.is_valid():
            prescription = rx_form.save(commit=False)
            prescription.save()

            createActivity(request.user,
                           type + " " + str(prescription.Doctor) + " edited a prescription for Patient "
                           + str(prescription.Patient_Record.Patient_Profile))

            return HttpResponseRedirect(reverse('records:prescription_detail',
                                                kwargs={'rx_id': prescription.id}))
    return render_to_response(
        'records/edit_prescription.html', {'rx_form': rx_form, 'prescription': prescription}, context)


@login_required()
def removePrescription(request, rx_id):
    type = get_user_type(request.user)

    if type != "Doctor":
        return HttpResponseRedirect(reverse('accounts:home'))

    prescription = get_object_or_404(Prescription, id=int(rx_id))
    user_id = prescription.Patient_Record.Patient_Profile.User.id

    createActivity(request.user,
                   type + " " + str(prescription.Doctor) + " removed a prescription for Patient "
                   + str(prescription.Patient_Record.Patient_Profile))

    prescription.delete()
    return HttpResponseRedirect(reverse('records:view_patient_record', kwargs={'user_id': user_id}))


@login_required()
def addTest(request, record_id):
    type = get_user_type(request.user)
    if type != "Doctor":
        return HttpResponseRedirect(reverse('accounts:home'))

    context = RequestContext(request)
    test_form = TestForm()
    record = get_object_or_404(Record, id=int(record_id))
    if request.method == 'POST':
        test_form = TestForm(data=request.POST, files=request.FILES)
        if test_form.is_valid():
            test = test_form.save(commit=False)
            test.Patient_Record = record
            test.Doctor = Doctor.objects.get(User__id=request.user.id)
            test.save()

            createActivity(request.user,
                           type + " " + str(test.Doctor) + " added a test for Patient "
                           + str(test.Patient_Record.Patient_Profile))

            return HttpResponseRedirect(reverse('records:view_patient_record',
                                                kwargs={'user_id': record.Patient_Profile.User.id}))

    return render_to_response(
        'records/add_test.html', {'test_form': test_form, 'record': record}, context)


@login_required()
def testDetail(request, test_id):
    context = RequestContext(request)
    test = get_object_or_404(Test, id=int(test_id))

    type = get_user_type(request.user)

    if type == "Patient":
        if request.user.id != test.Patient_Record.Patient_Profile.User.id:
            return HttpResponseRedirect(reverse('accounts:home'))

    return render_to_response(
        'records/test_detail.html',
        {'test': test, 'type': type},
        context)


@login_required()
def editTest(request, test_id):
    type = get_user_type(request.user)
    if type != "Doctor":
        return HttpResponseRedirect(reverse('accounts:home'))

    context = RequestContext(request)
    test = get_object_or_404(Test, id=int(test_id))
    test_form = TestForm(instance=test)
    if request.method == 'POST':
        test_form = TestForm(request.POST, instance=test, files=request.FILES)
        if test_form.is_valid():
            test = test_form.save(commit=False)
            test.save()

            createActivity(request.user,
                           type + " " + str(test.Doctor) + " edited a test for Patient "
                           + str(test.Patient_Record.Patient_Profile))

            return HttpResponseRedirect(reverse('records:test_detail',
                                                kwargs={'test_id': test.id}))
    return render_to_response(
        'records/edit_test.html', {'test_form': test_form, 'test': test}, context)


@login_required()
def removeTest(request, test_id):
    type = get_user_type(request.user)

    if type != "Doctor":
        return HttpResponseRedirect(reverse('accounts:home'))

    test = get_object_or_404(Test, id=int(test_id))
    user_id = test.Patient_Record.Patient_Profile.User.id

    createActivity(request.user,
                   type + " " + str(test.Doctor) + " deleted a test for Patient "
                   + str(test.Patient_Record.Patient_Profile))

    test.delete()
    return HttpResponseRedirect(reverse('records:view_patient_record', kwargs={'user_id': user_id}))


@login_required()
def admitPatient(request, record_id):

    type = get_user_type(request.user)
    if type == "Admin" or type == "Patient":
        return HttpResponseRedirect(reverse('accounts:home'))

    record = get_object_or_404(Record, id=int(record_id))

    if type == "Doctor":
        employee = Doctor.objects.get(User__id=request.user.id)
    else:
        employee = Nurse.objects.get(User__id=request.user.id)

    hospital = employee.Hospital
    record.Current_Hospital = hospital
    record.Admitted = True
    record.Time_Of_Admission = datetime.now()
    record.save()

    hospital.Number_Of_Patients += 1
    hospital.save()

    createActivity(request.user,
                   type + " " + str(employee) + " addmited Patient " +
                   str(record.Patient_Profile) + " to " + str(hospital))

    return HttpResponseRedirect(reverse('records:view_patient_record',
                                        kwargs={'user_id': record.Patient_Profile.User.id}))

def dischargePatient(request, record_id):

    type = get_user_type(request.user)
    if type != "Doctor":
        return HttpResponseRedirect(reverse('accounts:home'))

    record = get_object_or_404(Record, id=int(record_id))

    doctor = Doctor.objects.get(User__id=request.user.id)

    hospital = doctor.Hospital
    record.Admitted = False
    record.Time_Of_Discharge = datetime.now()
    record.save()

    hospital.Number_Of_Patients -= 1
    hospital.save()

    createActivity(request.user,
                   type + " " + str(doctor) + " discharged Patient " +
                   str(record.Patient_Profile) + " from " + str(hospital))

    return HttpResponseRedirect(reverse('records:view_patient_record',
                                        kwargs={'user_id': record.Patient_Profile.User.id}))

@login_required()
def exportInformation(request):
    context = RequestContext(request)

    type = get_user_type(request.user)
    if type != "Patient":
        return HttpResponseRedirect(reverse('accounts:home'))

    patient = get_object_or_404(Patient, User__id=request.user.id)

    create_csv(patient)

    return HttpResponseRedirect(reverse('accounts:home'))


