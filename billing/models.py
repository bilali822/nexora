from django.db import models
from django.contrib.auth.models import User
import uuid


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
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    omt_reference = models.CharField(max_length=50, blank=True)
    omt_phone = models.CharField(max_length=30, blank=True)
    notes = models.TextField(blank=True)
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'دفعة'
        verbose_name_plural = 'المدفوعات'

    def __str__(self):
        return f'{self.user} - ${self.amount}'
