from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from .models import ProjectRequest, ProjectAttachment


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
            return format_html('<a href="{}" target="_blank">📎 {}</a>',
                               obj.file.url, obj.file.name.split('/')[-1])
        return '—'
    file_link.short_description = 'الملف'


@admin.register(ProjectRequest)
class ProjectRequestAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = ProjectRequestResource
    list_display = (
        'status_badge',
        'payment_badge',              # ← حالة الدفع
        'name',
        'project_type',
        'budget',
        'whatsapp_link',
        'email_link',
        'waiting_time',
        'created_at',
    )
    list_filter = (
        'status',
        'project_type',
        'budget',
        'design_style',
        'created_at',
    )
    search_fields = ('name', 'email', 'whatsapp', 'features', 'tracking_id')
    readonly_fields = ('tracking_id', 'created_at', 'quick_actions', 'payment_details')
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
        ('💰 حالة الدفع', {
            'fields': ('payment_details',),
            'classes': ('collapse',),
        }),
        ('إدارة', {
            'fields': ('status', 'admin_notes', 'tracking_id', 'created_at')
        }),
    )

    # ============ Status Badge ============
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

    # ============ Payment Badge ============
    def payment_badge(self, obj):
        """حالة الدفع"""
        try:
            payment = obj.payment
        except Exception:
            return format_html(
                '<span style="background:#4a5568;color:#fff;padding:4px 10px;border-radius:12px;font-size:10px;font-weight:700">— لا دفعة</span>'
            )

        status_info = {
            'pending': ('#F59E0B', '⏳', 'بانتظار الدفع'),
            'submitted': ('#5B8CFF', '📩', 'قيد المراجعة'),
            'verified': ('#10B981', '✅', 'تم التحقق'),
            'rejected': ('#EF4444', '❌', 'مرفوض'),
        }
        color, icon, label = status_info.get(payment.status, ('#888', '?', 'غير معروف'))

        # رابط سريع لتغيير الحالة
        admin_url = reverse('admin:billing_payment_change', args=[payment.id])

        return format_html(
            '<a href="{}" style="text-decoration:none">'
            '<span style="background:{};color:#fff;padding:4px 10px;border-radius:12px;font-size:10px;font-weight:700;display:inline-flex;align-items:center;gap:4px">'
            '{} {} · ${}'
            '</span></a>',
            admin_url, color, icon, label, payment.amount
        )
    payment_badge.short_description = 'الدفع'
    payment_badge.admin_order_field = 'payment__status'

    # ============ Payment Details (تفاصيل كاملة) ============
    def payment_details(self, obj):
        """تفاصيل الدفع الكاملة داخل صفحة الطلب"""
        try:
            p = obj.payment
        except Exception:
            return format_html('<p style="color:#888">لا يوجد دفع مسجل</p>')

        status_colors = {
            'pending': '#F59E0B', 'submitted': '#5B8CFF',
            'verified': '#10B981', 'rejected': '#EF4444',
        }
        color = status_colors.get(p.status, '#888')
        admin_url = reverse('admin:billing_payment_change', args=[p.id])

        # زر التحقق / الرفض
        actions_html = ''
        if p.status == 'submitted':
            actions_html = format_html(
                '<div style="margin-top:16px;padding:14px;background:rgba(91,140,255,0.1);border-radius:10px;">'
                '<p style="margin:0 0 10px;color:#fff;font-weight:700">⚡ إجراءات سريعة:</p>'
                '<a href="{}" style="background:#5B8CFF;color:#fff;padding:8px 16px;border-radius:8px;text-decoration:none;font-weight:600;margin-inline-end:8px">'
                'فتح الدفعة للمراجعة'
                '</a>'
                '</div>',
                admin_url
            )

        return format_html('''
        <div style="background:#131a30;border:1px solid #1f2a4a;border-radius:12px;padding:20px;color:#fff;font-family:inherit">
            <h3 style="margin:0 0 16px;color:#fff;border-bottom:1px solid #1f2a4a;padding-bottom:12px">
                💰 تفاصيل الدفع
            </h3>

            <table style="width:100%;border-collapse:collapse">
                <tr>
                    <td style="padding:8px 0;color:#a0aec0;width:140px">الحالة:</td>
                    <td style="padding:8px 0">
                        <span style="background:{};color:#fff;padding:4px 12px;border-radius:12px;font-size:12px;font-weight:700">
                            {}
                        </span>
                    </td>
                </tr>
                <tr>
                    <td style="padding:8px 0;color:#a0aec0">المبلغ:</td>
                    <td style="padding:8px 0;font-weight:700;font-size:16px;color:#10B981">
                        ${} {}
                    </td>
                </tr>
                <tr>
                    <td style="padding:8px 0;color:#a0aec0">طريقة الدفع:</td>
                    <td style="padding:8px 0">{}</td>
                </tr>
                <tr>
                    <td style="padding:8px 0;color:#a0aec0">رقم OMT:</td>
                    <td style="padding:8px 0">
                        <code style="background:#0a0f1c;padding:4px 10px;border-radius:6px;color:#22D3EE;font-size:14px">
                            {}
                        </code>
                    </td>
                </tr>
                <tr>
                    <td style="padding:8px 0;color:#a0aec0">الهاتف:</td>
                    <td style="padding:8px 0">{}</td>
                </tr>
                <tr>
                    <td style="padding:8px 0;color:#a0aec0">تاريخ الطلب:</td>
                    <td style="padding:8px 0">{}</td>
                </tr>
                {}
            </table>

            <div style="margin-top:16px;padding-top:16px;border-top:1px solid #1f2a4a">
                <a href="{}" style="color:#5B8CFF;text-decoration:none;font-weight:600">
                    ← عرض/تعديل الدفعة
                </a>
            </div>
        </div>
        ''',
            color, p.get_status_display(),
            p.amount, p.currency,
            p.get_method_display(),
            p.omt_reference or '—',
            p.omt_phone or '—',
            p.created_at.strftime('%Y-%m-%d %H:%M'),
            actions_html,
            admin_url,
        )
    payment_details.short_description = 'تفاصيل الدفع'

    # ============ Quick Actions ============
    def quick_actions(self, obj):
        if not obj.pk:
            return '—'
        whatsapp_url = f'https://wa.me/{obj.whatsapp.replace(" ", "").replace("+", "")}'
        return format_html(
            '<a class="button" href="{}" target="_blank" style="background:#25D366;color:#fff;padding:8px 16px;border-radius:8px;text-decoration:none;margin-inline-end:8px">💬 واتساب</a>'
            '<a class="button" href="mailto:{}" style="background:#5B8CFF;color:#fff;padding:8px 16px;border-radius:8px;text-decoration:none">✉ إيميل</a>',
            whatsapp_url, obj.email
        )
    quick_actions.short_description = 'إجراءات سريعة'

    # ============ WhatsApp / Email ============
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

    # ============ Waiting Time ============
    def waiting_time(self, obj):
        delta = timezone.now() - obj.created_at
        hours = int(delta.total_seconds() // 3600)
        if hours < 1:
            return format_html('<span style="color:#10B981">الآن</span>')
        elif hours < 24:
            return format_html('<span style="color:#F59E0B">{} ساعة</span>', hours)
        else:
            days = hours // 24
            color = '#EF4444' if days > 3 else '#F59E0B'
            return format_html('<span style="color:{}">{} يوم</span>', color, days)
    waiting_time.short_description = 'الانتظار'

    # ============ Bulk Actions ============
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
