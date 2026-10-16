from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


INPUT = {'class': 'form-input'}


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={**INPUT, 'placeholder': 'you@email.com', 'autocomplete': 'email'})
    )
    first_name = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={**INPUT, 'placeholder': 'الاسم الأول', 'autocomplete': 'given-name'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            **INPUT, 'placeholder': 'اسم المستخدم', 'autocomplete': 'username'
        })
        self.fields['password1'].widget.attrs.update({
            **INPUT, 'placeholder': 'كلمة السر', 'autocomplete': 'new-password'
        })
        self.fields['password2'].widget.attrs.update({
            **INPUT, 'placeholder': 'تأكيد كلمة السر', 'autocomplete': 'new-password'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            **INPUT, 'placeholder': 'اسم المستخدم', 'autofocus': True,
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            **INPUT, 'placeholder': 'كلمة السر',
            'autocomplete': 'current-password'
        })
    )


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=100, required=False, label='الاسم الأول',
        widget=forms.TextInput(attrs={**INPUT, 'autocomplete': 'given-name'})
    )
    email = forms.EmailField(
        required=True, label='البريد الإلكتروني',
        widget=forms.EmailInput(attrs={**INPUT, 'autocomplete': 'email'})
    )

    class Meta:
        model = Profile
        fields = ['company', 'bio', 'avatar']
        widgets = {
            'company': forms.TextInput(attrs={**INPUT, 'placeholder': 'اسم الشركة (اختياري)'}),
            'bio': forms.Textarea(attrs={**INPUT, 'rows': 4, 'placeholder': 'نبذة قصيرة عنك...'}),
            'avatar': forms.FileInput(attrs={**INPUT}),
        }
        labels = {
            'company': 'الشركة',
            'bio': 'نبذة عنك',
            'avatar': 'الصورة الشخصية',
        }
