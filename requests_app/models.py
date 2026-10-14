from simple_history.models import HistoricalRecords
from django.db import models
import uuid


class ProjectRequest(models.Model):
    PROJECT_TYPE = [
        ('website', 'موقع تعريفي'), ('webapp', 'تطبيق ويب'),
        ('store', 'متجر إلكتروني'), ('dashboard', 'لوحة تحكم'),
        ('ui', 'تصميم UI/UX'), ('other', 'أخرى'),
    ]
    DESIGN_STYLE = [
        ('minimal', 'بسيط'), ('modern', 'عصري'), ('luxury', 'فخم'),
        ('dark', 'داكن'), ('colorful', 'ملوّن'), ('creative', 'إبداعي'),
    ]
    BUDGET = [
        ('<500', 'أقل من 500$'), ('500-1000', '500 - 1000$'),
        ('1000-3000', '1000 - 3000$'), ('>3000', 'أكثر من 3000$'),
        ('unknown', 'غير محدد'),
    ]
    STATUS = [
        ('new', 'جديد'), ('review', 'قيد المراجعة'),
        ('contacted', 'تم التواصل'), ('accepted', 'مقبول'),
        ('rejected', 'مرفوض'), ('done', 'مكتمل'),
    ]

    tracking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=30)
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPE)
    design_style = models.CharField(max_length=20, choices=DESIGN_STYLE)
    reference_url = models.URLField(blank=True)
    features = models.TextField()
    budget = models.CharField(max_length=20, choices=BUDGET)
    deadline = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='new')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "طلب مشروع"
        verbose_name_plural = "طلبات المشاريع"
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.get_project_type_display()}'
    history = HistoricalRecords()


class ProjectAttachment(models.Model):
    request = models.ForeignKey(ProjectRequest, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = "مرفق"
        verbose_name_plural = "المرفقات"

    def __str__(self):
        return self.file.name


class PriceCalculator(models.Model):
    """حاسبة السعر - تُستخدم بالأدمن فقط لضبط المعايير"""
    key = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "معيار سعر"
        verbose_name_plural = "حاسبة الأسعار"
        ordering = ['order']

    def __str__(self):
        return f'{self.label} - ${self.price}'
