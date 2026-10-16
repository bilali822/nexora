from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'user_link',
        'amount_display',
        'method',
        'status_badge',
        'omt_reference_display',
        'request_link',
        'created_at',
    )
    list_filter = ('status', 'method', 'currency', 'created_at')
    search_fields = ('user__username', 'user__email', 'omt_reference', 'omt_phone')
    readonly_fields = ('reference_id', 'created_at', 'verified_at', 'submitted_at', 'request_details')
    date_hierarchy = 'created_at'
    list_per_page = 25
    actions = ['action_verify', 'action_reject', 'action_pending']

    fieldsets = (
        ('👤 المستخدم', {
            'fields': ('user', 'project_request', 'request_details')
        }),
        ('💰 معلومات الدفع', {
            'fields': ('amount', 'currency', 'method', 'status')
        }),
        ('📱 معلومات OMT', {
            'fields': ('omt_reference', 'omt_phone')
        }),
        ('📝 ملاحظات', {
            'fields': ('notes', 'admin_notes')
        }),
        ('⚙️ تفاصيل النظام', {
            'fields': ('reference_id', 'created_at', 'submitted_at', 'verified_at'),
            'classes': ('collapse',)
        }),
    )

    # ============ Status Badge ============
    def status_badge(self, obj):
        colors = {
            'pending': '#F59E0B', 'submitted': '#5B8CFF',
            'verified': '#10B981', 'rejected': '#EF4444',
        }
        icons = {'pending': '⏳', 'submitted': '📩', 'verified': '✅', 'rejected': '❌'}
        color = colors.get(obj.status, '#888')
        icon = icons.get(obj.status, '?')
        return format_html(
            '<span style="background:{};color:#fff;padding:5px 12px;border-radius:12px;font-size:11px;font-weight:700">'
            '{} {}</span>',
            color, icon, obj.get_status_display()
        )
    status_badge.short_description = 'الحالة'

    # ============ Amount ============
    def amount_display(self, obj):
        return format_html(
            '<span style="color:#10B981;font-weight:700;font-size:14px">${} {}</span>',
            obj.amount, obj.currency
        )
    amount_display.short_description = 'المبلغ'

    # ============ User Link ============
    def user_link(self, obj):
        if not obj.user:
            return '—'
        url = f'/nexora-control-2026/auth/user/{obj.user.id}/change/'
        return format_html('<a href="{}" style="font-weight:600">{}</a>', url, obj.user.username)
    user_link.short_description = 'المستخدم'

    # ============ Request Link ============
    def request_link(self, obj):
        if not obj.project_request:
            return '—'
        url = f'/nexora-control-2026/requests_app/projectrequest/{obj.project_request.id}/change/'
        return format_html(
            '<a href="{}" style="color:#8B5CF6;font-weight:600">📋 {}</a>',
            url, obj.project_request.name
        )
    request_link.short_description = 'الطلب'

    # ============ OMT Reference ============
    def omt_reference_display(self, obj):
        if not obj.omt_reference:
            return format_html('<span style="color:#6b7a9e">—</span>')
        return format_html(
            '<code style="background:#0a0f1c;padding:4px 10px;border-radius:6px;color:#22D3EE;font-size:12px">{}</code>',
            obj.omt_reference
        )
    omt_reference_display.short_description = 'رقم OMT'

    # ============ Request Details (in change form) ============
    def request_details(self, obj):
        if not obj.project_request:
            return '—'
        req = obj.project_request
        url = f'/nexora-control-2026/requests_app/projectrequest/{req.id}/change/'
        return format_html('''
        <div style="background:#131a30;border-radius:10px;padding:16px;margin-top:8px">
            <p style="margin:0 0 8px"><strong>👤 الاسم:</strong> {}</p>
            <p style="margin:0 0 8px"><strong>📧 الإيميل:</strong> {}</p>
            <p style="margin:0 0 8px"><strong>💬 واتساب:</strong> {}</p>
            <p style="margin:0 0 8px"><strong>📦 النوع:</strong> {}</p>
            <p style="margin:0 0 8px"><strong>💰 الميزانية:</strong> {}</p>
            <p style="margin:8px 0 0"><a href="{}" style="color:#5B8CFF">← عرض الطلب كامل</a></p>
        </div>
        ''', req.name, req.email, req.whatsapp,
            req.get_project_type_display(), req.get_budget_display(), url)
    request_details.short_description = 'تفاصيل الطلب'

    # ============ Bulk Actions ============
    @admin.action(description='✅ التحقق من الدفعة')
    def action_verify(self, request, queryset):
        count = 0
        for p in queryset:
            if p.status == 'submitted' and p.amount > 0:
                p.status = 'verified'
                p.verified_at = timezone.now()
                p.save()
                count += 1
                # إيميل للعميل
                try:
                    if p.user and p.user.email:
                        send_mail(
                            '✅ تم التحقق من دفعتك - Nexora',
                            f'مرحباً {p.user.first_name or p.user.username},\n\n'
                            f'تم التحقق من دفعتك بمبلغ ${p.amount}.\n'
                            f'رقم المرجع: {p.omt_reference}\n\n'
                            f'رح نبدأ العمل على مشروعك قريباً.\n\n'
                            f'فريق Nexora',
                            settings.DEFAULT_FROM_EMAIL,
                            [p.user.email],
                            fail_silently=True,
                        )
                except Exception:
                    pass
        self.message_user(request, f'✅ تم التحقق من {count} دفعة')

    @admin.action(description='❌ رفض الدفعة')
    def action_reject(self, request, queryset):
        count = queryset.update(status='rejected')
        self.message_user(request, f'❌ تم رفض {count} دفعة')

    @admin.action(description='⏳ إرجاع لـ "بانتظار الدفع"')
    def action_pending(self, request, queryset):
        count = queryset.update(status='pending')
        self.message_user(request, f'⏳ تم إرجاع {count} دفعة')

    # ============ Save ============
    def save_model(self, request, obj, form, change):
        # إذا تغيّرت الحالة لـ verified
        if change and obj.status == 'verified' and not obj.verified_at:
            obj.verified_at = timezone.now()
        # إذا تغيّرت الحالة لـ submitted
        if change and obj.status == 'submitted' and not obj.submitted_at:
            obj.submitted_at = timezone.now()
        super().save_model(request, obj, form, change)
