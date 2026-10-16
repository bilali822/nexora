from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.db import transaction
from .models import Payment
from .forms import OMTConfirmForm


@login_required
@require_http_methods(['GET', 'POST'])
def omt_payment(request, payment_id):
    """صفحة الدفع عبر OMT Pay"""
    # تحقق من الملكية
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)

    # تحقق من الحالة
    if payment.status == 'verified':
        messages.info(request, '✅ هذه الدفعة تم التحقق منها مسبقاً')
        return redirect('billing:my_payments')
    if payment.status == 'rejected':
        messages.error(request, '❌ هذه الدفعة مرفوضة — تواصل معنا')
        return redirect('billing:my_payments')
    if payment.status == 'submitted':
        messages.info(request, '⏳ دفعتك قيد المراجعة')
        return redirect('billing:my_payments')

    # تحقق من المبلغ
    if payment.amount <= 0:
        messages.error(request, '❌ المبلغ غير محدد — تواصل معنا')
        return redirect('billing:my_payments')

    if request.method == 'POST':
        form = OMTConfirmForm(request.POST, instance=payment)
        if form.is_valid():
            with transaction.atomic():
                p = form.save(commit=False)
                p.status = 'submitted'
                p.submitted_at = timezone.now()
                p.save()

                # إيميل للإدارة
                try:
                    send_mail(
                        subject=f'💰 دفعة جديدة - OMT Pay',
                        message=f'''دفعة جديدة بانتظار التحقق:

👤 المستخدم: {request.user.username}
📧 الإيميل: {request.user.email}
💵 المبلغ: ${p.amount} {p.currency}
📋 رقم OMT: {p.omt_reference}
📱 الهاتف: {p.omt_phone}

🔗 تحقق: https://nexorastudiomakerwebandapps.pythonanywhere.com/admin/billing/payment/{p.id}/change/''',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[settings.ADMIN_EMAIL],
                        fail_silently=True,
                    )
                except Exception as e:
                    print(f'Email error: {e}')

            messages.success(request, '✅ تم إرسال رقم الدفع — رح نتحقق خلال 24 ساعة')
            return redirect('billing:success', payment.id)
        else:
            messages.error(request, '❌ في خطأ في البيانات — تحقق من الحقول')
    else:
        form = OMTConfirmForm(instance=payment)

    return render(request, 'billing/omt_payment.html', {
        'payment': payment,
        'form': form,
    })


@login_required
def payment_success(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    return render(request, 'billing/success.html', {'payment': payment})


@login_required
def my_payments(request):
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'billing/my_payments.html', {'payments': payments})
