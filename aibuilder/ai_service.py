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
        model = genai.GenerativeModel('gemini-1.5-flash')

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
