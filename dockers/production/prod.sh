#!/bin/bash
#
# Purpose: Config production enviroment
#
# Author: Victor Arnaud <victorhad@gmail.com>

echo "Deleting migrations"
find . -path "pgtbl/*/migrations/*.pyc"  -delete
find . -path "pgtbl/*/migrations/*.py" -not -name "__init__.py" -delete

echo "Creating migrations and insert into psql database"
make migrations
make migrate
make compilemessages

echo "Run server"
gunicorn --bind 0.0.0.0:8000 --chdir pgtbl tbl.wsgi --reload --graceful-timeout=900 --timeout=900 --log-level DEBUG --workers 5