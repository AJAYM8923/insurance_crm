from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['agent']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'age': forms.NumberInput(attrs={
                'readonly': 'readonly',
                'style': 'background-color: #e9ecef;',  # Optional styling
            }),
        }
