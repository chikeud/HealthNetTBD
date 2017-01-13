from django import forms
from .models import *
from django.contrib.auth.models import User
from accounts.models import*
from .utils import get_short_year_list
from HealthNet.settings import TIME_INPUT_FORMATS
from datetime import date
from django.forms.utils import ErrorList


class AppointmentFormPatient(forms.ModelForm):

    Doctor = forms.ModelChoiceField(queryset=Doctor.objects.none(), required = True,
                                    widget=forms.Select(attrs={'class':'selectpicker show-tick form-control', 'required': ''}), empty_label="[Doctor]")
    Date = forms.DateField(widget=forms.SelectDateWidget(years=get_short_year_list()))
    Time = forms.TimeField(input_formats=TIME_INPUT_FORMATS, error_messages={'invalid': "Time must be in HH:MM AM/PM format"})


    class Meta:
        model = Appointment
        fields = ['Doctor', 'Date', 'Time', 'Purpose']


    def __init__(self, *args, **kwargs):
        qs = kwargs.pop('doctors')
        super(AppointmentFormPatient, self).__init__(*args, **kwargs)
        self.fields['Doctor'].queryset = qs

    def is_valid(self):
        if super(AppointmentFormPatient, self).is_valid():
            d = self.cleaned_data['Date']
            if d < date.today():
                errors = self._errors.setdefault("Date", ErrorList())
                errors.append(u"Date cant be in the past")
                return False
            else:
                return True
        else:
            return False

class AppointmentFormDoctor(forms.ModelForm):

    Patient = forms.ModelChoiceField(queryset=Patient.objects.all(), required = True,
                                     widget=forms.Select(attrs={'class':'selectpicker show-tick form-control', 'required': ''}), empty_label="[Patient]")
    Date = forms.DateField(widget=forms.SelectDateWidget(years=get_short_year_list()))
    Time = forms.TimeField(input_formats=TIME_INPUT_FORMATS,
                           error_messages={'invalid': "Time must be in HH:MM AM/PM format"})
    class Meta:
        model = Appointment
        fields = ['Patient', 'Date', 'Time', 'Purpose']

    def is_valid(self):
        if super(AppointmentFormDoctor, self).is_valid():
            d = self.cleaned_data['Date']
            if d < date.today():
                errors = self._errors.setdefault("Date", ErrorList())
                errors.append(u"Date cant be in the past")
                return False
            else:
                return True
        else:
            return False

class AppointmentFormNurse(forms.ModelForm):

    Patient = forms.ModelChoiceField(queryset=Patient.objects.none(), required = True,
                                     widget=forms.Select(attrs={'class':'selectpicker show-tick form-control', 'required': ''}), empty_label="[Patient]")
    Doctor = forms.ModelChoiceField(queryset=Doctor.objects.none(), required=True,
                                    widget=forms.Select(
                                        attrs={'class': 'selectpicker show-tick form-control', 'required': ''}),
                                    empty_label="[Doctor]")
    Date = forms.DateField(widget=forms.SelectDateWidget(years=get_short_year_list()))
    Time = forms.TimeField(input_formats=TIME_INPUT_FORMATS,
                           error_messages={'invalid': "Time must be in HH:MM AM/PM format"})

    class Meta:
        model = Appointment
        fields = ['Patient', 'Doctor', 'Date', 'Time', 'Purpose']

    def __init__(self, *args, **kwargs):
        doctor_qs = kwargs.pop('doctors')
        patient_qs = kwargs.pop('patients')
        super(AppointmentFormNurse, self).__init__(*args, **kwargs)
        self.fields['Doctor'].queryset = doctor_qs
        self.fields['Patient'].queryset = patient_qs

    def is_valid(self):
        if super(AppointmentFormNurse, self).is_valid():
            d = self.cleaned_data['Date']
            if d < date.today():
                errors = self._errors.setdefault("Date", ErrorList())
                errors.append(u"Date cant be in the past")
                return False
            else:
                return True
        else:
            return False


class MessageForm(forms.ModelForm):
    Receiver = forms.ModelChoiceField(queryset=User.objects.none(), required=True,
                                    widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control', 'required': ''}), empty_label="[User]")

    class Meta:
        model = Message
        fields = ['Receiver', 'Subject', 'Text']

    def __init__(self, *args, **kwargs):
        user_qs = kwargs.pop('users')
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['Receiver'].queryset = user_qs