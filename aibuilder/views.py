from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django_ratelimit.decorators import ratelimit
from .forms import WebsitePromptForm
from .models import GeneratedWebsite
from .ai_service import generate_website_code, generate_website_code_simple


@login_required
@ratelimit(key='user', rate='5/h', method='POST', block=True)
def generate_site_view(request):
    """صفحة توليد الموقع بالذكاء الاصطناعي"""
    if request.method == 'POST':
        form = WebsitePromptForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']

            # أنشئ السجل
            site = GeneratedWebsite.objects.create(
                user=request.user,
                prompt=prompt,
                status='pending',
            )

            # ولّد الكود
            code, error = generate_website_code(prompt)

            # إذا فشل، استخدم النسخة البسيطة
            if error:
                code, error = generate_website_code_simple(prompt)

            if code:
                site.generated_code = code
                site.status = 'completed'
                site.save()
                messages.success(request, '✅ تم توليد الموقع بنجاح!')
                return redirect('aibuilder:preview_site', site_id=site.id)
            else:
                site.status = 'failed'
                site.error_message = error or 'خطأ غير معروف'
                site.save()
                messages.error(request, f'❌ فشل التوليد: {error}')

    else:
        form = WebsitePromptForm()

    return render(request, 'aibuilder/generate_form.html', {'form': form})


@login_required
def preview_site_view(request, site_id):
    """معاينة الموقع المولّد"""
    site = get_object_or_404(GeneratedWebsite, id=site_id, user=request.user)
    return render(request, 'aibuilder/preview.html', {'site': site})


@login_required
def my_sites_view(request):
    """قائمة المواقع المولّدة"""
    sites = GeneratedWebsite.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'aibuilder/my_sites.html', {'sites': sites})
