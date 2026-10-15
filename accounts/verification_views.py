from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


@login_required
def verify_phone(request):
    """صفحة إدخال رقم الهاتف وإرسال الرمز"""
    profile = request.user.profile

    if request.method == 'POST':
        phone = request.POST.get('phone')
        if phone:
            profile.phone = phone
            profile.save()
            try:
                from phone_verify.services import send_security_code
                send_security_code(phone, 'sms')
                messages.success(request, 'تم إرسال رمز التحقق إلى هاتفك.')
                return redirect('accounts:verify_phone_code')
            except Exception as e:
                messages.error(request, f'فشل إرسال الرمز. تحقق من إعدادات Twilio.')
                print(f'Phone verify error: {e}')
        else:
            messages.error(request, 'الرجاء إدخال رقم الهاتف.')

    return render(request, 'accounts/verify_phone.html', {'profile': profile})


@login_required
def verify_phone_code(request):
    """صفحة إدخال رمز التحقق"""
    profile = request.user.profile

    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            from phone_verify.services import verify_security_code
            verify_security_code(str(profile.phone), code)
            profile.phone_verified = True
            profile.save()
            messages.success(request, 'تم التحقق من رقم هاتفك بنجاح! ✅')
            return redirect('accounts:profile')
        except Exception as e:
            messages.error(request, 'الرمز غير صحيح أو منتهي الصلاحية.')
            print(f'Verify error: {e}')

    return render(request, 'accounts/verify_phone_code.html', {'profile': profile})


@login_required
def verify_email(request):
    """صفحة إعادة إرسال رابط التحقق"""
    profile = request.user.profile

    if request.method == 'POST':
        try:
            from allauth.account.models import EmailAddress
            email_address = EmailAddress.objects.get(user=request.user, email=request.user.email)
            email_address.send_confirmation(request)
            messages.success(request, 'تم إرسال رابط التحقق إلى بريدك.')
        except Exception as e:
            messages.error(request, 'فشل إرسال البريد. حاول مرة أخرى.')
            print(f'Email verify error: {e}')
        return redirect('accounts:profile')

    return render(request, 'accounts/verify_email.html')
