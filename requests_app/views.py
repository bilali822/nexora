from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .forms import ProjectRequestForm
from .models import ProjectRequest, ProjectAttachment
import urllib.request, json


def _telegram_notify(text):
    token = settings.TELEGRAM_BOT_TOKEN
    chat = settings.TELEGRAM_CHAT_ID
    if not token or not chat:
        return
    try:
        url = f'https://api.telegram.org/bot{token}/sendMessage'
        data = json.dumps({'chat_id': chat, 'text': text, 'parse_mode': 'HTML'}).encode()
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass


def request_form(request):
    if request.method == 'POST':
        form = ProjectRequestForm(request.POST, request.FILES)
        if form.is_valid():
            req_obj = form.save()
                        # إنشاء دفعة OMT تلقائياً
            try:
                from billing.models import Payment
                Payment.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    project_request=req_obj,
                    amount=0,
                    method='omt',
                    status='pending',
                )
            except Exception as e:
                print(f'Payment creation error: {e}')
            # ملفات مرفوعة
            for f in request.FILES.getlist('attachments'):
                ProjectAttachment.objects.create(request=req_obj, file=f)

            # إيميل للإدارة
            try:
                send_mail(
                    subject=f'طلب جديد: {req_obj.name}',
                    message=f'الاسم: {req_obj.name}\nالإيميل: {req_obj.email}\nواتساب: {req_obj.whatsapp}\nالنوع: {req_obj.get_project_type_display()}\nالميزانية: {req_obj.get_budget_display()}\n\n{req_obj.features}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass

            # إشعار تيليجرام
            _telegram_notify(
                f'🔔 <b>طلب جديد</b>\n'
                f'👤 {req_obj.name}\n'
                f'📧 {req_obj.email}\n'
                f'💬 {req_obj.whatsapp}\n'
                f'📦 {req_obj.get_project_type_display()}\n'
                f'💰 {req_obj.get_budget_display()}'
            )

            messages.success(request, 'تم إرسال طلبك، رح نتواصل معك قريباً.')
            return redirect('requests_app:success', tracking_id=req_obj.tracking_id)
    else:
        form = ProjectRequestForm()
    return render(request, 'requests_app/form.html', {'form': form})


def success(request, tracking_id):
    req = get_object_or_404(ProjectRequest, tracking_id=tracking_id)
    return render(request, 'requests_app/success.html', {'req': req})


def track(request):
    req = None
    q = request.GET.get('id', '')
    if q:
        req = ProjectRequest.objects.filter(tracking_id=q).first()
    return render(request, 'requests_app/track.html', {'req': req, 'q': q})
