from django import forms
from .models import AppointmentRequest


class AppointmentForm(forms.ModelForm):
    """Lead capture form - name, phone, email, preferred_date, message."""
    preferred_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Preferred date (optional)'
    )

    class Meta:
        model = AppointmentRequest
        fields = ['name', 'phone', 'email', 'preferred_date', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name',
                'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '10-digit mobile number',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email (optional)',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Any message or concern (optional)',
                'rows': 3,
            }),
        }
