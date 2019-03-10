# Continuos deploy
git fetch origin
echo y | sudo docker-compose rm --stop nginx
echo y | sudo docker-compose rm --stop pgtbl
git pull origin master
sudo docker-compose up -d --build
