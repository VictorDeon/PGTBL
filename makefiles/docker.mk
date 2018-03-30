# DOCKER DEPLOY ------------------------------------------------
up:
	# Create and start containers
	sudo docker-compose up -d

build:
	# Rebuild the docker compose
	sudo docker-compose build

images:
	# List images
	sudo docker images

ps:
	# List all running containers
	sudo docker ps

psall:
	# List all containers
	sudo docker ps -a

top:
	# List running processes
	sudo docker-compose top

restart:
	# Restart services
	sudo docker-compose restart

start:
	# Start services
	sudo docker-compose start

stop:
	# Stop services
	sudo docker-compose stop

logs:
	# View output from containers
	sudo docker-compose logs

rm:
	# Remove all containers not running
	sudo docker-compose rm

help:
	# Help of docker-compose commands
	sudo docker-compose help

exec:
	# Get in the bash of tlb container
	sudo docker exec -it tbl bash
