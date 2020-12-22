import os

from django.contrib.messages import constants as messages
from django.urls import reverse_lazy


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path of the directory containing apps
APPS_DIR = os.path.join(BASE_DIR, 'cloudstore/apps')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'cloudstore')

DEBUG = int(os.environ.get('DEBUG', default=0))

# 'DJANGO_ALLOWED_HOSTS' should be a single string of hosts with a space between each.
# For example: 'DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]'
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost 127.0.0.1 [::1]').split(' ')

# Application definition
INSTALLED_APPS = [
    'django_simple_bulma',
    'rest_framework',
    'rest_framework.authtoken',
    'private_storage',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudstore.apps.cloudstore',
    'cloudstore.apps.api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_simple_bulma.finders.SimpleBulmaFinder',
]

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'cloudstore/static'),
]

ROOT_URLCONF = 'cloudstore.urls'

# Default user model
AUTH_USER_MODEL = 'cloudstore.CloudstoreUser'

# Used when deciding whether to generate thumbnails
IMAGE_THUMBNAIL_TYPES = ['JPEG', 'GIF', 'PNG', 'BMP', 'WEBP']
IMAGE_THUMBNAIL_SIZE = (256, 256)

# We are proxied behind nginx
if not DEBUG:
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Root directory of all user files stored by the app
PRIVATE_STORAGE_ROOT = os.environ.get('FILE_STORAGE_DIR')

PRIVATE_STORAGE_AUTH_FUNCTION = 'cloudstore.apps.cloudstore.permissions.if_shared'

if DEBUG:
    PRIVATE_STORAGE_SERVER = 'private_storage.servers.DjangoServer'
else:
    PRIVATE_STORAGE_SERVER = 'private_storage.servers.NginxXAccelRedirectServer'
    PRIVATE_STORAGE_INTERNAL_URL = '/private-x-accel-redirect/'

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'cloudstore/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'cloudstore.context_processors.debug',
            ],
        },
    },
]

# WSGI app for development
WSGI_APPLICATION = 'cloudstore.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('SQL_DATABASE', os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': os.environ.get('SQL_USER', 'user'),
        'PASSWORD': os.environ.get('SQL_PASSWORD', 'password'),
        'HOST': os.environ.get('SQL_HOST', 'localhost'),
        'PORT': os.environ.get('SQL_PORT', '5432'),
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

# Django Rest Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ]
}

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Copenhagen'
USE_I18N = False
USE_L10N = True
USE_TZ = True

# Email config
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', True)
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', False)

# Don't add a slash to the end of requests
# APPEND_SLASH = False

# Redirct to home when logged in
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = reverse_lazy('cloudstore:login')

# Configure messages to use Bulma classes
MESSAGE_TAGS = {
    messages.DEBUG: 'is-light',
    messages.INFO: 'is-info',
    messages.SUCCESS: 'is-success',
    messages.WARNING: 'is-warning',
    messages.ERROR: 'is-danger',
}

# Custom settings for django-simple-bulma, primarily colors
BULMA_SETTINGS = {
    'output_style': 'compressed',
    'fontawesome_token': os.environ.get('FONTAWESOME', ''),
    'extensions': [
        'bulma-checkradio',
        'bulma-divider',
        'bulma-dropdown',
        'bulma-tooltip',
    ],
    'custom_scss': {
        # 'cloudstore/static/css/base.scss',
    },
    'variables': {
        'primary': '#CC174F',
        'white': 'hsl(0, 0%, 100%)',
        'white-bis': 'hsl(0, 0%, 98%)',
        'white-ter': 'hsl(0, 0%, 96%)',
        'black': 'hsl(0, 0%, 4%)',
        'black-bis': 'hsl(0, 0%, 7%)',
        'black-ter': 'hsl(0, 0%, 10%)',
        'dark': '#232022',
        'dark-bis': '#2B272A',
        'dark-ter': '#363134',
        'scheme-main': '$dark',
        'scheme-main-bis': '$dark-bis',
        'scheme-main-ter': '$dark-ter',
        'scheme-invert': '$black',
        'scheme-invert-bis': '$black-bis',
        'scheme-invert-ter': '$black-ter',
        'background': '$dark-bis',
        'progress-bar-background-color': '$dark',
        'panel-item-border': '1px solid $dark-bis',
        'grey-lighter': 'hsl(0, 0%, 86%)',
        'grey-lightest': 'hsl(0, 0%, 93%)',
        'red': '#CC1E1E',
        'green': '#3FB067',
        'text': '$grey-lighter',
        'text-light': '$grey-lightest',
        'text-strong': '$grey-lightest',
        'dropdown-item-hover-color': '$text-strong',
        'link': '$primary',
        'link-visited': '#CF3670',
        'link-hover': 'darken($link, 5%)',
        'link-active': '$link-hover',
        'link-focus': '$link-hover',
        'button-hover-border-color': '$link-hover',
        'button-focus-border-color': '$button-hover-border-color',
        'button-active-border-color': '$button-hover-border-color',
        'table-cell-border': '1px solid $dark-ter',
        'navbar-dropdown-item-hover-color': '$white',
        'modal-background-background-color': 'rgba($scheme-invert, 0.5)',
        'divider-background-color': '$dark-ter',
        'divider-thickness': '2px',
        'divider-font-size': '1rem',
        'divider-color': '$dark-ter',
        'footer-padding': '1rem 1.5rem 1rem',
        'dimensions': '16 24 32 48 64 96 128 200 256 512',
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '[%(levelname)s %(name)s] (%(asctime)s) %(message)s',
        },
        'short': {
            'format': '[%(levelname)s] %(message)s',
        },
    },
    'filters': {'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'}},
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'short',
        },
        'logfile': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './logs/cloudstore.log',
            'maxBytes': 2 * 1024 * 1024,
            'backupCount': 8,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['logfile', 'mail_admins'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'cloudstore': {
            'handlers': ['logfile', 'console', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
