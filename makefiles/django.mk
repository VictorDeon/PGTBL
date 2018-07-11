# SERVER -------------------------------------------------------

SERVER = 0.0.0.0:8080

run: manage.py
	# Run the development server
	python3 pgtbl/manage.py runserver ${SERVER}

# DATABASE -----------------------------------------------------

migrations: manage.py
	# Create all migrations from models
	python3 pgtbl/manage.py makemigrations

migrate: manage.py
	# Migrate all migrations on database
	python3 pgtbl/manage.py migrate

superuser: manage.py
	# Create a super user on system.
	python3 pgtbl/manage.py createsuperuser

sql: manage.py
	# Show SQL commands
	python3 pgtbl/manage.py sqlmigrate ${app_label} ${migration_name}

# SHELL --------------------------------------------------------

shell: manage.py
	# Run iteractive shell of project.
	python3 pgtbl/manage.py shell_plus

notebook: manage.py
	# Run iteractive shell notebook of project
	python3 pgtbl/manage.py shell_plus --notebook

# TRANSLATION --------------------------------------------------

files := "tbl/*.py"

messages:
	# Create a django.po to insert translations (pt-BR)
	django-admin makemessages -l pt_BR -i ${files}

compilemessages:
	# Create translations
	django-admin compilemessages

# STATIC FILES -------------------------------------------------

staticfiles: manage.py
	# Collect all static files
	python3 pgtbl/manage.py collectstatic
