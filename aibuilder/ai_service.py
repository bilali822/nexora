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
    api_key = os.environ.get('GROQ_API_KEY', '') or getattr(settings, 'GROQ_API_KEY', '')
    
    if not api_key or 'ضع' in api_key:
        return None, 'مفتاح Groq API غير مضبوط. أضفه في settings.py'

    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )

        # 1. تحديد نمط التصميم بدقة
        style_guide = ""
        if style == 'cyberpunk':
            style_guide = "bg-black text-cyan-400 font-mono, neon borders (border-fuchsia-500 shadow-[0_0_15px_#ff00ff]), uppercase headings."
        elif style == 'modern':
            style_guide = "bg-gray-50 text-gray-900 rounded-3xl, soft shadows (shadow-xl), clean sans-serif, generous spacing."
        elif style == 'minimal':
            style_guide = "bg-white text-black, stark black borders (border-2 border-black), no shadows, sharp edges."
        elif style == 'luxury':
            style_guide = "bg-neutral-950 text-amber-500 font-serif, thin gold borders (border-amber-500/30), elegant letter-spacing."
        
        # 2. إجبار الذكاء الاصطناعي على استخدام هذه الروابط الثابتة
        image_guide = """
        - Hero/Background Image: Use EXACTLY <img src="https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?auto=format&fit=crop&w=1600&q=80" class="absolute inset-0 w-full h-full object-cover opacity-40"> inside a relative container.
        - Food/Products Image: Use EXACTLY <img src="https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=800&q=80" class="w-full h-56 object-cover rounded-t-2xl">
        - Interior/Office Image: Use EXACTLY <img src="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=80" class="w-full h-56 object-cover rounded-t-2xl">
        - Team/Chef Image: Use EXACTLY <img src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=800&q=80" class="w-full h-56 object-cover rounded-t-2xl">
        """

        sys_prompt = f"""You are an ELITE Senior Frontend Developer and UI/UX Designer.
Generate a 3-page website (index.html, about.html, contact.html).
User Request: {prompt}

Theme & Design Rules:
- Primary Color: {color}
- Style: {style}
- Font: {font}
- Tailwind CSS via CDN.

DESIGN SYSTEM:
{style_guide}

MANDATORY IMAGES (DO NOT INVENT URLs - COPY EXACTLY):
{image_guide}

FONTS (MANDATORY):
<link href="https://fonts.googleapis.com/css2?family={font}:wght@400;700;900&display=swap" rel="stylesheet">
<style>body {{ font-family: '{font}', sans-serif; }}</style>

STRUCTURE (MANDATORY):
- Hero: Use a split layout with a glassmorphism card OR a background image with dark overlay.
- Cards: Use CSS Grid (grid-cols-1 md:grid-cols-3) with gap-8 and p-8.
- FORMS: Modern inputs with proper spacing.

Return ONLY a valid JSON object without markdown blocks.
Example:
{{
  "index.html": "<!DOCTYPE html><html>...</html>",
  "about.html": "<!DOCTYPE html><html>...</html>",
  "contact.html": "<!DOCTYPE html><html>...</html>"
}}"""

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": f"Generate the website for: {prompt}"}
            ],
            response_format={"type": "json_object"},
            max_tokens=8000,
            temperature=0.6
        )
        
        text = response.choices[0].message.content.strip()
        text = re.sub(r'^```json\s*', '', text)
        text = re.sub(r'^```\s*', '', text)
        text = re.sub(r'```$', '', text)
        
        json.loads(text)
        return text, None
    except Exception as e:
        return None, f'Groq API Error: {str(e)}'

def inject_seo_tags(html_content, site_title, site_desc):
    seo_block = f"""<meta name="description" content="{site_desc[:160]}"><meta property="og:title" content="{site_title}"><meta property="og:description" content="{site_desc[:160]}">"""
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
