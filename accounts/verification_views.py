from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from allauth.account.models import EmailAddress
from django.utils.crypto import get_random_string


@login_required
def verify_email(request):
    """إرسال رابط تحقق"""
    if request.method == 'POST':
        try:
            email = request.user.email
            if not email:
                messages.error(request, '❌ ما في إيميل على حسابك')
                return redirect('accounts:profile')

            token = get_random_string(64)
            request.session['email_verify_token'] = token
            request.session['email_verify_email'] = email

            url = request.build_absolute_uri(f'/accounts/confirm/{token}/')

            send_mail(
                '[Nexora] تأكيد البريد',
                f'مرحباً {request.user.username},\n\nاضغط:\n{url}\n\nفريق Nexora',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            messages.success(request, f'✅ تم إرسال الرابط إلى {email}')
        except Exception as e:
            messages.error(request, f'❌ خطأ: {e}')
        return redirect('accounts:profile')
    return render(request, 'accounts/verify_email.html')


@login_required
def confirm_email(request, token):
    """تأكيد الإيميل"""
    saved = request.session.get('email_verify_token')
    if token and token == saved:
        profile = request.user.profile
        profile.email_verified = True
        profile.save()

        email = request.session.get('email_verify_email')
        if email:
            EmailAddress.objects.update_or_create(
                user=request.user, email=email,
                defaults={'primary': True, 'verified': True}
            )

        request.session.pop('email_verify_token', None)
        request.session.pop('email_verify_email', None)
        messages.success(request, '✅ تم تأكيد بريدك بنجاح!')
        return redirect('accounts:profile')
    messages.error(request, '❌ الرابط غير صالح')
    return redirect('accounts:profile')
