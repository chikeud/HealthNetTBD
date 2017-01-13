from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from .forms import*
from records.forms import RecordForm
from .utils import *
from django.contrib.auth.decorators import login_required
from logger.utils import createActivity


def home(request):
    user = request.user
    if user.is_authenticated():
        if user.is_active:
            return HttpResponseRedirect(reverse('accounts:profile'))
        else:
            return HttpResponse("Your account is disabled.")
    return render(request, 'accounts/home.html')


def register(request):
    return render(request, 'accounts/register.html')


def message(request):
    context = RequestContext(request)
    user = request.user
    type = get_user_type(user)
    return render_to_response(
        'accounts/message.html',
        {'type': type}, context)


def registerPatient(request):
    context = RequestContext(request)

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        patient_form = PatientForm(data=request.POST)
        record_form = RecordForm(data=request.POST)
        if user_form.is_valid() and patient_form.is_valid() and record_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            patient = patient_form.save(commit=False)
            patient.User = user
            emergency_patient = Patient.objects.filter(
                User__first_name=patient.Emergency_Contact_First_Name
            ).filter(
                User__last_name=patient.Emergency_Contact_Last_Name
            )
            if emergency_patient:
                emergency_patient = emergency_patient[0]
                patient.Emergency_Patient = emergency_patient
                patient.Emergency_Contact_Number = emergency_patient.Phone_Number
            else:
                patient.Emergency_Patient = None
            patient.save()

            record = record_form.save(commit=False)
            record.Patient_Profile = patient
            record.Admitted = False
            record.Time_Of_Admission = None
            record.Time_Of_Discharge = None
            record.save()

            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)

            createActivity(user, "New Patient " + str(patient) + " registered")


            return HttpResponseRedirect(reverse('accounts:home'))
    else:
        user_form = UserForm()
        patient_form = PatientForm()
        record_form = RecordForm()
    return render_to_response(
            'accounts/patient_register.html',
            {'user_form': user_form, 'patient_form': patient_form, 'record_form': record_form},
            context)


def updateInfo(request):
    type = get_user_type(request.user)
    if type == "Patient":
        return update_patient(request)
    else:
        return updateEmployee(request)


@login_required()
def update_patient(request):
    context = RequestContext(request)
    user = request.user
    type = get_user_type(user)
    context = RequestContext(request)
    user = request.user
    patient = Patient.objects.get(User__id=user.id)
    user_form = UserForm(instance=user)
    patient_form = PatientForm(instance=patient)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        patient_form = PatientForm(request.POST, instance=patient)
        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            patient = patient_form.save(commit=False)
            patient.User = user
            emergency_patient = Patient.objects.filter(
                User__first_name=patient.Emergency_Contact_First_Name
            ).filter(
                User__last_name=patient.Emergency_Contact_Last_Name
            )
            if emergency_patient:
                emergency_patient = emergency_patient[0]
                patient.Emergency_Patient = emergency_patient
                patient.Emergency_Contact_Number = emergency_patient.Phone_Number

            patient = patient_form.save(commit=False)
            patient.save()

            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)

            createActivity(user, "Patient " + str(patient) + " updated profile information")


            return HttpResponseRedirect(reverse('accounts:home'))
    return render_to_response(
        'accounts/update.html',
        {'type':type, 'user_form': user_form, 'profile_form': patient_form}, context)


@login_required()
def updateEmployee(request):
    context = RequestContext(request)
    user = request.user
    type = get_user_type(user)
    if type == "Patient":
        return HttpResponseRedirect(reverse('accounts:home'))

    user_form = UserForm(instance=user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            first_name = user.first_name
            last_name = user.last_name
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)



            createActivity(user, type + " " + first_name + " " + last_name + " updated profile information" )

            return HttpResponseRedirect(reverse('accounts:home'))

    return render_to_response(
        'accounts/update.html',
        {'user_form': user_form,
         'type':type}, context)


@login_required()
def registerEmploylee(request, employee_type):
    type = get_user_type(request.user)

    if type != "Admin":
        return HttpResponseRedirect(reverse('accounts:home'))
    context = RequestContext(request)
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        admin = get_object_or_404(Admin, User_id=request.user.id)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            if employee_type == '0':  # Doctor
                employee = Doctor(User=user, Hospital=admin.Hospital)
                employee.save()
                type = "Doctor"
            elif employee_type == '1':  # Nurse
                employee = Nurse(User=user, Hospital=admin.Hospital)
                employee.save()
                type = "Nurse"
            elif employee_type == '2':  # Admin
                employee = Admin(User=user, Hospital=admin.Hospital)
                employee.save()
                type = "Admin"
            else:  # None, raise an error
                return HttpResponseRedirect(reverse('accounts:home'))

            registered = True
            employee.save()

            createActivity(request.user, "New " + type + " registered")
    else:
        user_form = UserForm()

        if employee_type == '0':  # Doctor
            type = "Doctor"
        elif employee_type == '1':  # Nurse
            type = "Nurse"
        elif employee_type == '2':  # Admin
            type = "Admin"
        else:  # None, raise an error
            return HttpResponseRedirect(reverse('accounts:home'))

    return render_to_response(
        'accounts/employee_register.html',
        {'user_form': user_form, 'registered': registered, 'type': type, 'employee_type': employee_type},
        context)


@login_required()
def profile(request):
    type = get_user_type(request.user)
    if type == "Doctor":
        return render(request, 'accounts/doctor_profile.html')
    elif type == "Patient":
        return render(request, 'accounts/patient_profile.html')
    elif type == "Nurse":
        return render(request, 'accounts/nurse_profile.html')
    else:
        return render(request, 'accounts/admin_profile.html')


@login_required()
def searchPatient(request):

    type = get_user_type(request.user)
    if type == "Patient":
        return HttpResponseRedirect(reverse('accounts:home'))

    context = RequestContext(request)
    results = []
    error = ''
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        if first_name and last_name:
            results = Patient.objects.filter(User__first_name__icontains=first_name).filter(User__last_name__icontains=last_name)
        elif first_name:

            results = Patient.objects.filter(User__first_name__icontains=first_name)
        elif last_name:

            results = Patient.objects.filter(User__last_name__icontains=last_name)
        else:
            error = "At least one field is required"

        if type == "Nurse":
            nurse = Nurse.objects.get(User__id=request.user.id)
            results = results.filter(Record__Current_Hospital=nurse.Hospital)


    return render_to_response(
        'accounts/search_patient.html', {'results': results, 'error': error}, context)


def loginUser(request):

    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)

                createActivity(user, str(user) + " logged in")

                return HttpResponseRedirect(reverse('accounts:home'))
            else:
                return HttpResponse("Your account is disabled!")
        else:

            return render_to_response('accounts/login.html', {'error': "Invalid credentials"}, context)
    else:
        return render_to_response(
            'accounts/login.html', context)


def logoutUser(request):
    user = request.user
    logout(request)
    createActivity(user, str(user) + " logged out")
    return HttpResponseRedirect(reverse('accounts:home'))
