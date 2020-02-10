"""
Django settings for opendataserver project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import configparser
import os

from django.utils.translation import ugettext_lazy as _

config = configparser.RawConfigParser()
config.read_file(open('.env.cfg', encoding='utf-8'))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k=cd+br*i#v@n)0w%3m+a4n+-nhv%h-)2mhhor3!qsmm@vc&d6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bulma',
    'sass_processor',
    'accounts',
    'base',
    'data_sources.airrohr',
    'data_sources.ttn'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'base.middlewares.project.ProjectMiddleware'
]

ROOT_URLCONF = 'opendataserver.urls'

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
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'opendataserver.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# Password Hashing algorithms
# https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-PASSWORD_HASHERS

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# User model
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-user-model
AUTH_USER_MODEL = 'accounts.User'

#
AUTHENTICATION_BACKEND = [
    'accounts.EmailAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend'
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Locale Paths
# https://docs.djangoproject.com/en/3.0/ref/settings/#locale-paths
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGES = (
    ('en', _('English')),
    ('de', _('German')),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]
SASS_PROCESSOR_ROOT = os.path.join(BASE_DIR, 'static')

# Mail Settings
# https://docs.djangoproject.com/en/3.0/ref/settings/#email-host
DEFAULT_FROM_EMAIL = config.get('mail', 'from', fallback='opendataserver@localhost')
EMAIL_PORT = config.getint('mail', 'port', fallback=25)
EMAIL_HOST_USER = config.get('mail', 'user', fallback='')
EMAIL_HOST_PASSWORD = config.get('mail', 'password', fallback='')
EMAIL_HOST = config.get('mail', 'host', fallback='localhost')
EMAIL_USE_TLS = config.getboolean('mail', 'tls', fallback=False)
EMAIL_USE_SSL = config.getboolean('mail', 'ssl', fallback=False)
EMAIL_SUBJECT_PREFIX = '[OpenDataServer] '

# Celery
CELERY_BROKER_URL = config.get('celery', 'broker_url')
CELERY_RESULT_BACKEND = config.get('celery', 'result_backend')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
# CELERY_BEAT_SCHEDULE = {}

# InfluxDB
INFLUXDB_HOST = config.get('influxdb', 'host', fallback='localhost')
INFLUXDB_PORT = config.getint('influxdb', 'port', fallback=8086)
INFLUXDB_USERNAME = config.get('influxdb', 'username', fallback='root')
INFLUXDB_PASSWORD = config.get('influxdb', 'password', fallback='root')
INFLUXDB_DATABASE = config.get('influxdb', 'database', fallback='opendataserver')
INFLUXDB_SSL = config.getboolean('influxdb', 'ssl', fallback=False)
INFLUXDB_VERIFY_SSL = config.getboolean('influxdb', 'verify_ssl', fallback=False)
INFLUXDB_REPLICATION_FACTOR = config.getint('influxdb', 'replication_factor', fallback=1)
