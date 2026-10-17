import os
import json
import re
import requests
from bs4 import BeautifulSoup
from django.conf import settings
from openai import OpenAI

def scrape_competitor(url):
    if not url: return ""
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup.get_text(separator=' ', strip=True)[:2000]
    except Exception:
        return ""

def generate_website_code(prompt, color, font, style, competitor_text=""):
    # استخدام مفتاح DeepSeek
    api_key = os.environ.get('GROQ_API_KEY', '') or getattr(settings, 'GROQ_API_KEY', '')
    
    if not api_key:
        return None, 'مفتاح Groq API غير مضبوط. أضفه في settings.py'

    try:
        # DeepSeek متوافق مع OpenAI API
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )

        sys_prompt = f"""You are an elite web developer. Your task is to generate a 3-page website (index.html, about.html, contact.html).
You MUST strictly follow the user's request. Do NOT use generic SaaS landing page layouts.
If the user asks for a restaurant, build a restaurant. If they ask for a clinic, build a clinic.

Theme Rules:
- Primary Color: {color}
- Font: {font}
- Style: {style}
- Use this for images: <img src="https://picsum.photos/800/600?random=1">
- Include internal links between the 3 pages in the navigation.
- Use Tailwind CSS via CDN.

{f"Inspiration from competitor: {competitor_text}" if competitor_text else ""}

User Request: {prompt}

Return ONLY a valid JSON object without markdown blocks.
Example format:
{{
  "index.html": "<!DOCTYPE html><html>...</html>",
  "about.html": "<!DOCTYPE html><html>...</html>",
  "contact.html": "<!DOCTYPE html><html>...</html>"
}}"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": f"Please generate the website for: {prompt}"}
            ],
            response_format={"type": "json_object"}
        )
        
        text = response.choices[0].message.content.strip()
        text = re.sub(r'^```json\s*', '', text)
        text = re.sub(r'^```\s*', '', text)
        text = re.sub(r'```$', '', text)
        json.loads(text)
        return text, None
    except Exception as e:
        return None, f'DeepSeek Error: {str(e)}'

def inject_seo_tags(html_content, site_title, site_desc):
    seo_block = f"""
    <!-- SEO Auto-Generated -->
    <meta name="description" content="{site_desc[:160]}">
    <meta property="og:title" content="{site_title}">
    <meta property="og:description" content="{site_desc[:160]}">
    <!-- End SEO -->
    """
    if '</head>' in html_content:
        html_content = html_content.replace('</head>', seo_block + '</head>')
    return html_content

def apply_seo_to_pages(json_code, site_title="Nexora Website", site_desc="موقع احترافي مبني بواسطة Nexora"):
    try:
        pages = json.loads(json_code)
        for filename, html in pages.items():
            if filename.endswith('.html'):
                pages[filename] = inject_seo_tags(html, site_title, site_desc)
        return json.dumps(pages, ensure_ascii=False)
    except:
        return json_code
