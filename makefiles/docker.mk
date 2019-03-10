# DOCKER DEPLOY ------------------------------------------------
up:
	# Create and start containers
	sudo docker-compose up -d

build:
	# Rebuild the docker compose
	sudo docker-compose build

restart:
	# Restart services
	sudo docker-compose restart

logs:
	# View output from containers
	sudo docker-compose logs -f -t

start:
	# Start services
	sudo docker-compose start

stop:
	# Stop services
	sudo docker-compose stop

ps:
	# List all running containers
	sudo docker-compose ps

down:
	# Stop and Remove all containers
	sudo docker-compose down

help:
	# Help of docker-compose commands
	sudo docker-compose help

images:
	# List images
	sudo docker images

exec:
	# Get in the bash of tlb container
	sudo docker-compose exec pgtbl bash
