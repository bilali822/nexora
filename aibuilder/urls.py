from django.urls import path
from . import views

app_name = 'aibuilder'

urlpatterns = [
    path('generate/', views.generate_site_view, name='generate'),
    path('preview/<int:site_id>/', views.fullscreen_preview, name='preview_site'),
    path('manage/<int:site_id>/', views.manage_site, name='manage_site'),
    path('export/<int:site_id>/', views.export_zip, name='export_zip'),
    path('edit/<int:site_id>/', views.edit_with_ai, name='edit_with_ai'),
    path('publish/<int:site_id>/', views.publish_here_now, name='publish_here_now'),
]
