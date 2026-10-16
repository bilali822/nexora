from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config('SECRET_KEY', default='change-me')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'jazzmin',
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'phone_verify',
    'phonenumber_field',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'import_export',
    'tinymce',
    'simple_history',
    'adminsortable2',
    'dbbackup',
    'widget_tweaks',
    'accounts',
    'billing',
    'core',
    'projects',
    'requests_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
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
JAZZMIN_SETTINGS = {
    "site_title": "Nexora Admin",
    "site_header": "Nexora",
    "site_brand": "Nexora — Web & Apps",
    "site_logo": None,
    "welcome_sign": "مرحباً بك في لوحة تحكم Nexora",
    "copyright": "Nexora © 2026",
    "search_model": ["auth.User", "requests_app.ProjectRequest"],
    "user_avatar": None,
    "topmenu_links": [
        {"name": "الرئيسية", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "الموقع", "url": "/", "new_window": True},
        {"model": "requests_app.ProjectRequest"},
        {"app": "core"},
    ],
    "usermenu_links": [
        {"name": "الموقع", "url": "/", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": [
        "requests_app", "core", "projects",
        "requests_app.ProjectRequest",
        "core.Service", "core.WhyUs", "core.ProcessStep", "core.Stat",
        "core.PricingPlan", "core.FAQ", "core.Testimonial", "core.Client",
        "core.BlogPost",
        "core.SiteSettings",
        "projects.Project",
        "auth",
    ],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "requests_app.ProjectRequest": "fas fa-inbox",
        "requests_app.ProjectAttachment": "fas fa-paperclip",
        "requests_app.PriceCalculator": "fas fa-calculator",
        "core.Service": "fas fa-concierge-bell",
        "core.WhyUs": "fas fa-star",
        "core.ProcessStep": "fas fa-list-ol",
        "core.Stat": "fas fa-chart-bar",
        "core.PricingPlan": "fas fa-tags",
        "core.PricingFeature": "fas fa-check",
        "core.FAQ": "fas fa-question-circle",
        "core.Testimonial": "fas fa-comment-dots",
        "core.Client": "fas fa-handshake",
        "core.BlogPost": "fas fa-newspaper",
        "core.ContactMessage": "fas fa-envelope",
        "core.SiteSettings": "fas fa-cog",
        "projects.Project": "fas fa-briefcase",
        "projects.ProjectImage": "fas fa-image",
        "projects.BeforeAfter": "fas fa-exchange-alt",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
        "core.SiteSettings": "single",
    },
    "language_chooser": True,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "darkly",
    "default_theme_mode": "dark",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}

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
JAZZMIN_SETTINGS["custom_css"] = None
JAZZMIN_SETTINGS["use_google_fonts_cdn"] = True

# رابط Dashboard مخصص في القائمة
JAZZMIN_SETTINGS["custom_links"] = {
    "الرئيسية المخصصة": [
        {
            "name": "لوحة التحكم",
            "url": "admin:index",
            "icon": "fas fa-tachometer-alt",
        },
    ],
}

# CSS مخصص للأدمن
JAZZMIN_SETTINGS["custom_css"] = "admin_custom/custom_admin.css"
JAZZMIN_SETTINGS["custom_js"] = "admin_custom/custom_admin.js"

# ========== Whitnoise (static files) ==========
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ========== Rate Limiting ==========
RATELIMIT_USE_CACHE = 'default'
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
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'accounts:profile'
LOGOUT_REDIRECT_URL = 'core:home'

# ========== Allauth ==========
SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_SESSION_REMEMBER = True
LOGIN_REDIRECT_URL = 'accounts:profile'
ACCOUNT_LOGOUT_REDIRECT_URL = 'core:home'
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[Nexora] '


# ========== Phone Verify ==========
PHONE_VERIFICATION = {
    'BACKEND': 'phone_verify.backends.twilio.TwilioBackend',
    'OPTIONS': {
        'SID': config('TWILIO_ACCOUNT_SID', default=''),
        'SECRET': config('TWILIO_AUTH_TOKEN', default=''),
        'FROM': config('TWILIO_PHONE_NUMBER', default='+1234567890'),
        'SANDBOX_TOKEN': '123456',
    },
    'TOKEN_LENGTH': 6,
    'MESSAGE': 'رمز التحقق من Nexora: {token}',
    'APP_NAME': 'Nexora',
    'SECURITY_CODE_EXPIRATION_TIME': 15,
}

# ========== Email (Gmail SMTP) ==========
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'nexora.1lebanon@gmail.com'
EMAIL_HOST_PASSWORD = 'qnbh fqfo iepq grsm'
DEFAULT_FROM_EMAIL = 'Nexora <nexora.1lebanon@gmail.com>'
SERVER_EMAIL = 'nexora.1lebanon@gmail.com'

# ========== Allauth (new API) ==========
ACCOUNT_LOGIN_METHODS = {'email', 'username'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']

# ========== PRODUCTION (PythonAnywhere) ==========
import os
_env_host = os.environ.get('PYTHONANYWHERE_DOMAIN', '')
if _env_host:
    DEBUG = False
    ALLOWED_HOSTS = [_env_host, 'localhost', '127.0.0.1']
    CSRF_TRUSTED_ORIGINS = [f'https://{_env_host}']
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
