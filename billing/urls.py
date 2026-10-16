from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('omt/<int:payment_id>/', views.omt_payment, name='omt_payment'),
    path('success/<int:payment_id>/', views.payment_success, name='success'),
    path('my-payments/', views.my_payments, name='my_payments'),
]
