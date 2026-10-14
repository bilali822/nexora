from django.urls import path
from . import views

app_name = 'requests_app'

urlpatterns = [
    path('', views.request_form, name='form'),
    path('success/<uuid:tracking_id>/', views.success, name='success'),
    path('track/', views.track, name='track'),
]
