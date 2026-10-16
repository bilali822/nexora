from django import forms


class WebsitePromptForm(forms.Form):
    prompt = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-input',
            'rows': 5,
            'placeholder': 'صف الموقع الذي تريده... مثال: موقع لمطعم إيطالي بألوان دافئة وقائمة طعام تفاعلية',
        }),
        label='وصف الموقع',
        required=True,
        max_length=1000,
    )
