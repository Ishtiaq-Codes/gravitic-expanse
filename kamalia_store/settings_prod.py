"""
Production settings for kamalia_store project.
Uses environment variables for sensitive configuration.

Usage: DJANGO_SETTINGS_MODULE=kamalia_store.settings_prod

Required environment variables (.env file):
  SECRET_KEY=your-secret-key-here
  ALLOWED_HOSTS=your-ec2-ip,your-domain.com

Optional environment variables:
  USE_SQLITE=true   (default: true — uses SQLite on EC2)
  DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT  (only needed for PostgreSQL)
"""

from .settings import *
from decouple import config

# ─── Core ────────────────────────────────────────────────────────────────────

DEBUG = False

SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# ─── Middleware (WhiteNoise must be 2nd, right after SecurityMiddleware) ──────

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',        # ← serves static files fast
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ─── Database ─────────────────────────────────────────────────────────────────
# Defaults to SQLite (easy EC2 deploy). Set USE_SQLITE=false to use PostgreSQL.

USE_SQLITE = config('USE_SQLITE', default='true').lower() == 'true'

if USE_SQLITE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
            'OPTIONS': {
                'timeout': 20,  # wait up to 20s on locked DB (concurrent requests)
            }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='kamalia_store'),
            'USER': config('DB_USER', default='postgres'),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }

# ─── Static Files (WhiteNoise handles serving + compression) ─────────────────

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# ─── CSRF / Trusted Origins ───────────────────────────────────────────────────
# Add your EC2 IP and domain here so forms (login, cart, checkout) work

CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default=''
).split(',') if config('CSRF_TRUSTED_ORIGINS', default='') else []

# Always include a fallback from ALLOWED_HOSTS
CSRF_TRUSTED_ORIGINS += [
    f'http://{host}' for host in ALLOWED_HOSTS if host
] + [
    f'https://{host}' for host in ALLOWED_HOSTS if host
]

# ─── Security ─────────────────────────────────────────────────────────────────
# SSL settings are OFF by default — enable only after you add HTTPS/SSL cert

SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default='false').lower() == 'true'
SESSION_COOKIE_SECURE = config('SECURE_SSL_REDIRECT', default='false').lower() == 'true'
CSRF_COOKIE_SECURE = config('SECURE_SSL_REDIRECT', default='false').lower() == 'true'

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS — only enable after SSL is working
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# ─── Logging ──────────────────────────────────────────────────────────────────

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}
