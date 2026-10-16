from django import forms
from django.core.exceptions import ValidationError
from .models import Payment


class OMTConfirmForm(forms.ModelForm):
    omt_reference = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'مثال: OMT123456789',
            'minlength': 6,
            'maxlength': 50,
            'pattern': '[A-Za-z0-9\\-]{6,50}',
            'autocomplete': 'off',
            'required': True,
        }),
        help_text='رقم من 6-50 حرف (أحرف وأرقام فقط)',
    )
    omt_phone = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '+961 81 234 567',
            'pattern': '[0-9+\\s\\-]{7,30}',
            'autocomplete': 'tel',
            'required': True,
        }),
        help_text='الرقم اللي حوّلت منه',
    )
    notes = forms.CharField(
        required=False,
        max_length=500,
        widget=forms.Textarea(attrs={
            'class': 'form-input',
            'rows': 3,
            'placeholder': 'ملاحظات إضافية (اختياري)',
            'maxlength': 500,
        }),
    )

    class Meta:
        model = Payment
        fields = ['omt_reference', 'omt_phone', 'notes']

    def clean_omt_reference(self):
        ref = self.cleaned_data.get('omt_reference', '').strip().upper()
        # شيل المسافات
        ref = ref.replace(' ', '')
        if len(ref) < 6:
            raise ValidationError('رقم OMT قصير جداً — 6 أحرف على الأقل')
        if len(ref) > 50:
            raise ValidationError('رقم OMT طويل جداً')
        if not any(c.isdigit() for c in ref):
            raise ValidationError('رقم OMT يجب أن يحتوي على أرقام')
        # تحقق من عدم التكرار
        if Payment.objects.filter(omt_reference=ref).exclude(pk=self.instance.pk).exists():
            raise ValidationError('رقم OMT مستخدم مسبقاً')
        return ref

    def clean_omt_phone(self):
        phone = self.cleaned_data.get('omt_phone', '').strip()
        # شيل المسافات والشرطات
        clean = ''.join(c for c in phone if c.isdigit() or c == '+')
        if len(clean) < 7:
            raise ValidationError('رقم الهاتف قصير جداً')
        if len(clean) > 15:
            raise ValidationError('رقم الهاتف طويل جداً')
        return phone
