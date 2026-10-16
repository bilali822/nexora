from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Payment
from .forms import OMTConfirmForm


@login_required
def omt_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    if request.method == 'POST':
        form = OMTConfirmForm(request.POST, instance=payment)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.status = 'submitted'
            payment.save()
            try:
                send_mail('دفعة جديدة - OMT Pay',
                    f'المستخدم: {request.user.username}\nالمبلغ: ${payment.amount}\nOMT: {payment.omt_reference}',
                    settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL], fail_silently=True)
            except Exception:
                pass
            messages.success(request, '✅ تم إرسال رقم الدفع')
            return redirect('billing:success', payment.id)
    else:
        form = OMTConfirmForm(instance=payment)
    return render(request, 'billing/omt_payment.html', {'payment': payment, 'form': form})


@login_required
def payment_success(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    return render(request, 'billing/success.html', {'payment': payment})


@login_required
def my_payments(request):
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'billing/my_payments.html', {'payments': payments})
