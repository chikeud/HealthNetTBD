from django import forms
from .models import *
from django.contrib.auth.models import User
from .utils import get_year_list


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']


class PatientForm(forms.ModelForm):
    Date_of_Birth = forms.DateField(widget=forms.SelectDateWidget(years=get_year_list()))

    class Meta:
        model = Patient
        fields = ['Phone_Number', 'Street_Address', 'City', 'State', 'Zip_Code', 'Date_of_Birth', 'Emergency_Contact_First_Name',
                  'Emergency_Contact_Last_Name', 'Emergency_Contact_Number']

# class NurseForm(forms.ModelForm):
#     class Meta:
#         model = Nurse
#         fields = ['Hospital']
#
# class AdminForm(forms.ModelForm):
#     class Meta:
#         model = Admin
#         fields = ['Hospital']
#
# class DoctorForm(forms.ModelForm):
#     class Meta:
#         model = Doctor
#         fields = ['Hospital']