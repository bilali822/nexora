from django.contrib import admin
from django.utils.html import format_html
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'method', 'status', 'status_badge', 'omt_reference', 'created_at')
    list_filter = ('status', 'method')
    search_fields = ('user__username', 'omt_reference')
    readonly_fields = ('reference_id', 'created_at', 'verified_at')
    list_editable = ('status',)

    def status_badge(self, obj):
        colors = {'pending': '#F59E0B', 'submitted': '#5B8CFF', 'verified': '#10B981', 'rejected': '#EF4444'}
        return format_html('<span style="background:{};color:#fff;padding:4px 12px;border-radius:12px;font-size:11px">{}</span>', colors.get(obj.status, '#888'), obj.get_status_display())
    status_badge.short_description = 'الحالة'
