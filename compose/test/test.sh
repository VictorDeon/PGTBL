#!/bin/bash
#
# Purpose: Script to run tests into travis-ci
#
# Author: Victor Arnaud <victorhad@gmail.com>

echo "Creating migrations and insert into sqlite database"
python3 manage.py makemigrations
python3 manage.py migrate

echo "Run the tests"
coverage run --source="." manage.py test **/tests/
