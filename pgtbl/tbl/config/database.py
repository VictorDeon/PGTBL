"""
File to insert the development and production database.

To more information:
https://docs.djangoproject.com/en/1.11/ref/settings/#databases
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# This represent: ../../../sqlite.db
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

# Development Database
SQLITE = {
    'default': {
        # Add sqlite database on development enviroment
        'ENGINE': 'django.db.backends.sqlite3',
        # Path that will store the sqlite database
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

POSTGRES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT')
    }
}
