from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    company = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True, max_length=500)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'ملف شخصي'
        verbose_name_plural = 'الملفات الشخصية'

    def __str__(self):
        return f'ملف {self.user.username}'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


class OTPCode(models.Model):
    """رمز تحقق مؤقت"""
    PURPOSE_CHOICES = [
        ('signup', 'تسجيل حساب'),
        ('login', 'تسجيل دخول'),
    ]

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='otp_codes')
    code = models.CharField(max_length=6)
    purpose = models.CharField(max_length=10, choices=PURPOSE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'رمز تحقق'
        verbose_name_plural = 'رموز التحقق'

    def __str__(self):
        return f'{self.user.username} - {self.code}'

    def is_valid(self):
        from django.utils import timezone
        from datetime import timedelta
        # صالح 10 دقائق
        expiry = self.created_at + timedelta(minutes=10)
        return not self.is_used and timezone.now() < expiry

    @classmethod
    def generate(cls, user, purpose):
        import random
        # احذف الأكواد القديمة
        cls.objects.filter(user=user, purpose=purpose, is_used=False).update(is_used=True)
        # أنشئ كود جديد
        code = str(random.randint(100000, 999999))
        return cls.objects.create(user=user, code=code, purpose=purpose)
