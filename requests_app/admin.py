from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from simple_history.admin import SimpleHistoryAdmin
from .models import ProjectRequest, ProjectAttachment, PriceCalculator


class ProjectRequestResource(resources.ModelResource):
    class Meta:
        model = ProjectRequest
        fields = ('tracking_id', 'name', 'email', 'whatsapp', 'project_type',
                  'design_style', 'budget', 'status', 'created_at')
        export_order = ('tracking_id', 'name', 'email', 'whatsapp', 'project_type',
                        'design_style', 'budget', 'status', 'created_at')


class AttachmentInline(admin.TabularInline):
    model = ProjectAttachment
    extra = 0
    readonly_fields = ('uploaded_at', 'file_link')

    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">📎 {}</a>', obj.file.url, obj.file.name.split('/')[-1])
        return '—'
    file_link.short_description = 'الملف'


@admin.register(ProjectRequest)
class ProjectRequestAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = ProjectRequestResource
    list_display = (
        'status_badge', 'name', 'project_type', 'budget',
        'whatsapp_link', 'email_link', 'waiting_time', 'created_at'
    )
    list_filter = ('status', 'project_type', 'budget', 'design_style', 'created_at')
    search_fields = ('name', 'email', 'whatsapp', 'features', 'tracking_id')
    readonly_fields = ('tracking_id', 'created_at', 'quick_actions')
    date_hierarchy = 'created_at'
    inlines = [AttachmentInline]
    list_per_page = 25
    actions = ['mark_review', 'mark_contacted', 'mark_accepted', 'mark_rejected', 'mark_done']
    fieldsets = (
        ('معلومات العميل', {
            'fields': ('name', 'email', 'whatsapp', 'quick_actions')
        }),
        ('تفاصيل المشروع', {
            'fields': ('project_type', 'design_style', 'reference_url',
                       'features', 'budget', 'deadline', 'notes')
        }),
        ('إدارة', {
            'fields': ('status', 'admin_notes', 'tracking_id', 'created_at')
        }),
    )

    def status_badge(self, obj):
        colors = {
            'new': '#5B8CFF', 'review': '#F59E0B', 'contacted': '#8B5CF6',
            'accepted': '#10B981', 'rejected': '#EF4444', 'done': '#6b7a9e',
        }
        color = colors.get(obj.status, '#888')
        return format_html(
            '<span style="background:{};color:#fff;padding:4px 12px;border-radius:12px;font-size:11px;font-weight:bold">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'الحالة'

    def whatsapp_link(self, obj):
        if not obj.whatsapp:
            return '—'
        num = obj.whatsapp.replace(' ', '').replace('+', '').replace('-', '')
        return format_html(
            '<a href="https://wa.me/{}" target="_blank" style="color:#25D366;font-weight:bold">💬 واتساب</a>',
            num
        )
    whatsapp_link.short_description = 'تواصل'

    def email_link(self, obj):
        return format_html('<a href="mailto:{}" style="color:#5B8CFF">✉ إيميل</a>', obj.email)
    email_link.short_description = 'إيميل'

    def waiting_time(self, obj):
        from django.utils import timezone
        delta = timezone.now() - obj.created_at
        hours = int(delta.total_seconds() // 3600)
        if hours < 1:
            return mark_safe('<span style="color:#10B981">الآن</span>')
        elif hours < 24:
            return format_html('<span style="color:#F59E0B">{} ساعة</span>', hours)
        else:
            days = hours // 24
            color = '#EF4444' if days > 3 else '#F59E0B'
            return format_html('<span style="color:{}">{} يوم</span>', color, days)
    waiting_time.short_description = 'الانتظار'

    def quick_actions(self, obj):
        if not obj.pk:
            return '—'
        return format_html(
            '<a class="button" href="https://wa.me/{}" target="_blank" style="background:#25D366;color:#fff;padding:8px 16px;border-radius:8px;text-decoration:none;margin-inline-end:8px">💬 واتساب</a>'
            '<a class="button" href="mailto:{}" style="background:#5B8CFF;color:#fff;padding:8px 16px;border-radius:8px;text-decoration:none">✉ إيميل</a>',
            obj.whatsapp.replace(' ', '').replace('+', ''), obj.email
        )
    quick_actions.short_description = 'إجراءات سريعة'

    @admin.action(description='🟡 تعليم كـ "قيد المراجعة"')
    def mark_review(self, request, queryset):
        queryset.update(status='review')

    @admin.action(description='🟣 تعليم كـ "تم التواصل"')
    def mark_contacted(self, request, queryset):
        queryset.update(status='contacted')

    @admin.action(description='🟢 قبول')
    def mark_accepted(self, request, queryset):
        queryset.update(status='accepted')

    @admin.action(description='🔴 رفض')
    def mark_rejected(self, request, queryset):
        queryset.update(status='rejected')

    @admin.action(description='⚫ مكتمل')
    def mark_done(self, request, queryset):
        queryset.update(status='done')


@admin.register(PriceCalculator)
class PriceCalculatorAdmin(admin.ModelAdmin):
    list_display = ('label', 'price', 'order')
    list_editable = ('price', 'order')
