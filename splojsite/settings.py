from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv
from datetime import timedelta
import logging

# Load environment variables
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Security
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'your-secret-key')
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "sploj.com",
    "www.sploj.com",
    "web-production-33eb.up.railway.app",
]

# Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'cloudinary',
    'cloudinary_storage',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'splojsite.urls'

WSGI_APPLICATION = 'splojsite.wsgi.application'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Database
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:yourpassword@localhost:5432/yourdb')
DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        ssl_require=not DEBUG,
    )
}

# Superuser (for startup automation)
DJANGO_SUPERUSER_USERNAME = os.getenv('DJANGO_SUPERUSER_USERNAME', 'sploj-office')
DJANGO_SUPERUSER_EMAIL = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@sploj.com')
DJANGO_SUPERUSER_PASSWORD = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'Machynlleth25!')

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'main' / 'static' / 'custom',
    BASE_DIR / 'main' / 'static',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Media via Cloudinary
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dqmh99cik',
    'API_KEY': '669762426159988',
    'API_SECRET': 'pZa7ZQbOf7Y_Lbs6OSqZ8Zf7lxg',
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Security Headers
if DEBUG:
    SECURE_SSL_REDIRECT = False
    SECURE_PROXY_SSL_HEADER = None
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
else:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

X_FRAME_OPTIONS = 'DENY'

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "https://sploj.com",
    "https://www.sploj.com",
    "https://web-production-33eb.up.railway.app",
]

# CORS (optional for future)
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "https://sploj.com",
    "https://www.sploj.com",
]

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Default PK type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
