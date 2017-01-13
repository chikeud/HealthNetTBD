from django import forms
from .models import *
from accounts.utils import *

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['Sex', 'Weight', 'Height_Feet', 'Height_Inches', 'Current_Hospital', 'Insurance_ID']


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['Drug_Name', 'Drug_Strength', 'Dosage_Form', 'Quantity', 'Number_Of_Refills']


class TestForm(forms.ModelForm):
    Date = forms.DateField(widget=forms.SelectDateWidget(years=get_year_list()))
    class Meta:
        model = Test
        fields = ['Date','Test_Name', 'Notes', 'Released', 'Files']