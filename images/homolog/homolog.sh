#!/bin/bash
#
# Purpose: Config homolog enviroment
#
# Author: Victor Arnaud <victorhad@gmail.com>

echo "Creating migrations and insert into sqlite database"
make migrations
make migrate

echo "Run the server"
make run
