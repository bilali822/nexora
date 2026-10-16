from django.db import models
from django.urls import reverse


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('website', 'موقع'),
        ('webapp', 'تطبيق ويب'),
        ('store', 'متجر إلكتروني'),
        ('dashboard', 'لوحة تحكم'),
        ('ui', 'تصميم UI/UX'),
    ]
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    client_name = models.CharField(max_length=100, blank=True)
    short_description = models.CharField(max_length=250)
    description = models.TextField()
    challenge = models.TextField(blank=True, help_text='التحدي')
    solution = models.TextField(blank=True, help_text='الحل')
    result = models.TextField(blank=True, help_text='النتيجة')
    cover = models.ImageField(upload_to='projects/covers/')
    url = models.URLField(blank=True)
    tech_stack = models.CharField(max_length=200)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "مشروع"
        verbose_name_plural = "المشاريع"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('projects:detail', kwargs={'slug': self.slug})

    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(',') if t.strip()]


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)


    class Meta:
        verbose_name = "صورة مشروع"
        verbose_name_plural = "صور المشاريع"

    def __str__(self):
        return f'صورة - {self.project.title}'


class BeforeAfter(models.Model):
    project = models.ForeignKey(Project, related_name='before_after', on_delete=models.CASCADE)
    before = models.ImageField(upload_to='projects/before/')
    after = models.ImageField(upload_to='projects/after/')
    label = models.CharField(max_length=100, blank=True)


    class Meta:
        verbose_name = "قبل/بعد"
        verbose_name_plural = "قبل وبعد"

    def __str__(self):
        return f'قبل/بعد - {self.project.title}'
