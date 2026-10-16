from django.urls import path
from . import views

app_name = 'aibuilder'

urlpatterns = [
    path('generate/', views.generate_site_view, name='generate'),
    path('preview/<int:site_id>/', views.preview_site_view, name='preview_site'),
    path('my-sites/', views.my_sites_view, name='my_sites'),
]
