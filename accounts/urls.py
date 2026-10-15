from django.urls import path
from . import views, verification_views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('verify-phone/', verification_views.verify_phone, name='verify_phone'),
    path('verify-phone/code/', verification_views.verify_phone_code, name='verify_phone_code'),
    path('verify-email/', verification_views.verify_email, name='verify_email'),
]
