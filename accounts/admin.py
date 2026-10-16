from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'email_verified', 'created_at')
    search_fields = ('user__username', 'user__email', 'company')
    list_filter = ('email_verified', 'created_at')
    readonly_fields = ('created_at',)
