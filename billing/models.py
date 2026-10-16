from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator
from django.core.exceptions import ValidationError
import uuid


def validate_omt_reference(value):
    """التحقق من صيغة رقم OMT المرجعي"""
    if not value:
        raise ValidationError('رقم OMT المرجعي مطلوب')
    clean = value.strip().upper().replace(' ', '')
    if len(clean) < 6:
        raise ValidationError('رقم OMT قصير جداً (6 أحرف على الأقل)')
    if not any(c.isdigit() for c in clean):
        raise ValidationError('رقم OMT يجب أن يحتوي على أرقام')
    if len(clean) > 50:
        raise ValidationError('رقم OMT طويل جداً')


def validate_phone(value):
    """التحقق من رقم الهاتف اللبناني"""
    if not value:
        raise ValidationError('رقم الهاتف مطلوب')
    clean = ''.join(c for c in value if c.isdigit() or c == '+')
    if len(clean) < 7:
        raise ValidationError('رقم الهاتف غير صحيح')


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'في انتظار الدفع'),
        ('submitted', 'تم إرسال الرقم المرجعي'),
        ('verified', 'تم التحقق'),
        ('rejected', 'مرفوض'),
    ]
    METHOD_CHOICES = [
        ('omt', 'OMT Pay'),
        ('whish', 'Whish Money'),
        ('cash', 'الدفع عند التسليم'),
        ('bank', 'تحويل بنكي'),
    ]

    reference_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    project_request = models.OneToOneField('requests_app.ProjectRequest', on_delete=models.CASCADE, related_name='payment', null=True, blank=True)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='omt')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    omt_reference = models.CharField(max_length=50, blank=True, validators=[validate_omt_reference])
    omt_phone = models.CharField(max_length=30, blank=True, validators=[validate_phone])
    notes = models.TextField(blank=True, max_length=500)
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'دفعة'
        verbose_name_plural = 'المدفوعات'

    def __str__(self):
        return f'{self.user} - ${self.amount}'

    def clean(self):
        super().clean()
        if self.status == 'submitted' and self.amount <= 0:
            raise ValidationError('لا يمكن إرسال دفعة بمبلغ 0')

    def can_be_submitted(self):
        """هل يمكن إرسال هذه الدفعة؟"""
        return (
            self.status == 'pending' and
            self.amount > 0 and
            not self.omt_reference
        )
