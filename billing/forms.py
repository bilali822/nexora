from django import forms
from .models import Payment


class OMTConfirmForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['omt_reference', 'omt_phone', 'notes']
        widgets = {
            'omt_reference': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'OMT-123456789'}),
            'omt_phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+961-XXXXXXXX'}),
            'notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }
        labels = {
            'omt_reference': 'رقم OMT Pay المرجعي',
            'omt_phone': 'رقم الهاتف',
            'notes': 'ملاحظات',
        }
