# Build an debian image
FROM python:3.6

# Update, Upgrade and configure locale
RUN apt-get update

# Install SO dependecies
RUN apt-get install -y python3-dev \
    python3-pip \
    libpq-dev \
    gettext \
    vim \
    build-essential

# Install pip dependecies
RUN pip3 install --upgrade pip

# Create developer user
RUN useradd -ms /bin/bash developer

# Insert Enviroment variable
ENV MODE_ENVIROMENT=development

# Create software folder and run requiriments
ADD . /home/developer/software
WORKDIR /home/developer/software
RUN pip3 install -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Create user developer
RUN chown -R developer: /home/developer/software
USER developer

# Run the script to create database in every command inside docker
RUN chmod +x compose/local/dev.sh
ENTRYPOINT ["compose/local/dev.sh"]

# Run the server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
