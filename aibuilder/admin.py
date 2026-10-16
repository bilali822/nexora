from django.contrib import admin
from .models import GeneratedWebsite


@admin.register(GeneratedWebsite)
class GeneratedWebsiteAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created_at')
    list_filter = ('status',)
    readonly_fields = ('created_at',)
