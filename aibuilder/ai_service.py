"""خدمة توليد المواقع بالذكاء الاصطناعي"""
import os
import re
from django.conf import settings


def generate_website_code(user_prompt):
    """
    توليد كود HTML/CSS من Gemini API
    """
    api_key = getattr(settings, 'GEMINI_API_KEY', '') or os.environ.get('GEMINI_API_KEY', '')
    if not api_key:
        return None, 'مفتاح Gemini API غير مضبوط'

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        full_prompt = f'''أنت مطور ويب محترف. قم بإنشاء كود HTML و CSS كامل لصفحة هبوط احترافية بناءً على الوصف التالي:

"{user_prompt}"

المتطلبات:
- استخدم HTML5 و CSS3
- استخدم Tailwind CSS عبر CDN
- اجعل التصميم متجاوب (Responsive)
- استخدم خط Tajawal من Google Fonts
- اجعل الاتجاه RTL للعربية
- أخرج الكود فقط بدون أي شرح. ابدأ بـ <!DOCTYPE html>'''

        response = model.generate_content(full_prompt)
        code = response.text.strip()

        # نظّف الكود من علامات Markdown
        code = re.sub(r'^```html\s*', '', code)
        code = re.sub(r'^```\s*', '', code)
        code = re.sub(r'```\s*$', '', code)

        return code.strip(), None
    except ImportError:
        return None, 'مكتبة google-generativeai غير مثبتة'
    except Exception as e:
        return None, f'خطأ: {str(e)}'


def generate_website_code_simple(user_prompt):
    """
    نسخة تجريبية بدون API — تولّد صفحة بسيطة
    """
    code = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>موقعك المولّد</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap" rel="stylesheet">
<style>
body {{ font-family: 'Tajawal', sans-serif; }}
</style>
</head>
<body class="bg-gradient-to-br from-blue-500 to-purple-600 min-h-screen">
<div class="container mx-auto px-4 py-16 text-center text-white">
  <h1 class="text-5xl font-black mb-6">مرحباً بك</h1>
  <p class="text-xl mb-8 opacity-90">{user_prompt[:200]}</p>
  <a href="#" class="bg-white text-purple-600 px-8 py-3 rounded-full font-bold hover:bg-gray-100 transition inline-block">
    ابدأ الآن
  </a>
</div>
</body>
</html>'''
    return code, None
