from pathlib import Path
import os
import dj_database_url

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = 'django-insecure-7r@%=2n!8k$+1bmzjw6b@a$3xsmq&1'
DEBUG = False
ALLOWED_HOSTS = ['sploj.com', 'www.sploj.com', 'web-production-33eb.up.railway.app']

# Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'storages',
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

# URLs
ROOT_URLCONF = 'splojsite.urls'
WSGI_APPLICATION = 'splojsite.wsgi.application'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# Database (LOCAL DEVELOPMENT should use Railway PUBLIC URL)
DATABASES = {
    'default': dj_database_url.parse(
        'postgresql://postgres:cwmPLSkrTgRCQFTOGnIugKsnFBlkuprl@interchange.proxy.rlwy.net:39970/railway',
        conn_max_age=600,
        ssl_require=True,
    )
}

# Superuser (optional automation)
DJANGO_SUPERUSER_USERNAME = 'sploj-office'
DJANGO_SUPERUSER_EMAIL = 'admin@sploj.com'
DJANGO_SUPERUSER_PASSWORD = 'Machynlleth25!'

# Password validation
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
STATICFILES_DIRS = [BASE_DIR / 'main' / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Wasabi S3 Media Settings
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = 'B83PFQOU9FCYCVZGMZIY'
AWS_SECRET_ACCESS_KEY = '8TrYW21MzNcL3nkPpAaiwpDopvazvWtzVvRLHUu8'
AWS_STORAGE_BUCKET_NAME = 'sploj-media'
AWS_S3_ENDPOINT_URL = 'https://s3.eu-west-1.wasabisys.com'
AWS_S3_REGION_NAME = 'eu-west-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False  # Pre-signed URLs used in templates
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.eu-west-1.wasabisys.com/'

# Default PK type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security Headers
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    'https://sploj.com',
    'https://www.sploj.com',
    'https://web-production-33eb.up.railway.app',
]

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} | {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
