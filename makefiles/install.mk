install: dependencies pip

dependencies:
	sudo apt-get update
	sudo apt-get -y upgrade
	sudo apt-get install -y python3-dev sqlite python3-pip libpq-dev
	sudo apt-get install -y gettext

pip: dependencies
	sudo pip3 install --upgrade pip
	sudo pip3 install virtualenvwrapper
	echo "# VIRTUALENV_ALREADY_ADDED" >> ~/.bashrc
	echo "WORKON_HOME=~/.virtualenvs" >> ~/.bashrc
	echo "VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc
	echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
