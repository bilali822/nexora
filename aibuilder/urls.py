from django.urls import path
from . import views

app_name = 'aibuilder'

urlpatterns = [
    path('generate/', views.generate_site_view, name='generate'),
    path('preview/<int:site_id>/', views.preview_site_view, name='preview_site'),
    path('export/<int:site_id>/', views.export_zip, name='export_zip'),
    path('edit/<int:site_id>/', views.edit_with_ai, name='edit_with_ai'),
    path('deploy/<int:site_id>/', views.deploy_github, name='deploy_github'),
]
