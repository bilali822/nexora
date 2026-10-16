from django.contrib import admin
from django.utils.html import format_html
from .models import GeneratedWebsite


@admin.register(GeneratedWebsite)
class GeneratedWebsiteAdmin(admin.ModelAdmin):
    list_display = ('user', 'prompt_short', 'status_badge', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'prompt')
    readonly_fields = ('created_at',)

    def prompt_short(self, obj):
        return obj.prompt[:80] + '...' if len(obj.prompt) > 80 else obj.prompt
    prompt_short.short_description = 'الوصف'

    def status_badge(self, obj):
        colors = {'pending': '#F59E0B', 'completed': '#10B981', 'failed': '#EF4444'}
        return format_html(
            '<span style="background:{};color:#fff;padding:4px 12px;border-radius:12px;font-size:11px">{}</span>',
            colors.get(obj.status, '#888'), obj.get_status_display()
        )
    status_badge.short_description = 'الحالة'
