from django.urls import path
from . import views, verification_views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('verify-email/', verification_views.verify_email, name='verify_email'),
    path('confirm/<str:token>/', verification_views.confirm_email, name='confirm_email'),
]
