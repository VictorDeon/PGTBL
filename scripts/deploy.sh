# Continuos deploy
git fetch origin
echo y | sudo docker-compose -f docker-compose.deploy.yml rm --stop tbl-nginx
echo y | sudo docker-compose -f docker-compose.deploy.yml rm --stop tbl
git pull origin master
sudo docker-compose -f docker-compose.deploy.yml up -d --build
