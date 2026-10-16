from django.contrib import admin
from .models import Project, ProjectImage, BeforeAfter


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 3


class BeforeAfterInline(admin.StackedInline):
    model = BeforeAfter
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'created_at')
    list_filter = ('category', 'is_featured')
    list_editable = ('is_featured',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline, BeforeAfterInline]
