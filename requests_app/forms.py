from django import forms
from .models import ProjectRequest


class ProjectRequestForm(forms.ModelForm):
    class Meta:
        model = ProjectRequest
        fields = ['name', 'email', 'whatsapp', 'project_type', 'design_style',
                  'reference_url', 'features', 'budget', 'deadline', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-input'}),
            'project_type': forms.Select(attrs={'class': 'form-input'}),
            'design_style': forms.Select(attrs={'class': 'form-input'}),
            'reference_url': forms.URLInput(attrs={'class': 'form-input'}),
            'features': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'budget': forms.Select(attrs={'class': 'form-input'}),
            'deadline': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }
