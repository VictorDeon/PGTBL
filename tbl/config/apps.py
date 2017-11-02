"""
File to enter application dependencies in development and
production environments
"""

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

TBL_APPS = [
    'core',
    'accounts',
    'disciplines',
]

EXTERNAL_APPS = [
    'rolepermissions',
    'widget_tweaks',
]

PRODUCTION_APPS = DJANGO_APPS + TBL_APPS + EXTERNAL_APPS

DEVELOPMENT_APPS = ['django_extensions'] + PRODUCTION_APPS
