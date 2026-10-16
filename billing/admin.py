from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'method', 'status', 'omt_reference', 'created_at')
    list_filter = ('status', 'method')
    search_fields = ('user__username', 'omt_reference')
    list_editable = ('status',)
    readonly_fields = ('reference_id', 'created_at', 'verified_at')
