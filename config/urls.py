from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.i18n import set_language
from core.sitemaps import ProjectSitemap, BlogSitemap, StaticSitemap

sitemaps = {
    'projects': ProjectSitemap,
    'blog': BlogSitemap,
    'static': StaticSitemap,
}

# استبدل صفحة الأدمن الرئيسية بـ Dashboard مخصص
from core.admin_dashboard import custom_admin_index
admin.site.index = custom_admin_index

# تسميات
admin.site.site_header = 'Nexora — لوحة التحكم'
admin.site.site_title = 'Nexora Admin'
admin.site.index_title = 'مرحباً بك في Nexora'

urlpatterns = [
    path('i18n/setlang/', set_language, name='set_language'),
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('', include('core.urls')),
    path('projects/', include('projects.urls')),
    path('request/', include('requests_app.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'core.views.handler404'
