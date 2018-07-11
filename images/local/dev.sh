#!/bin/bash
#
# Purpose: Config development enviroment
#
# Author: Victor Arnaud <victorhad@gmail.com>

echo "Creating migrations and insert into sqlite database"
python3 pgtbl/manage.py makemigrations
python3 pgtbl/manage.py migrate

echo "Run the server"
python3 pgtbl/manage.py runserver 0.0.0.0:8000
