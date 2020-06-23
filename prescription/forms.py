from django.forms import ModelForm, NumberInput
from .models import Patient, PatientDetail

# Patient Form
class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'gender', 'age']
        widgets = {
            'age': NumberInput(attrs={'min': 0}),
        }

# Patient Update Form
class PatientUpdateForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'gender', 'age']
        widgets = {
            'age': NumberInput(attrs={'min': 0}),
        }

# Patient Detail Form
class PatientDetailForm(ModelForm):
    class Meta:
        model = PatientDetail
        fields = ['patient', 'disease_identified', 'weight_in_kg', 'alcoholic', 'pregnant', 'breast_feeding',
        'liver_disease', 'eye_disease', 'kidney_disease', 'diabetes']
        widgets = {
            'weight_in_kg': NumberInput(attrs={'min': 0}),
        }

# Patient Detail Update Form
class PatientDetailUpdateForm(ModelForm):
    class Meta:
        model = PatientDetail
        fields = ['patient', 'disease_identified', 'weight_in_kg', 'alcoholic', 'pregnant', 'breast_feeding',
        'liver_disease', 'eye_disease', 'kidney_disease', 'diabetes', 'medicine']
        widgets = {
            'weight_in_kg': NumberInput(attrs={'min': 0}),
        }
