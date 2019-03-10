# DATABASE -----------------------------------------------------

migrations:
	# Create all migrations from models
	sudo docker-compose exec pgtbl python3 pgtbl/manage.py makemigrations

migrate:
	# Migrate all migrations on database
	sudo docker-compose exec pgtbl python3 pgtbl/manage.py migrate

superuser:
	# Create a super user on system.
	sudo docker-compose exec pgtbl python3 pgtbl/manage.py createsuperuser

# SHELL --------------------------------------------------------

shell:
	# Run iteractive shell of project.
	sudo docker-compose exec pgtbl python3 pgtbl/manage.py shell

# TRANSLATION --------------------------------------------------

app := "pgtbl"

messages:
	# Create a django.po to insert translations (pt-BR)
	sudo docker-compose exec pgtbl cd pgtbl/${app} && django-admin makemessages -l pt_BR -a

compilemessages:
	# Create translations
	sudo docker-compose exec pgtbl django-admin compilemessages

# STATIC FILES -------------------------------------------------

staticfiles:
	# Collect all static files
	sudo docker-compose exec pgtbl python3 pgtbl/manage.py collectstatic --noinput

# POPULATE DB --------------------------------------------------

json := database.json

fixture:
	# Create files with data model = app_label.ModelName e json = pgtbl/app_name/fixtures/model-name.json
	sudo docker-compose exec pgtbl python3 pgtbl/manage.py dumpdata ${model} --indent 4 > ${json}

populate:
	# Populate database with specific model
	sudo docker-compose exec pgtbl python3 pgtbl/manage.py loaddata pgtbl/**/fixtures/**.json
