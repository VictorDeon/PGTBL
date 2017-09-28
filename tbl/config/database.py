import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# This represent: tbl/settings/config/database
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DB_DEVELOPMENT = {
    'default': {
        # Add sqlite database on development enviroment
        'ENGINE': 'django.db.backends.sqlite3',
        # Path that will store the sqlite database
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DB_PRODUCTION = {
    'default': {
        # Add postgresql database on production
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # Name of database file
        'NAME': 'tbl',
        # Name of user on postgresql
        'USER': 'victor',
        # Password of user on postgresql
        'PASSWORD': 'victorhad',
        # Host and port of postgresql server
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}
