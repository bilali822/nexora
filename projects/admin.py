from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from adminsortable2.admin import SortableInlineAdminMixin
from simple_history.admin import SimpleHistoryAdmin
from .models import Project, ProjectImage, BeforeAfter


def thumb(url, size=60):
    if not url:
        return '—'
    return format_html('<img src="{}" style="height:{}px;border-radius:8px;object-fit:cover" />', url, size)


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 3
    fields = ('image', 'image_preview', 'caption')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        return thumb(obj.image.url, 80) if obj.image else '—'
    image_preview.short_description = 'معاينة'


class BeforeAfterInline(admin.StackedInline):
    model = BeforeAfter
    extra = 1


class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project
        fields = ('id', 'title', 'slug', 'category', 'client_name', 'is_featured', 'created_at')


@admin.register(Project)
class ProjectAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = ProjectResource
    list_display = ('cover_thumb', 'title', 'category_badge', 'client_name', 'is_featured', 'is_featured_badge', 'created_at')
    list_filter = ('category', 'is_featured', 'created_at')
    list_editable = ('is_featured',)
    search_fields = ('title', 'short_description', 'tech_stack', 'client_name')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'cover_preview')
    inlines = [ProjectImageInline, BeforeAfterInline]
    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('title', 'slug', 'category', 'client_name', 'is_featured', 'created_at')
        }),
        ('الوصف', {
            'fields': ('short_description', 'description', 'tech_stack')
        }),
        ('الحالة', {
            'fields': ('challenge', 'solution', 'result'),
            'classes': ('collapse',)
        }),
        ('الوسائط', {
            'fields': ('cover', 'cover_preview', 'url')
        }),
    )

    def cover_thumb(self, obj):
        return thumb(obj.cover.url, 80) if obj.cover else '—'
    cover_thumb.short_description = 'الغلاف'

    def cover_preview(self, obj):
        if obj.cover:
            return format_html('<img src="{}" style="max-width:400px;border-radius:12px" />', obj.cover.url)
        return '—'
    cover_preview.short_description = 'معاينة الغلاف'

    def category_badge(self, obj):
        colors = {
            'website': '#5B8CFF', 'webapp': '#10B981', 'store': '#F59E0B',
            'dashboard': '#EF4444', 'ui': '#8B5CF6',
        }
        color = colors.get(obj.category, '#888')
        return format_html(
            '<span style="background:{};color:#fff;padding:4px 10px;border-radius:12px;font-size:11px">{}</span>',
            color, obj.get_category_display()
        )
    category_badge.short_description = 'النوع'

    def is_featured_badge(self, obj):
        if obj.is_featured:
            return format_html('<span style="color:#10B981;font-size:18px">✓</span>')
        return format_html('<span style="color:#aaa">—</span>')
    is_featured_badge.short_description = 'مميز'
