from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.http import require_http_methods
from .models import OTPCode
from .forms import RegisterForm

User = get_user_model()


def send_otp_email(user, code, purpose):
    """إرسال رمز OTP بتصميم HTML احترافي"""
    subject_map = {
        'signup': f'🎉 مرحباً بك في Nexora — كود التفعيل: {code}',
        'login': f'🔐 كود تسجيل الدخول: {code}',
    }
    subject = subject_map.get(purpose, f'كودك: {code}')

    context = {
        'user_name': user.first_name or user.username,
        'code': code,
        'purpose': purpose,
        'email': user.email,
    }

    # HTML + نص عادي (fallback)
    html_content = render_to_string('emails/otp_email.html', context)
    text_content = f'''مرحباً {user.first_name or user.username}،

شكراً لانضمامك إلى Nexora — استوديو متخصص بتصميم وتطوير المواقع وتطبيقات الويب.

كود التحقق: {code}

الكود صالح 10 دقائق.

إذا لم تطلب هذا الكود، تجاهل الرسالة.

Nexora — Web & Apps
https://nexorastudiomakerwebandapps.pythonanywhere.com'''

    msg = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)


@require_http_methods(['GET', 'POST'])
def register_with_otp(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            otp = OTPCode.generate(user, 'signup')
            send_otp_email(user, otp.code, 'signup')

            request.session['otp_user_id'] = user.id
            request.session['otp_purpose'] = 'signup'

            messages.success(request, f'📧 تم إرسال كود التحقق إلى {user.email}')
            return redirect('accounts:verify_otp')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def login_with_otp(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = User.objects.filter(email=username).first() or User.objects.filter(username=username).first()

        if user and user.check_password(password):
            if not user.is_active:
                messages.error(request, '❌ الحساب غير مفعّل، أنشئ حساباً جديداً.')
                return redirect('accounts:register')

            otp = OTPCode.generate(user, 'login')
            send_otp_email(user, otp.code, 'login')

            request.session['otp_user_id'] = user.id
            request.session['otp_purpose'] = 'login'

            messages.success(request, f'📧 تم إرسال الكود إلى {user.email}')
            return redirect('accounts:verify_otp')
        else:
            messages.error(request, '❌ اسم المستخدم أو كلمة السر غلط')

    return render(request, 'accounts/login.html')


@require_http_methods(['GET', 'POST'])
def verify_otp(request):
    user_id = request.session.get('otp_user_id')
    purpose = request.session.get('otp_purpose', 'login')

    if not user_id:
        messages.error(request, '❌ انتهت الجلسة، جرب مرة ثانية')
        return redirect('accounts:login')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, '❌ المستخدم غير موجود')
        return redirect('accounts:login')

    if request.method == 'POST':
        code = request.POST.get('code', '').strip()

        otp = OTPCode.objects.filter(
            user=user, purpose=purpose, is_used=False
        ).first()

        if otp and otp.code == code and otp.is_valid():
            otp.is_used = True
            otp.save()

            if not user.is_active:
                user.is_active = True
                user.save()

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            request.session.pop('otp_user_id', None)
            request.session.pop('otp_purpose', None)

            messages.success(request, f'✅ أهلاً {user.first_name or user.username}!')
            return redirect('accounts:profile')
        else:
            messages.error(request, '❌ الكود غلط أو منتهي الصلاحية')

    return render(request, 'accounts/verify_otp.html', {
        'email': user.email,
        'purpose': purpose,
    })


@require_http_methods(['POST'])
def resend_otp(request):
    user_id = request.session.get('otp_user_id')
    purpose = request.session.get('otp_purpose', 'login')

    if not user_id:
        return redirect('accounts:login')

    try:
        user = User.objects.get(id=user_id)
        otp = OTPCode.generate(user, purpose)
        send_otp_email(user, otp.code, purpose)
        messages.success(request, f'📧 تم إرسال كود جديد إلى {user.email}')
    except User.DoesNotExist:
        messages.error(request, '❌ المستخدم غير موجود')

    return redirect('accounts:verify_otp')
