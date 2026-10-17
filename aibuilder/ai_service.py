import os
import json
import re
import requests
from bs4 import BeautifulSoup
from django.conf import settings

def scrape_competitor(url):
    if not url: return ""
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup.get_text(separator=' ', strip=True)[:2000]
    except Exception:
        return ""

def generate_website_code(prompt, color, font, style, competitor_text=""):
    api_key = getattr(settings, 'GEMINI_API_KEY', '') or os.environ.get('GEMINI_API_KEY', '')
    if not api_key:
        return None, 'مفتاح Gemini API غير مضبوط'

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

        sys_prompt = f"""You are an expert web developer. Generate a 3-page website.
Theme: Color {color}, Font {font}, Style {style}.
Use AI images by formatting as: <img src="https://image.pollinations.ai/prompt/[ENGLISH_PROMPT]?width=800&height=600">
{"Inspiration from competitor: " + competitor_text if competitor_text else ""}

User Request: {prompt}

Return ONLY a valid JSON object without markdown blocks, mapping filenames to HTML strings.
Example:
{{
  "index.html": "<!DOCTYPE html><html>...</html>",
  "about.html": "<!DOCTYPE html><html>...</html>",
  "contact.html": "<!DOCTYPE html><html>...</html>"
}}"""

        response = model.generate_content(sys_prompt)
        text = response.text.strip()
        
        # Clean markdown
        text = re.sub(r'^```json\s*', '', text)
        text = re.sub(r'^```\s*', '', text)
        text = re.sub(r'```$', '', text)
        
        return text, None
    except Exception as e:
        return None, str(e)


def inject_seo_tags(html_content, site_title, site_desc):
    """حقن الـ SEO Tags في الـ HTML المولد تلقائياً"""
    import re
    from datetime import datetime
    
    seo_block = f"""
    <!-- SEO Auto-Generated -->
    <meta name="description" content="{site_desc[:160]}">
    <meta name="keywords" content="web design, development, Nexora, {site_title}">
    <meta name="author" content="Nexora">
    <meta name="robots" content="index, follow">
    
    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="{site_title}">
    <meta property="og:description" content="{site_desc[:160]}">
    <meta property="og:site_name" content="{site_title}">
    <meta property="og:locale" content="ar_LB">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{site_title}">
    <meta name="twitter:description" content="{site_desc[:160]}">
    
    <!-- Schema.org -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "{site_title}",
      "description": "{site_desc[:160]}",
      "publisher": {{"@type": "Organization", "name": "Nexora"}}
    }}
    </script>
    <!-- End SEO -->
    """

    # حقن قبل </head>
    if '</head>' in html_content:
        html_content = html_content.replace('</head>', seo_block + '</head>')
    return html_content

def apply_seo_to_pages(json_code, site_title="Nexora Website", site_desc="موقع احترافي مبني بواسطة Nexora"):
    import json
    try:
        pages = json.loads(json_code)
        for filename, html in pages.items():
            if filename.endswith('.html'):
                pages[filename] = inject_seo_tags(html, site_title, site_desc)
        return json.dumps(pages)
    except:
        return json_code
