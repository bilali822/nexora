from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import OTPCode
from .forms import RegisterForm

User = get_user_model()


def send_otp_email(user, code, purpose):
    """إرسال رمز OTP للإيميل"""
    subject = 'رمز التحقق - Nexora'
    if purpose == 'signup':
        title = 'تأكيد إنشاء الحساب'
    else:
        title = 'تأكيد تسجيل الدخول'

    message = f'''مرحباً {user.first_name or user.username}،

{title}

رمز التحقق الخاص بك: {code}

⏰ الرمز صالح لمدة 10 دقائق فقط.

إذا لم تطلب هذا الرمز، تجاهل هذه الرسالة.

شكراً،
فريق Nexora'''

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )


@require_http_methods(['GET', 'POST'])
def register_with_otp(request):
    """تسجيل حساب مع إرسال OTP"""
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # الحساب غير مفعّل
            user.save()

            # أنشئ كود OTP
            otp = OTPCode.generate(user, 'signup')
            send_otp_email(user, otp.code, 'signup')

            # احفظ المستخدم في السيشن
            request.session['otp_user_id'] = user.id
            request.session['otp_purpose'] = 'signup'

            messages.success(request, f'📧 تم إرسال رمز التحقق إلى {user.email}')
            return redirect('accounts:verify_otp')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def login_with_otp(request):
    """تسجيل دخول مع OTP"""
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # جرّب تسجيل دخول بالإيميل أو اسم المستخدم
        user = User.objects.filter(email=username).first() or User.objects.filter(username=username).first()

        if user and user.check_password(password):
            if not user.is_active:
                messages.error(request, '❌ الحساب غير مفعّل، أنشئ حساباً جديداً.')
                return redirect('accounts:register')

            # أنشئ OTP
            otp = OTPCode.generate(user, 'login')
            send_otp_email(user, otp.code, 'login')

            request.session['otp_user_id'] = user.id
            request.session['otp_purpose'] = 'login'

            messages.success(request, f'📧 تم إرسال رمز إلى {user.email}')
            return redirect('accounts:verify_otp')
        else:
            messages.error(request, '❌ اسم المستخدم أو كلمة السر غلط')

    return render(request, 'accounts/login.html')


@require_http_methods(['GET', 'POST'])
def verify_otp(request):
    """صفحة إدخال رمز OTP"""
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

        # ابحث عن كود صالح
        otp = OTPCode.objects.filter(
            user=user, purpose=purpose, is_used=False
        ).first()

        if otp and otp.code == code and otp.is_valid():
            # ✅ الكود صح
            otp.is_used = True
            otp.save()

            # فعّل المستخدم
            if not user.is_active:
                user.is_active = True
                user.save()

            # سجّل دخول
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            # نظّف السيشن
            request.session.pop('otp_user_id', None)
            request.session.pop('otp_purpose', None)

            messages.success(request, f'✅ أهلاً {user.first_name or user.username}!')
            return redirect('accounts:profile')
        else:
            messages.error(request, '❌ الرمز غلط أو منتهي الصلاحية')

    return render(request, 'accounts/verify_otp.html', {
        'email': user.email,
        'purpose': purpose,
    })


@require_http_methods(['POST'])
def resend_otp(request):
    """إعادة إرسال الرمز"""
    user_id = request.session.get('otp_user_id')
    purpose = request.session.get('otp_purpose', 'login')

    if not user_id:
        return redirect('accounts:login')

    try:
        user = User.objects.get(id=user_id)
        otp = OTPCode.generate(user, purpose)
        send_otp_email(user, otp.code, purpose)
        messages.success(request, f'📧 تم إرسال رمز جديد إلى {user.email}')
    except User.DoesNotExist:
        messages.error(request, '❌ المستخدم غير موجود')

    return redirect('accounts:verify_otp')
