"""
Django settings for monitoring project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
#import django_processinfo

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-h(tj$%876#l(ci!)v9af79tk40(ens$*948af4=#%aww)^ae&u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
MY_DEBUG = False
DOMAIN_PATH = 'sys-monitoring.kz'

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'django_tables2',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'storage_drive',
    'dashboard_authentication',
    'dashboard',
    'dashboard_api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.locale.LocaleMiddleware'
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'monitoring.urls'

LOGOUT_REDIRECT_URL = "dashboard:index"
LOGIN_URL = 'dashboard_auth:login'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'dashboard.context_processors.default_context',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'monitoring.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'kk'

TIME_ZONE = 'Asia/Almaty'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

#MY

STATIC_ROOT =  f'/home/{DOMAIN_PATH}/public_html/static'
MEDIA_ROOT = f'/home/{DOMAIN_PATH}/public_html/media'
if MY_DEBUG:
    STATIC_ROOT =  os.path.join(BASE_DIR, 'static') 
    MEDIA_ROOT =  os.path.join(BASE_DIR, 'media') 

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'dashboard.CustomUser'
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
REST_FRAMEWORK = {
    'DATETIME_FORMAT': "%m/%d/%Y %I:%M%P",
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

# SIMPLE_JWT = {
#      'ACCESS_TOKEN_LIFETIME': time.timedelta(minutes=10),
#      'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
#     #  'ROTATE_REFRESH_TOKENS': True,
#     #  'BLACKLIST_AFTER_ROTATION': True
# }

if MY_DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'filters': ['require_debug_true'],
            },
        },
        'loggers': {
            'mylogger': {
                'handlers': ['console'],
                'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
                'propagate': True,
            },
        },
    }

# from django_processinfo import app_settings as PROCESSINFO
# django_processinfo.ADD_INFO = True

from django.utils.translation import gettext_lazy as _

LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
    ('kk', _('Kazakh')),
)
# LANGUAGES = [
#     ('kk', 'Kazakh'),
#     ('en', 'English'),
# ]

# # Specify the custom names for the languages
# LANGUAGE_CUSTOM_NAMES = {
#     'kk': 'Қазақша',  # Custom name for Kazakh
#     'en': 'English',  # Custom name for English
# }


LOCALE_PATHS = [
    BASE_DIR / 'locale/',
    
]