from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'اسمك'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'you@email.com'}),
            'subject': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'الموضوع'}),
            'message': forms.Textarea(attrs={'class': 'form-input', 'rows': 5, 'placeholder': 'رسالتك...'}),
        }
