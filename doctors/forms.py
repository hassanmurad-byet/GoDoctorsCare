from django import forms
from patients.models import Appointment, Consultation, Medication
from django import forms
from patients.models import Appointment, Consultation, Medication
from django.forms import inlineformset_factory

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['diagnosis', 'prescription_notes', 'follow_up_date']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'prescription_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'follow_up_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'diagnosis': 'Diagnosis',
            'prescription_notes': 'Prescription Notes',
            'follow_up_date': 'Follow-Up Date'
        }

MedicationFormSet = inlineformset_factory(
    Consultation,
    Medication,
    fields=('name', 'dosage', 'frequency', 'duration', 'instructions'),
    extra=1,
    can_delete=True,
    widgets={
        'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Paracetamol'}),
        'dosage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 500mg'}),
        'frequency': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2 times/day'}),
        'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 5 days'}),
        'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Take after food'}),
    },
    labels={
        'name': 'Medicine Name',
        'dosage': 'Dosage',
        'frequency': 'Frequency',
        'duration': 'Duration',
        'instructions': 'Instructions',
    }
)
