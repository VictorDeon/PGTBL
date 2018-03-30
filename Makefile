# File Name: Makefile
# Purpose  : Symplify project commands
# Author   : Victor Arnaud
# Date     : 05/11/2017

# Execute some targets in django.mk file with command $ make
all: migrations migrate compilemessages superuser run

# Phone target are used when target not be a file
# If we have a file with same name of target, the
# command will run the same way.
.PHONE: all

# Documentation
doc-serve:
	# Run the mkdocs server
	mkdocs serve

doc:
	# Build the documentation
	mkdocs gh-deploy


# DJANGO
include makefiles/django.mk

# TEST
include makefiles/test.mk

# DOCKER
include makefiles/docker.mk

# INSTALL
include makefiles/install.mk

# SHELL
# make <target>: Execute the commands inside the target
# make -f <filename> <target>: Execute Makefile with another name
# make <target> -n: Show the commands that will be executed by this target
# make <target> -s: Execute the commands without show the commands (silense)
