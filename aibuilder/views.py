import json
import zipfile
import io
import base64
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .models import GeneratedWebsite
from .forms import WebsitePromptForm, EditWithAIForm, GitHubDeployForm
from .ai_service import generate_website_code, scrape_competitor, apply_seo_to_pages
from .models import GeneratedWebsite, SiteVersion

@login_required
def generate_site_view(request):
    if request.method == 'POST':
        form = WebsitePromptForm(request.POST)
        if form.is_valid():
            site = form.save(commit=False)
            site.user = request.user
            site.status = 'pending'
            
            competitor_text = scrape_competitor(site.competitor_url)
            
            code, error = generate_website_code(
                site.prompt, site.theme_color, site.theme_font, site.theme_style, competitor_text
            )

            if error or not code:
                messages.error(request, f'❌ فشل التوليد: {error}')
                site.status = 'failed'
                site.error_message = str(error)
                site.save()
                return redirect('aibuilder:generate')
            else:
                code = apply_seo_to_pages(code, site.prompt[:50])
                site.generated_code = code
                site.status = 'completed'
            
            site.save()
            return redirect('aibuilder:preview_site', site_id=site.id)
    else:
        form = WebsitePromptForm()
    return render(request, 'aibuilder/generate_form.html', {'form': form})

@login_required
def preview_site_view(request, site_id):
    site = get_object_or_404(GeneratedWebsite, id=site_id, user=request.user)
    try:
        pages = json.loads(site.generated_code)
        index_html = pages.get('index.html', '')
    except:
        index_html = site.generated_code or ''
        
    return render(request, 'aibuilder/preview.html', {'site': site, 'index_html': index_html, 'versions': site.versions.all()[:10]})

@login_required
def export_zip(request, site_id):
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
            import google.generativeai as genai
            genai.configure(api_key=getattr(settings, 'GEMINI_API_KEY', ''))
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # حفظ نسخة احتياطية قبل التعديل
            SiteVersion.objects.create(
                site=site,
                code_snapshot=site.generated_code,
                instruction_applied=instruction[:250]
            )

            prompt = f"Here is the current JSON of website pages:\n{site.generated_code}\n\nApply this modification to the code: {instruction}\nReturn ONLY updated valid JSON."
            res = model.generate_content(prompt)
            text = res.text.strip().replace('```json', '').replace('```', '')
            
            site.generated_code = text
            site.save()
            messages.success(request, '✅ تم التعديل بنجاح (تم حفظ نسخة سابقة)')
        except Exception as e:
            messages.error(request, f'❌ فشل التعديل: {e}')
            
    return redirect('aibuilder:preview_site', site_id=site.id)

@login_required
@require_POST
def deploy_github(request, site_id):
    site = get_object_or_404(GeneratedWebsite, id=site_id, user=request.user)
    form = GitHubDeployForm(request.POST)
    if form.is_valid():
        token = form.cleaned_data['github_token']
        repo = form.cleaned_data['repo_name']
        headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}
        
        # 1. Create Repo
        r = requests.post('https://api.github.com/user/repos', json={'name': repo, 'auto_init': False}, headers=headers)
        if r.status_code not in [201, 422]:
            messages.error(request, 'فشل إنشاء المستودع. تحقق من التوكن.')
            return redirect('aibuilder:preview_site', site_id=site.id)
            
        user_login = requests.get('https://api.github.com/user', headers=headers).json()['login']
        
        # 2. Upload Files
        try:
            pages = json.loads(site.generated_code)
            for filename, content in pages.items():
                encoded_content = base64.b64encode(content.encode()).decode()
                data = {'message': f'Add {filename}', 'content': encoded_content}
                requests.put(f'https://api.github.com/repos/{user_login}/{repo}/contents/{filename}', json=data, headers=headers)
                
            site.github_repo_url = f'https://{user_login}.github.io/{repo}/'
            site.is_published = True
            site.status = 'published'
            site.save()
            messages.success(request, f'✅ تم النشر! رابطك: {site.github_repo_url}')
        except Exception as e:
            messages.error(request, f'❌ فشل الرفع: {e}')
            
    return redirect('aibuilder:preview_site', site_id=site.id)


@login_required
@require_POST
def rollback_version(request, site_id, version_id):
    site = get_object_or_404(GeneratedWebsite, id=site_id, user=request.user)
    version = get_object_or_404(SiteVersion, id=version_id, site=site)
    
    # احفظ الحالة الحالية في نسخة جديدة قبل التراجع
    SiteVersion.objects.create(
        site=site,
        code_snapshot=site.generated_code,
        instruction_applied='Auto-save before rollback'
    )
    
    site.generated_code = version.code_snapshot
    site.save()
    messages.success(request, f'✅ تم التراجع للنسخة #{version_id}')
    return redirect('aibuilder:preview_site', site_id=site.id)
