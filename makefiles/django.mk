# SERVER -------------------------------------------------------

SERVER = 0.0.0.0:8080

run: pgtbl/manage.py
	# Run the development server
	python3 pgtbl/manage.py runserver ${SERVER}

# DATABASE -----------------------------------------------------

migrations: pgtbl/manage.py
	# Create all migrations from models
	python3 pgtbl/manage.py makemigrations

migrate: pgtbl/manage.py
	# Migrate all migrations on database
	python3 pgtbl/manage.py migrate

superuser: pgtbl/manage.py
	# Create a super user on system.
	python3 pgtbl/manage.py createsuperuser

sql: pgtbl/manage.py
	# Show SQL commands
	python3 pgtbl/manage.py sqlmigrate ${app_label} ${migration_name}

# SHELL --------------------------------------------------------

shell: pgtbl/manage.py
	# Run iteractive shell of project.
	python3 pgtbl/manage.py shell_plus

notebook: pgtbl/manage.py
	# Run iteractive shell notebook of project
	python3 pgtbl/manage.py shell_plus --notebook

# TRANSLATION --------------------------------------------------

files := "pgtbl/*.py"

messages:
	# Create a django.po to insert translations (pt-BR)
	django-admin makemessages -l pt_BR -i ${files}

compilemessages:
	# Create translations
	django-admin compilemessages

# STATIC FILES -------------------------------------------------

staticfiles: pgtbl/manage.py
	# Collect all static files
	python3 pgtbl/manage.py collectstatic --noinput

# POPULATE DB --------------------------------------------------

json := database.json

fixture: pgtbl/manage.py
	# Create files with data model = app_label.ModelName e json = pgtbl/app_name/fixtures/model-name.json
	python3 pgtbl/manage.py dumpdata ${model} --indent 4 > ${json}

populate: pgtbl/manage.py
	# Populate database with specific model
	python3 pgtbl/manage.py loaddata pgtbl/**/fixtures/**.json
