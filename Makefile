# INSTALL --------------------------------------
install:
	# Create tbl enviroment
	# BUG: Not work yet
	mkvirtualenv tbl
	pip3 install -r requeriments-dev.txt
	python3 manage.py makemigrations
	python3 manage.py migrate
	django-admin makemessages
	django-admin compilemessages

dev:
	# Get in on dev enviroment
	workon dev

clean:
	# Search and clean all files .pyc and .pyo in __pycache__ directories
	# Run it before run make test
	find . | grep -E "(\.pyc|\.pyo)" | xargs rm -rf

# SERVER ---------------------------------------
run:
	# Run the development server
	python3 manage.py runserver 0.0.0.0:8080

# DATABASE -------------------------------------

migrations:
	# Create all migrations from models
	python3 manage.py makemigrations

migrate:
	# Migrate all migrations on database
	python3 manage.py migrate

superuser:
	# Create a super user on system.
	python3 manage.py createsuperuser

# SHELL ---------------------------------------

shell:
	# Run iteractive shell of project.
	python3 manage.py shell_plus

notebook:
	# Run iteractive shell notebook of project
	python3 manage.py shell_plus --notebook

# TRANSLATION ---------------------------------

messages:
	# Create a django.po to insert translations (pt-BR)
	django-admin makemessages -l pt_BR -i "tbl/*.py"

compilemessages:
	# Create translations
	django-admin compilemessages

# STATIC FILES --------------------------------

staticfiles:
	# Collect all static files
	python3 manage.py collectstatic

# TESTS ---------------------------------------

test:
	# Execute all tests
	coverage run --source="." manage.py test **/tests/

report:
	coverage report -m

html:
	coverage html

# DOCKER DEPLOY ---------------------------------

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
