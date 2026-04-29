"""
Configuration principale Django pour PronosPlatform (PRODUCTION READY)
"""

from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
from decouple import config, Csv
import dj_database_url
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────
def env_bool(value):
    """Convertit valeurs env en bool propre."""
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()

    if normalized in {'1', 'true', 'yes', 'on', 'debug', 'dev', 'development'}:
        return True
    if normalized in {'0', 'false', 'no', 'off', 'production', 'prod'}:
        return False

    raise ValueError(f"Invalid boolean value: {value}")


# ─────────────────────────────────────────────────────────────
# Sécurité
# ─────────────────────────────────────────────────────────────
DEBUG = config('DEBUG', default=True, cast=env_bool)

SECRET_KEY = config('SECRET_KEY', default=None)
if SECRET_KEY is None:
    if not DEBUG:
        raise ImproperlyConfigured("SECRET_KEY must be set in production.")
    SECRET_KEY = 'django-insecure-dev-only-change-me'

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='localhost,127.0.0.1',
    cast=Csv()
)

if not ALLOWED_HOSTS and not DEBUG:
    raise ImproperlyConfigured("ALLOWED_HOSTS cannot be empty in production.")


# ─────────────────────────────────────────────────────────────
# Applications
# ─────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',

    # Third-party
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'crispy_forms',
    'crispy_tailwind',
    'django_ckeditor_5',
    'taggit',
    'django_filters',
    'import_export',
    'drf_spectacular',

    # Apps locales
    'apps.accounts',
    'apps.pronostics',
    'apps.bookmakers',
    'apps.blog',
    'apps.vip',
    'apps.api',
]


# ─────────────────────────────────────────────────────────────
# Middleware
# ─────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'config.urls'
SITE_ID = 1


# ─────────────────────────────────────────────────────────────
# Templates
# ─────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.pronostics.context_processors.global_stats',
                'apps.vip.context_processors.vip_status',
            ],
        },
    },
]


WSGI_APPLICATION = 'config.wsgi.application'


# ─────────────────────────────────────────────────────────────
# Base de données
# ─────────────────────────────────────────────────────────────
DATABASES = {
    'default': dj_database_url.config(
        default=config(
            'DATABASE_URL',
            default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
        ),
        conn_max_age=600,
    )
}


# ─────────────────────────────────────────────────────────────
# Auth
# ─────────────────────────────────────────────────────────────
AUTH_USER_MODEL = 'accounts.User'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ─────────────────────────────────────────────────────────────
# Internationalisation
# ─────────────────────────────────────────────────────────────
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Porto-Novo'
USE_I18N = True
USE_TZ = True


# ─────────────────────────────────────────────────────────────
# Static & Media
# ─────────────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

WHITENOISE_AUTOREFRESH = DEBUG

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ─────────────────────────────────────────────────────────────
# Django REST Framework
# ─────────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}


# ─────────────────────────────────────────────────────────────
# JWT
# ─────────────────────────────────────────────────────────────
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
}


# ─────────────────────────────────────────────────────────────
# CORS / CSRF
# ─────────────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='',
    cast=Csv()
)

CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='',
    cast=Csv()
)


# ─────────────────────────────────────────────────────────────
# Crispy Forms
# ─────────────────────────────────────────────────────────────
CRISPY_ALLOWED_TEMPLATE_PACKS = 'tailwind'
CRISPY_TEMPLATE_PACK = 'tailwind'


# ─────────────────────────────────────────────────────────────
# CKEditor 5
# ─────────────────────────────────────────────────────────────
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading', '|',
            'bold', 'italic', 'underline', 'link', '|',
            'bulletedList', 'numberedList', 'blockQuote', '|',
            'insertTable', 'mediaEmbed', 'undo', 'redo',
        ],
        'language': 'fr',
        'height': 400,
    },
}


# ─────────────────────────────────────────────────────────────
# Email
# ─────────────────────────────────────────────────────────────
EMAIL_BACKEND = config(
    'EMAIL_BACKEND',
    default='django.core.mail.backends.console.EmailBackend'
)

EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = True

EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

DEFAULT_FROM_EMAIL = config(
    'DEFAULT_FROM_EMAIL',
    default='noreply@pronos-platform.com'
)


# ─────────────────────────────────────────────────────────────
# Sécurité production
# ─────────────────────────────────────────────────────────────
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True

    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    X_FRAME_OPTIONS = 'DENY'