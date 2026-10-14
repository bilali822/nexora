from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import BlogPost
from projects.models import Project


class ProjectSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'
    def items(self):
        return Project.objects.all()
    def lastmod(self, obj):
        return obj.created_at


class BlogSitemap(Sitemap):
    priority = 0.6
    changefreq = 'weekly'
    def items(self):
        return BlogPost.objects.filter(is_published=True)
    def lastmod(self, obj):
        return obj.created_at


class StaticSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'
    def items(self):
        return ['core:home', 'core:services', 'core:about', 'core:pricing',
                'core:blog_list', 'core:contact', 'projects:list']
    def location(self, item):
        return reverse(item)
