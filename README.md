# TBL - Team-Based Learning

## Installation

* Get the github repository: ```git clone <repository_url>```

* Install dependencies to run python3 and pip3

  ```sh
  sudo apt-get update
  
  sudo apt-get install -y python3-dev sqlite python3-pip libpq-dev
  sudo apt-get install -y gettext
  ```

* Create a virtual development environment (virtualenvwrapper)

  ```sh
  sudo pip3 install --upgrade pip
  sudo pip3 install virtualenvwrapper
  ```

* Inside the .bashrc file insert:

  ```sh
  WORKON_HOME=~/.virtualenvs
  VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
  source /usr/local/bin/virtualenvwrapper.sh
  ```

  - To create a virtual environment: ```mkvirtualenv <venv_name>```

  - To enter the virtual environment: ```workon <venv_name>```

  - To exit the virtual environment: ```deactivate```

* Install project dependencies inside virtual environment

  ```sh
  pip install -r requeriments.txt
  ```

* Run Makefile commands to create database

  ```sh
  make migrations
  make migrate
  make superuser
  ```

* Run the django server

  ```sh
  make run
  ```

## Documentation and Badges

Documentation: [Wiki - TBL](https://github.com/TeamBasedLearning/TBL/wiki)

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/bcbcac621e1847e7af8e61bc202a03c6)](https://www.codacy.com/app/VictorArnaud/TBL?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=TeamBasedLearning/TBL&amp;utm_campaign=Badge_Grade)

[![Build Status](https://travis-ci.org/VictorArnaud/TBL.svg?branch=master)](https://travis-ci.org/VictorArnaud/TBL)
