"""
Django settings for massenergize_portal_backend project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from .utils.utils import load_json

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DATA = load_json(BASE_DIR + '/_main_/config2.json')


os.environ["DATABASE_ENGINE"] = CONFIG_DATA["DATABASE_ENGINE"]
os.environ["DATABASE_NAME"] =  CONFIG_DATA["DATABASE_NAME"]
os.environ["DATABASE_USER"] = CONFIG_DATA["DATABASE_USER"]
os.environ["DATABASE_PASSWORD"] = CONFIG_DATA["DATABASE_PASSWORD"]
os.environ["DATABASE_HOST"] =  CONFIG_DATA["DATABASE_HOST"]
os.environ["DATABASE_PORT"] = CONFIG_DATA["DATABASE_PORT"]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY =  CONFIG_DATA["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*'] #TODO: restrict this when ready to deploy

# Application definition

INSTALLED_APPS = [
    'admin_portal',
    'carbon_calculator',
    'database',
    'user_portal',
    'website',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -------- CORS CONFIGURATION ---------------#
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

CORS_ORIGIN_WHITELIST = [
    "https://massenergize.org",
    "http://massenergize.org",
    "https://energizewayland.org",
    "https://energizewayland.org",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001"
]
CORS_ORIGIN_REGEX_WHITELIST = [
    r"^https://\w+\.massenergize\.org$",
    r"^https://\w+\.massenergize\.com$",
    r"^https://\w+\.energizewayland\.org$",
    r"^http://\w+\.massenergize\.org$",
    r"^http://\w+\.massenergize\.com$",
    r"^http://\w+\.energizewayland\.org$",
]
# -------- END CORS CONFIGURATION ---------------#

CSRF_TRUSTED_ORIGINS = [
    '.massenergize.org',
    '.energizewayland.org'
    'http://localhost:3001',
    'http://localhost:3000'
]


#-------- AWS CONFIGURATION ---------------------#
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = CONFIG_DATA['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = CONFIG_DATA['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = CONFIG_DATA['AWS_STORAGE_BUCKET_NAME']
S3_USE_SIGV4 = True
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_REGION_NAME = 'us-east-2'
AWS_DEFAULT_ACL  = None
#--------END AWS CONFIGURATION ---------------------#


ROOT_URLCONF = '_main_.urls'


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

WSGI_APPLICATION = '_main_.wsgi.application'

CSRF_COOKIE_NAME = 'csrfToken'
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_ENGINE'),
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT')
    },
    'test': {
        'ENGINE': os.environ.get('DATABASE_ENGINE'),
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': ''
    },
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'


# Simplified static file serving.
STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'