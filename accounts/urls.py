from django.urls import path
from . import views, verification_views, otp_views

app_name = 'accounts'

urlpatterns = [
    path('login/', otp_views.login_with_otp, name='login'),
    path('register/', otp_views.register_with_otp, name='register'),
    path('verify-otp/', otp_views.verify_otp, name='verify_otp'),
    path('resend-otp/', otp_views.resend_otp, name='resend_otp'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('verify-email/', verification_views.verify_email, name='verify_email'),
    path('confirm/<str:token>/', verification_views.confirm_email, name='confirm_email'),
]
