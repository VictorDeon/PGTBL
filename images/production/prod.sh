#!/bin/bash
#
# Purpose: Config production enviroment
#
# Author: Victor Arnaud <victorhad@gmail.com>

# Waiting the PostgreSQL initialize
postgres_ready() {
python3 << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="", host="db")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgresql is unavailable - Waiting..."
  sleep 1
done

echo "Deleting migrations"
find . -path "pgtbl/*/migrations/*.pyc"  -delete
find . -path "pgtbl/*/migrations/*.py" -not -name "__init__.py" -delete

echo "Deleting staticfiles"
find . -path "pgtbl/tbl/staticfiles/*"  -delete
find . -path "pgtbl/tbl/mediafiles/*"  -delete

echo "Creating migrations and insert into psql database"
python3 pgtbl/manage.py makemigrations
python3 pgtbl/manage.py migrate

echo "Run server"
gunicorn --bind 0.0.0.0:8000 --chdir pgtbl tbl.wsgi
