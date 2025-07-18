# forms.py
from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['agent']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }
