#!/bin/bash
#
# Purpose: Config production enviroment
#
# Author: Victor Arnaud <victorhad@gmail.com>

echo "Deleting migrations"
find . -path "pgtbl/*/migrations/*.pyc"  -delete
find . -path "pgtbl/*/migrations/*.py" -not -name "__init__.py" -delete

echo "Waiting for database connect"
postgres_ready() {
python3 << END
import sys
import psycopg2
import os
try:
    conn = psycopg2.connect(
      dbname=os.environ.get('POSTGRES_NAME', 'pgtbl_db'),
      user=os.environ.get('POSTGRES_USER', 'pgtbl'),
      password=os.environ.get('POSTGRES_PASSWORD', 'pgtbl'),
      host=os.environ.get('POSTGRES_HOST', 'db')
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "PostgreSQL is not available - Waiting..."
  sleep 1
done

echo "Creating migrations and insert into psql database"
make migrations
make migrate
make compilemessages

echo "Run server"
gunicorn --bind 0.0.0.0:8000 --chdir pgtbl tbl.wsgi --reload --graceful-timeout=900 --timeout=900 --log-level DEBUG --workers 5