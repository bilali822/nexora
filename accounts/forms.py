from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'اسم المستخدم',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'كلمة السر',
        })
    )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'you@email.com',
        })
    )
    first_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'الاسم الأول',
        })
    )
    phone = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '+961-XXXXXXXX',
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'اسم المستخدم',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'كلمة السر',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'تأكيد كلمة السر',
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        if commit:
            user.save()
            # حدّث الـ profile
            profile = user.profile
            profile.phone = self.cleaned_data.get('phone', '')
            profile.save()
        return user


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=False, label='الاسم الأول',
        widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(required=True, label='البريد الإلكتروني',
        widget=forms.EmailInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Profile
        fields = ['phone', 'company', 'bio', 'avatar']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'company': forms.TextInput(attrs={'class': 'form-input'}),
            'bio': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'avatar': forms.FileInput(attrs={'class': 'form-input'}),
        }
        labels = {
            'phone': 'رقم الهاتف',
            'company': 'الشركة',
            'bio': 'نبذة عنك',
            'avatar': 'الصورة الشخصية',
        }
