from django.db import models
from django.contrib.auth.models import User


class GeneratedWebsite(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد التوليد'),
        ('completed', 'مكتمل'),
        ('failed', 'فشل'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generated_sites', null=True, blank=True)
    prompt = models.TextField(verbose_name='وصف الموقع')
    generated_code = models.TextField(blank=True, null=True, verbose_name='الكود المولّد')
    preview_url = models.URLField(blank=True, null=True, verbose_name='رابط المعاينة')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'موقع مولّد'
        verbose_name_plural = 'المواقع المولّدة'

    def __str__(self):
        return f'{self.user} - {self.prompt[:50]}'
