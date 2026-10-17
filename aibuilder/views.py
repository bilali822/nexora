import json
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .models import GeneratedWebsite
from .forms import WebsitePromptForm, EditWithAIForm
from .ai_service import generate_website_code, scrape_competitor, apply_seo_to_pages

# ================================================================
# PUBLISH TO HERE.NOW (FIXED)
# ================================================================
def publish_to_here_now(html_content):
    try:
        # 1. إنشاء عملية نشر
        create_payload = {
            "files": [{"path": "index.html", "size": len(html_content.encode('utf-8')), "contentType": "text/html"}]
        }
        create_res = requests.post('https://here.now/api/v1/publish', json=create_payload, timeout=10)
        create_data = create_res.json()
        
        if 'upload' not in create_data:
            raise Exception(f"API Error: {create_data}")

        upload_url = create_data['upload']['uploads'][0]['url']
        slug = create_data.get('slug')
        version_id = create_data['upload'].get('versionId')

        # 2. رفع الملف
        put_res = requests.put(upload_url, data=html_content.encode('utf-8'), headers={'Content-Type': 'text/html'}, timeout=10)
        if put_res.status_code not in [200, 201]:
            raise Exception(f"Upload failed: {put_res.status_code}")

        # 3. إنهاء النشر
        finalize_url = create_data['upload'].get('finalizeUrl') or f'https://here.now/api/v1/publish/{slug}/finalize'
        finalize_payload = {'versionId': version_id} if version_id else {}
        fin_res = requests.post(finalize_url, json=finalize_payload, timeout=10)
        
        if fin_res.status_code != 200:
            raise Exception(f"Finalize failed: {fin_res.text}")

        return create_data.get('siteUrl')
    except Exception as e:
        raise Exception(str(e))

# ================================================================
# VIEWS
# ================================================================
@login_required
def generate_site_view(request):
    if request.method == 'POST':
        form = WebsitePromptForm(request.POST)
        if form.is_valid():
            site = form.save(commit=False)
            site.user = request.user
            site.status = 'pending'
            
            competitor_text = scrape_competitor(site.competitor_url)
            code, error = generate_website_code(site.prompt, site.theme_color, site.theme_font, site.theme_style, competitor_text)

            if error or not code:
                messages.error(request, f'❌ فشل التوليد: {error}')
                site.status = 'failed'
                site.error_message = str(error)
                site.save()
                return redirect('aibuilder:generate')
            
            code = apply_seo_to_pages(code, site.prompt[:50])
            site.generated_code = code
            site.status = 'completed'
            site.save()
            return redirect('aibuilder:preview_site', site_id=site.id)
    else:
        form = WebsitePromptForm()
    return render(request, 'aibuilder/generate_form.html', {'form': form})

@login_required
def fullscreen_preview(request, site_id):
    site = get_object_or_404(GeneratedWebsite, id=site_id, user=request.user)
    try:
        pages = json.loads(site.generated_code)
        index_html = pages.get('index.html', '')
    except:
        index_html = site.generated_code or ''
    return render(request, 'aibuilder/fullscreen_preview.html', {'site': site, 'index_html': index_html})

@login_required
def manage_site(request, site_id):
    site = get_object_or_404(GeneratedWebsite, id=site_id, user=request.user)
    try:
        pages = json.loads(site.generated_code)
        index_html = pages.get('index.html', '')
    except:
        index_html = site.generated_code or ''
    return render(request, 'aibuilder/manage.html', {'site': site, 'index_html': index_html, 'versions': site.versions.all()[:10]})

@login_required
@require_POST
def publish_here_now(request, site_id):
    site = get_object_or_404(GeneratedWebsite, id=site_id, user=request.user)
    try:
        pages = json.loads(site.generated_code)
        html = pages.get('index.html', '')
    except:
        html = site.generated_code or ''

    if not html:
        messages.error(request, 'لا يوجد كود للنشره.')
        return redirect('aibuilder:manage_site', site_id=site.id)

    try:
        url = publish_to_here_now(html)
        site.published_url = url
        site.is_published = True
        site.status = 'published'
        site.save()
        messages.success(request, f'✅ تم النشر بنجاح! الرابط: {url}')
    except Exception as e:
        messages.error(request, f'❌ فشل النشر: {e}')

    return redirect('aibuilder:manage_site', site_id=site.id)

@login_required
def export_zip(request, site_id):
    import zipfile, io
    site = get_object_or_404(GeneratedWebsite, id=site_id, user=request.user)
    try:
        pages = json.loads(site.generated_code)
    except:
        pages = {"index.html": site.generated_code or ""}
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filename, content in pages.items():
            zip_file.writestr(filename, content)
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="site_{site.id}.zip"'
    return response

@login_required
@require_POST
def edit_with_ai(request, site_id):
    site = get_object_or_404(GeneratedWebsite, id=site_id, user=request.user)
    form = EditWithAIForm(request.POST)
    if form.is_valid():
        instruction = form.cleaned_data['instruction']
        try:
            from openai import OpenAI
            import os
            from django.conf import settings as st
            client = OpenAI(api_key=os.environ.get('GROQ_API_KEY','') or getattr(st,'GROQ_API_KEY',''), base_url="https://api.groq.com/openai/v1")
            prompt = f"Here is the current JSON of website pages:\n{site.generated_code}\n\nApply this modification: {instruction}\nReturn ONLY updated valid JSON."
            res = client.chat.completions.create(model="openai/gpt-oss-120b", messages=[{"role":"user","content":prompt}], response_format={"type":"json_object"}, max_tokens=8000)
            text = res.choices[0].message.content.strip()
            site.generated_code = text
            site.save()
            messages.success(request, '✅ تم التعديل بنجاح')
        except Exception as e:
            messages.error(request, f'❌ فشل التعديل: {e}')
    return redirect('aibuilder:manage_site', site_id=site.id)
