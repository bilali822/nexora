from simple_history.models import HistoricalRecords
from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Service(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    details = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    starting_price = models.CharField(max_length=50, blank=True)
    delivery_time = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "الخدمة"
        verbose_name_plural = "الخدمات"
        ordering = ['order']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:service_detail', kwargs={'slug': self.slug})
    history = HistoricalRecords()


class WhyUs(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='fa-star')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "ميزة"
        verbose_name_plural = "لماذا نحن"
        ordering = ['order']

    def __str__(self):
        return self.title
    history = HistoricalRecords()


class ProcessStep(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "خطوة"
        verbose_name_plural = "طريقة العمل"
        ordering = ['order']

    def __str__(self):
        return f'{self.order}. {self.title}'
    history = HistoricalRecords()


class Stat(models.Model):
    label = models.CharField(max_length=80)
    value = models.CharField(max_length=20)
    icon = models.CharField(max_length=50, default='fa-chart-bar')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "إحصائية"
        verbose_name_plural = "الإحصائيات"
        ordering = ['order']

    def __str__(self):
        return f'{self.value} {self.label}'
    history = HistoricalRecords()


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    avatar = models.ImageField(upload_to='testimonials/', blank=True)
    rating = models.PositiveIntegerField(default=5)
    is_active = models.BooleanField(default=True)


    class Meta:
        verbose_name = "رأي عميل"
        verbose_name_plural = "آراء العملاء"

    def __str__(self):
        return self.name
    history = HistoricalRecords()


class Client(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='clients/', blank=True)
    website = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "عميل"
        verbose_name_plural = "العملاء"
        ordering = ['order']

    def __str__(self):
        return self.name
    history = HistoricalRecords()


class FAQ(models.Model):
    question = models.CharField(max_length=250)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "سؤال شائع"
        verbose_name_plural = "الأسئلة الشائعة"
        ordering = ['order']

    def __str__(self):
        return self.question
    history = HistoricalRecords()


class PricingPlan(models.Model):
    name = models.CharField(max_length=80)
    tagline = models.CharField(max_length=150, blank=True)
    price = models.CharField(max_length=50)
    is_popular = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "باقة"
        verbose_name_plural = "الباقات"
        ordering = ['order']

    def __str__(self):
        return self.name
    history = HistoricalRecords()


class PricingFeature(models.Model):
    plan = models.ForeignKey(PricingPlan, related_name='features', on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    included = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "ميزة باقة"
        verbose_name_plural = "ميزات الباقات"
        ordering = ['order']

    def __str__(self):
        return self.text


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.CharField(max_length=300)
    content = models.TextField()
    cover = models.ImageField(upload_to='blog/', blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "مقال"
        verbose_name_plural = "المدونة"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:blog_detail', kwargs={'slug': self.slug})
    history = HistoricalRecords()


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


    class Meta:
        verbose_name = "رسالة تواصل"
        verbose_name_plural = "رسائل التواصل"

    def __str__(self):
        return f'{self.name} - {self.subject}'


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=80, default='Nexora')
    tagline = models.CharField(max_length=200, default='Web & Apps')
    email = models.EmailField(default='hello@nexora.dev')
    phone = models.CharField(max_length=30, blank=True)
    whatsapp = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=200, blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    github = models.URLField(blank=True)
    meta_description = models.TextField(default='Nexora تصمم وتطور مواقع وتطبيقات ويب حديثة.')

    class Meta:
        verbose_name = "إعدادات الموقع"
        verbose_name_plural = "إعدادات الموقع"

    def __str__(self):
        return 'إعدادات الموقع'

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
    history = HistoricalRecords()