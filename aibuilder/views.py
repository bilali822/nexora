from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import WebsitePromptForm
from .models import GeneratedWebsite
from .ai_service import generate_website_code
from .designs import TEMPLATES


@login_required
def generate_site_view(request):
    if request.method == 'POST':
        form = WebsitePromptForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            template_key = request.POST.get('template', '')

            site = GeneratedWebsite.objects.create(
                user=request.user,
                prompt=prompt,
                status='pending',
            )

            code, error = generate_website_code(prompt, template_key)

            if code:
                site.generated_code = code
                site.status = 'completed'
                site.save()
                messages.success(request, '✅ تم توليد الموقع بنجاح!')
                return redirect('aibuilder:preview_site', site_id=site.id)
            else:
                site.status = 'failed'
                site.error_message = error or 'خطأ'
                site.save()
                messages.error(request, f'❌ فشل: {error}')

    else:
        form = WebsitePromptForm()

    return render(request, 'aibuilder/generate_form.html', {
        'form': form,
        'templates': TEMPLATES,
    })


@login_required
def preview_site_view(request, site_id):
    site = get_object_or_404(GeneratedWebsite, id=site_id, user=request.user)
    return render(request, 'aibuilder/preview.html', {'site': site})


@login_required
def my_sites_view(request):
    sites = GeneratedWebsite.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'aibuilder/my_sites.html', {'sites': sites})
