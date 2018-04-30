# DOCKER DEPLOY ------------------------------------------------
file := "docker-compose.yml"

up:
# Create and start containers
ifeq (${file}, "docker-compose.yml")
	sudo docker-compose -f ${file} up -d
else
	sudo docker-compose -f ${file} up
endif

build:
	# Rebuild the docker compose
	sudo docker-compose -f ${file} build

restart:
	# Restart services
	sudo docker-compose -f ${file} restart

logs:
	# View output from containers
	sudo docker-compose -f ${file} logs -f -t

start:
	# Start services
	sudo docker-compose -f ${file} start

stop:
	# Stop services
	sudo docker-compose -f ${file} stop

ps:
	# List all running containers
	sudo docker-compose -f ${file} ps

down:
	# Stop and Remove all containers
	sudo docker-compose -f ${file} down

help:
	# Help of docker-compose commands
	sudo docker-compose help

images:
	# List images
	sudo docker images

exec:
	# Get in the bash of tlb container
	sudo docker exec -it tbl bash
