from django import forms
from .models import GeneratedWebsite

class WebsitePromptForm(forms.ModelForm):
    class Meta:
        model = GeneratedWebsite
        fields = ['prompt', 'competitor_url', 'theme_color', 'theme_font', 'theme_style']
        widgets = {
            'prompt': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'صف الموقع الذي تريده... مثال: موقع لمطعم إيطالي بألوان دافئة وقائمة طعام تفاعلية'}),
            'competitor_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://example.com (اختياري)'}),
            'theme_color': forms.TextInput(attrs={'class': 'form-input', 'type': 'color'}),
            'theme_font': forms.Select(attrs={'class': 'form-input'}, choices=[('Tajawal', 'Tajawal'), ('Cairo', 'Cairo'), ('Inter', 'Inter'), ('Almarai', 'Almarai')]),
            'theme_style': forms.Select(attrs={'class': 'form-input'}, choices=[('modern', 'Modern'), ('minimal', 'Minimal'), ('dark', 'Dark'), ('cyberpunk', 'Cyberpunk')]),
        }

class EditWithAIForm(forms.Form):
    instruction = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'مثال: خلي الهيدر أزرق وزر الشراء أكبر...'}))

class GitHubDeployForm(forms.Form):
    github_token = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'GitHub Personal Access Token (repo scope)'}))
    repo_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'my-new-website'}))
