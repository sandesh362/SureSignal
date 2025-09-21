@"
import os
import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Load configuration
CONFIG_PATH = BASE_DIR / 'config.yaml'
config = {}
if CONFIG_PATH.exists():
    with open(CONFIG_PATH, 'r') as f:
        config = yaml.safe_load(f)

SECRET_KEY = config.get('django', {}).get('secret_key', 'your-secret-key-here')
DEBUG = config.get('django', {}).get('debug', True)
ALLOWED_HOSTS = config.get('django', {}).get('allowed_hosts', ['localhost', '127.0.0.1'])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'core',
    'data_ingestion',  # This matches your 'ingestion' folder
    'text_processing',  # This matches your 'text processing' folder
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'misinformation_detector.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'misinformation_detector.wsgi.application'

# MongoDB Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': config.get('mongodb', {}).get('database', 'misinformation_db'),
        'CLIENT': {
            'host': config.get('mongodb', {}).get('connection_string', 'mongodb://localhost:27017'),
        }
    }
}

# API Configuration
TWITTER_CONFIG = config.get('twitter', {})
NEWSAPI_CONFIG = config.get('newsapi', {})

# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
"@ 
