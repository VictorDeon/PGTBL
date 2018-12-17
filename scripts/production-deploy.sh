#!/bin/bash
#
# Purpose: Continuous deploy on production enviroment
#
# Author: Victor Arnaud <victorhad@gmail.com>

sudo apt-get update && sudo apt-get install -y python3-pip && pip3 install django
pip3 install -r requirements/requirements-prod.txt
make staticfiles

sudo docker login --username $DOCKER_HUB_USER --password $DOCKER_HUB_PASS
sudo docker-compose -f docker-compose.production.yml build
sudo docker-compose -f docker-compose.production.yml push

# sudo apt-get install sshpass -y
# sshpass -p $SSH_PASSWORD ssh vagrant@192.168.45.21 '/bin/bash /home/vagrant/TBL/scripts/deploy.sh'
