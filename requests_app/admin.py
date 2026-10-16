from django.contrib import admin
from .models import ProjectRequest, ProjectAttachment


class AttachmentInline(admin.TabularInline):
    model = ProjectAttachment
    extra = 0


@admin.register(ProjectRequest)
class ProjectRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'project_type', 'budget', 'status', 'created_at')
    list_filter = ('status', 'project_type', 'budget')
    list_editable = ('status',)
    search_fields = ('name', 'email', 'whatsapp', 'tracking_id')
    readonly_fields = ('tracking_id', 'created_at')
    inlines = [AttachmentInline]
