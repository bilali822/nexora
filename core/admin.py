from django.contrib import admin
from django.utils.html import format_html, mark_safe
from django.urls import reverse
from django.utils.safestring import SafeString
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from simple_history.admin import SimpleHistoryAdmin
from tinymce.widgets import TinyMCE
from django.db import models
from .models import (Service, WhyUs, ProcessStep, Stat, Testimonial, Client,
                     FAQ, PricingPlan, PricingFeature, BlogPost, ContactMessage,
                     SiteSettings)


# ============ صور مصغّرة ============
def thumb(url, size=60):
    if not url:
        return '—'
    return format_html('<img src="{}" style="height:{}px;border-radius:8px;object-fit:cover" />', url, size)


# ============ Service ============
@admin.register(Service)
class ServiceAdmin(SortableAdminMixin, SimpleHistoryAdmin):
    list_display = ('icon_preview', 'title', 'starting_price', 'delivery_time', 'order')
    list_display_links = ('title',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('المعلومات الأساسية', {'fields': ('title', 'slug', 'icon', 'order')}),
        ('الوصف', {'fields': ('description', 'details')}),
        ('التسعير', {'fields': ('starting_price', 'delivery_time')}),
    )

    def icon_preview(self, obj):
        if not obj.icon:
            return '—'
        return format_html('<i class="fas {}" style="font-size:20px;color:#8B5CF6"></i>', obj.icon)
    icon_preview.short_description = 'أيقونة'


# ============ WhyUs ============
@admin.register(WhyUs)
class WhyUsAdmin(SortableAdminMixin, SimpleHistoryAdmin):
    list_display = ('icon_preview', 'title', 'order')
    search_fields = ('title',)

    def icon_preview(self, obj):
        return format_html('<i class="fas {}" style="font-size:20px;color:#5B8CFF"></i>', obj.icon)
    icon_preview.short_description = 'أيقونة'


# ============ ProcessStep ============
@admin.register(ProcessStep)
class ProcessStepAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('order', 'title')


# ============ Stat ============
@admin.register(Stat)
class StatAdmin(SortableAdminMixin, SimpleHistoryAdmin):
    list_display = ('icon_preview', 'label', 'value', 'order')

    def icon_preview(self, obj):
        return format_html('<i class="fas {}" style="font-size:20px;color:#10B981"></i>', obj.icon)
    icon_preview.short_description = 'أيقونة'


# ============ Testimonial ============
@admin.register(Testimonial)
class TestimonialAdmin(SimpleHistoryAdmin):
    list_display = ('avatar_thumb', 'name', 'role', 'rating_stars', 'is_active')
    list_filter = ('is_active', 'rating')
    list_editable = ('is_active',)
    search_fields = ('name', 'message')

    def avatar_thumb(self, obj):
        return thumb(obj.avatar.url) if obj.avatar else '—'
    avatar_thumb.short_description = 'الصورة'

    def rating_stars(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span style="color:#fbbf24;font-size:16px">{}</span>', stars)
    rating_stars.short_description = 'التقييم'


# ============ Client ============
@admin.register(Client)
class ClientAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('logo_thumb', 'name', 'website', 'order')

    def logo_thumb(self, obj):
        return thumb(obj.logo.url) if obj.logo else '—'
    logo_thumb.short_description = 'الشعار'


# ============ FAQ ============
@admin.register(FAQ)
class FAQAdmin(SortableAdminMixin, SimpleHistoryAdmin):
    list_display = ('question', 'is_active', 'order')
    list_editable = ('is_active',)
    search_fields = ('question', 'answer')


# ============ Pricing ============
class PricingFeatureInline(admin.TabularInline):
    model = PricingFeature
    extra = 3
    fields = ('text', 'included')


@admin.register(PricingPlan)
class PricingPlanAdmin(SortableAdminMixin, SimpleHistoryAdmin):
    list_display = ('name', 'price', 'is_popular', 'order')
    list_editable = ('is_popular',)
    inlines = [PricingFeatureInline]


# ============ BlogPost ============
class BlogPostResource(resources.ModelResource):
    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'slug', 'excerpt', 'is_published', 'created_at')


@admin.register(BlogPost)
class BlogPostAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = BlogPostResource
    list_display = ('cover_thumb', 'title', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    list_editable = ('is_published',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)

    def cover_thumb(self, obj):
        return thumb(obj.cover.url, 80) if obj.cover else '—'
    cover_thumb.short_description = 'الغلاف'

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in ('content', 'excerpt'):
            kwargs['widget'] = TinyMCE()
        return super().formfield_for_dbfield(db_field, request, **kwargs)


# ============ ContactMessage ============
@admin.register(ContactMessage)
class ContactMessageAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    list_editable = ('is_read',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    actions = ['mark_as_read', 'mark_as_unread']

    @admin.action(description='تعليم كمقروء')
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description='تعليم كغير مقروء')
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)


# ============ SiteSettings (Singleton) ============
@admin.register(SiteSettings)
class SiteSettingsAdmin(SimpleHistoryAdmin):
    fieldsets = (
        ('معلومات الموقع', {'fields': ('site_name', 'tagline', 'meta_description')}),
        ('تواصل', {'fields': ('email', 'phone', 'whatsapp', 'address')}),
        ('سوشيال ميديا', {'fields': ('facebook', 'instagram', 'linkedin', 'twitter', 'github')}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
