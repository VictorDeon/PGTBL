"""
Django settings for tbl project.
"""

# Imports are being used indirectly, do not remove.
from .config import *
import os

# development or production enviroment
MODE_ENVIROMENT = os.getenv("MODE_ENVIROMENT", "development")

# Urls
ROOT_URLCONF = 'tbl.urls'

# WSGI - Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'tbl.wsgi.application'

# Internationalization
LANGUAGE_CODE = DEFAULT_LANGUAGE
TIME_ZONE = SAO_PAULO
USE_I18N = INTERNATIONALIZATION
USE_L10N = FORMAT_DATES
USE_TZ = TIMEZONE_DATETIMES

# Allow all host/domain to access this aplication
ALLOWED_HOSTS = ['*']

# Permissions
ROLEPERMISSIONS_MODULE = 'core.roles'

# Enviroments mode (development or production)
if MODE_ENVIROMENT == 'development':
    DEBUG = True
    INSTALLED_APPS = DEVELOPMENT_APPS
    DATABASES = SQLITE

elif MODE_ENVIROMENT == 'production':
    DEBUG = False
    INSTALLED_APPS = PRODUCTION_APPS
    DATABASES = POSTGRES
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
