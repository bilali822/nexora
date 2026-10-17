from django.db import models
from django.contrib.auth.models import User


class GeneratedWebsite(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد التوليد'),
        ('completed', 'مكتمل'),
        ('failed', 'فشل'),
        ('published', 'منشور'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generated_sites', null=True, blank=True)
    prompt = models.TextField(verbose_name='وصف الموقع')
    
    # Theme
    theme_color = models.CharField(max_length=20, default='#EA580C')
    theme_font = models.CharField(max_length=50, default='Tajawal')
    theme_style = models.CharField(max_length=50, default='modern')
    
    # Content
    generated_code = models.TextField(blank=True, null=True, verbose_name='الكود المولّد (JSON للصفحات)')
    
    # Deployment
    github_repo_url = models.URLField(blank=True, null=True)
    published_url = models.URLField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    competitor_url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'موقع مولّد'
        verbose_name_plural = 'المواقع المولّدة'

    def __str__(self):
        return f'{self.user} - {self.prompt[:50]}'


class SiteVersion(models.Model):
    """نسخة محفوظة من الموقع المولد (History / Rollback)"""
    site = models.ForeignKey(GeneratedWebsite, on_delete=models.CASCADE, related_name='versions')
    code_snapshot = models.TextField()
    instruction_applied = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'نسخة موقع'
        verbose_name_plural = 'نسخ المواقع'

    def __str__(self):
        return f'Version {self.id} of Site {self.site.id}'
