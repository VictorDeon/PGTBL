# Continuos deploy
cd TBL
git fetch origin
git pull origin master
echo y | docker-compose -f ../docker-compose.deploy.yml rm --stop tbl
docker-compose -f ../docker-compose.deploy.yml up --build -d
