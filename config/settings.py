from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config('SECRET_KEY', default='change-me')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'aibuilder',
    'billing',
    'core',
    'projects',
    'requests_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3','NAME': BASE_DIR / 'db.sqlite3'}}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Asia/Beirut'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ========== i18n ==========
from django.utils.translation import gettext_lazy as _
LANGUAGES = [
    ('ar', _('العربية')),
    ('en', _('English')),
]
LOCALE_PATHS = [BASE_DIR / 'locale']
USE_I18N = True
USE_L10N = True

# للإنتاج استخدم SMTP:
# # # # # # ADMIN_EMAIL = config('ADMIN_EMAIL', default='admin@nexora.dev')

# ========== Telegram ==========
TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN', default='')
TELEGRAM_CHAT_ID = config('TELEGRAM_CHAT_ID', default='')

# ========== WhatsApp ==========
WHATSAPP_NUMBER = config('WHATSAPP_NUMBER', default='9610000000')

# ========== Recaptcha ==========
RECAPTCHA_SITE_KEY = config('RECAPTCHA_SITE_KEY', default='')
RECAPTCHA_SECRET_KEY = config('RECAPTCHA_SECRET_KEY', default='')

# ========== Sitemaps ==========

# ========== Jazzmin ==========

# ========== TinyMCE ==========
TINYMCE_DEFAULT_CONFIG = {
    'height': 500,
    'menubar': True,
    'plugins': 'advlist autolink lists link image charmap preview anchor searchreplace visualblocks code fullscreen insertdatetime media table help wordcount',
    'toolbar': 'undo redo | blocks | bold italic forecolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image media | removeformat | code fullscreen',
    'directionality': 'rtl',
    'language': 'ar',
    'content_style': "body { font-family: 'Tajawal', sans-serif; font-size: 16px; }",
}

# ========== Backup ==========
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': BASE_DIR / 'backups'}
import os
os.makedirs(BASE_DIR / 'backups', exist_ok=True)

# ========== Import Export ==========
IMPORT_EXPORT_USE_TRANSACTIONS = True

# ========== Simple History ==========
SIMPLE_HISTORY_HISTORY_CHANGE_REASON_USE_TEXT_FIELD = True

# Font Awesome للأدمن

# رابط Dashboard مخصص في القائمة

# CSS مخصص للأدمن

# ========== Whitnoise (static files) ==========
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ========== Rate Limiting ==========
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# ========== Tawk.to Live Chat ==========
TAWKTO_PROPERTY_ID = config('TAWKTO_PROPERTY_ID', default='')
TAWKTO_WIDGET_ID = config('TAWKTO_WIDGET_ID', default='default')

# ========== Analytics ==========
GOOGLE_ANALYTICS_ID = config('GOOGLE_ANALYTICS_ID', default='')
FACEBOOK_PIXEL_ID = config('FACEBOOK_PIXEL_ID', default='')
HOTJAR_ID = config('HOTJAR_ID', default='')

# ========== Site URL (للـ sitemap و og) ==========
SITE_URL = config('SITE_URL', default='http://127.0.0.1:8000')

# ========== SECURE (للإنتاج) ==========
# لما تنشر، فعّل هذي:
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# ========== PRODUCTION ==========
import os
import dj_database_url

# من .env أو من Environment Variables
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['*']

# ثقة بـ Render و Cloudflare
CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',
    'https://*.dpdns.org',
    'https://*.qzz.io',
    'https://webbuilder.dpdns.org',
]

# Security
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

# قاعدة البيانات
if not DEBUG:
    DATABASES = {
        'default': dj_database_url.config(
            default=config('DATABASE_URL', default='sqlite:///db.sqlite3'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
# ========== PRODUCTION SETTINGS for PythonAnywhere ==========
import os

DEBUG = False
ALLOWED_HOSTS = ['Mohamad15037.pythonanywhere.com']
CSRF_TRUSTED_ORIGINS = ['https://Mohamad15037.pythonanywhere.com']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ========== Authentication ==========

# ========== Allauth ==========

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

# ========== Phone Verify ==========

# ========== Email (Gmail SMTP) ==========
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'nexora.1lebanon@gmail.com'
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = 'Nexora <nexora.1lebanon@gmail.com>'
SERVER_EMAIL = 'nexora.1lebanon@gmail.com'

# ========== Allauth (new API) ==========

# ========== PRODUCTION (PythonAnywhere) ==========
import os
_env_host = os.environ.get('PYTHONANYWHERE_DOMAIN', '')
if _env_host:
    DEBUG = False
    ALLOWED_HOSTS = [_env_host, 'localhost', '127.0.0.1']
    CSRF_TRUSTED_ORIGINS = [f'https://{_env_host}']
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEBUG = False
ALLOWED_HOSTS = ['nexorastudiomakerwebandapps.pythonanywhere.com', 'localhost', '127.0.0.1']
CSRF_TRUSTED_ORIGINS = ['https://nexorastudiomakerwebandapps.pythonanywhere.com']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ================================================================
# SECURITY — Enhanced (auto-added)
# ================================================================

# Clickjacking
X_FRAME_OPTIONS = 'DENY'

# MIME sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# Referrer
SECURE_REFERRER_POLICY = 'same-origin'

# Password hashing — PBKDF2 (آمن ومتوافق مع PythonAnywhere)
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
]

# Proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
