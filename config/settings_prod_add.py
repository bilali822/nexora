# ========== PRODUCTION SETTINGS for PythonAnywhere ==========
import os

DEBUG = False
ALLOWED_HOSTS = ['Mohamad15037.pythonanywhere.com']
CSRF_TRUSTED_ORIGINS = ['https://Mohamad15037.pythonanywhere.com']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
